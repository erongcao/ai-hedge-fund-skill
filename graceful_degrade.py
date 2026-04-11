"""
优雅降级装饰器和工具
确保 API 失败时服务不中断
"""

import functools
import traceback
from typing import Any, Optional, Callable, TypeVar
from datetime import datetime
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')


class DegradeInfo:
    """降级信息记录"""
    def __init__(self):
        self.total_calls = 0
        self.success_calls = 0
        self.failed_calls = 0
        self.fallback_used = 0
        self.last_error = None
        self.last_error_time = None
    
    @property
    def success_rate(self) -> float:
        if self.total_calls == 0:
            return 1.0
        return self.success_calls / self.total_calls
    
    def record_success(self):
        self.total_calls += 1
        self.success_calls += 1
    
    def record_failure(self, error: Exception):
        self.total_calls += 1
        self.failed_calls += 1
        self.last_error = str(error)
        self.last_error_time = datetime.now()
    
    def record_fallback(self):
        self.fallback_used += 1


# 全局降级统计
degrade_stats: dict = {}


def graceful_degrade(
    fallback_value: Any = None,
    fallback_func: Optional[Callable] = None,
    log_level: str = "warning",
    raise_on_critical: bool = False,
    critical_exceptions: tuple = (KeyboardInterrupt, SystemExit)
):
    """
    优雅降级装饰器
    
    Args:
        fallback_value: API 失败时返回的默认值
        fallback_func: 可选的降级处理函数
        log_level: 日志级别 (debug, info, warning, error)
        raise_on_critical: 遇到关键异常时是否抛出
        critical_exceptions: 关键异常类型列表
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        func_name = func.__name__
        
        # 初始化统计
        if func_name not in degrade_stats:
            degrade_stats[func_name] = DegradeInfo()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            stats = degrade_stats[func_name]
            
            try:
                # 尝试执行原函数
                result = func(*args, **kwargs)
                stats.record_success()
                return result
                
            except critical_exceptions:
                # 关键异常，直接抛出
                raise
                
            except Exception as e:
                # 记录失败
                stats.record_failure(e)
                
                # 记录日志
                log_msg = f"[{func_name}] API call failed: {e}"
                if log_level == "debug":
                    logger.debug(log_msg)
                elif log_level == "info":
                    logger.info(log_msg)
                elif log_level == "warning":
                    logger.warning(log_msg)
                else:
                    logger.error(log_msg)
                    logger.error(traceback.format_exc())
                
                # 尝试降级处理
                if fallback_func:
                    try:
                        fallback_result = fallback_func(*args, **kwargs)
                        stats.record_fallback()
                        logger.info(f"[{func_name}] Fallback executed successfully")
                        return fallback_result
                    except Exception as fallback_error:
                        logger.error(f"[{func_name}] Fallback also failed: {fallback_error}")
                
                # 返回默认值
                if raise_on_critical and stats.success_rate < 0.5:
                    raise RuntimeError(
                        f"{func_name} has failed {stats.failed_calls} times "
                        f"({(1-stats.success_rate)*100:.1f}% failure rate)"
                    )
                
                logger.info(f"[{func_name}] Returning fallback value: {fallback_value}")
                return fallback_value
        
        # 附加统计方法
        wrapper.get_stats = lambda: degrade_stats[func_name]
        wrapper.reset_stats = lambda: degrade_stats.pop(func_name, None)
        
        return wrapper
    return decorator


def async_graceful_degrade(
    fallback_value: Any = None,
    fallback_func: Optional[Callable] = None,
    log_level: str = "warning"
):
    """异步版本的优雅降级装饰器"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        func_name = func.__name__
        
        if func_name not in degrade_stats:
            degrade_stats[func_name] = DegradeInfo()
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            stats = degrade_stats[func_name]
            
            try:
                result = await func(*args, **kwargs)
                stats.record_success()
                return result
            except Exception as e:
                stats.record_failure(e)
                
                log_msg = f"[{func_name}] Async API call failed: {e}"
                if log_level == "error":
                    logger.error(log_msg)
                else:
                    logger.warning(log_msg)
                
                if fallback_func:
                    try:
                        if asyncio.iscoroutinefunction(fallback_func):
                            fallback_result = await fallback_func(*args, **kwargs)
                        else:
                            fallback_result = fallback_func(*args, **kwargs)
                        stats.record_fallback()
                        return fallback_result
                    except Exception as fallback_error:
                        logger.error(f"[{func_name}] Async fallback failed: {fallback_error}")
                
                return fallback_value
        
        wrapper.get_stats = lambda: degrade_stats[func_name]
        return wrapper
    return decorator


def get_degrade_report() -> str:
    """获取降级统计报告"""
    if not degrade_stats:
        return "No API calls recorded yet."
    
    lines = ["\n📊 API 降级统计报告", "=" * 50]
    
    for func_name, stats in degrade_stats.items():
        lines.append(f"\n{func_name}:")
        lines.append(f"  总调用: {stats.total_calls}")
        lines.append(f"  成功: {stats.success_calls}")
        lines.append(f"  失败: {stats.failed_calls}")
        lines.append(f"  降级使用: {stats.fallback_used}")
        lines.append(f"  成功率: {stats.success_rate*100:.1f}%")
        if stats.last_error:
            lines.append(f"  最后错误: {stats.last_error}")
    
    lines.append("=" * 50)
    return "\n".join(lines)


def reset_all_stats():
    """重置所有统计"""
    global degrade_stats
    degrade_stats = {}
    logger.info("All degrade stats reset")


# 常用降级值
FALLBACK_VALUES = {
    'empty_list': [],
    'empty_dict': {},
    'empty_str': '',
    'zero': 0,
    'none': None,
    'neutral_sentiment': {
        'sentiment': 'neutral',
        'score': 50,
        'confidence': 'low',
        'note': 'Data unavailable, using neutral assumption'
    },
    'empty_analysis': {
        'signals': [],
        'consensus': 'hold',
        'confidence': 0,
        'note': 'Analysis failed, no recommendation'
    }
}


# 示例用法
if __name__ == "__main__":
    # 示例 1: 基本用法
    @graceful_degrade(fallback_value=None)
    def fetch_expensive_data(ticker: str):
        """模拟可能失败的 API 调用"""
        import random
        if random.random() < 0.5:
            raise Exception("API Error")
        return {"price": 100, "volume": 1000000}
    
    # 示例 2: 使用降级函数
    def fallback_fetch(ticker: str):
        print(f"Using fallback for {ticker}")
        return {"price": None, "volume": None, "source": "fallback"}
    
    @graceful_degrade(fallback_func=fallback_fetch)
    def fetch_with_fallback(ticker: str):
        raise Exception("Primary API failed")
    
    # 测试
    print("Testing graceful degrade...")
    for i in range(5):
        result = fetch_expensive_data("AAPL")
        print(f"Call {i+1}: {result}")
    
    print(fetch_with_fallback("MSFT"))
    print(get_degrade_report())
