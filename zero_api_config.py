"""
零 API Key 模式配置
自动检测 API key 可用性，优先使用免费数据源
"""

import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum


class DataSourceMode(Enum):
    """数据源模式"""
    FREE_ONLY = "free"           # 仅使用免费数据源
    ENHANCED = "enhanced"        # 使用 API 增强
    AUTO = "auto"                # 自动检测


@dataclass
class APIKeyManager:
    """API Key 管理器"""
    alpha_vantage: Optional[str] = None
    financial_datasets: Optional[str] = None
    brave_api: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'APIKeyManager':
        """从环境变量加载"""
        return cls(
            alpha_vantage=os.getenv('ALPHA_VANTAGE_API_KEY'),
            financial_datasets=os.getenv('FINANCIAL_DATASETS_API_KEY'),
            brave_api=os.getenv('BRAVE_API_KEY')
        )
    
    @property
    def has_any_key(self) -> bool:
        """是否有任何 API key"""
        return any([self.alpha_vantage, self.financial_datasets, self.brave_api])
    
    @property
    def available_sources(self) -> Dict[str, bool]:
        """返回可用的数据源"""
        return {
            'yahoo_finance': True,  # 始终可用
            'alpha_vantage': bool(self.alpha_vantage),
            'financial_datasets': bool(self.financial_datasets),
            'brave_news': bool(self.brave_api)
        }
    
    def get_status_report(self) -> str:
        """获取状态报告"""
        sources = self.available_sources
        lines = ["📊 数据源状态:"]
        for source, available in sources.items():
            status = "✅" if available else "❌"
            lines.append(f"  {status} {source}")
        return "\n".join(lines)


@dataclass
class ZeroAPIConfig:
    """零 API Key 模式配置"""
    mode: DataSourceMode = DataSourceMode.AUTO
    api_keys: APIKeyManager = field(default_factory=APIKeyManager.from_env)
    
    @classmethod
    def from_env(cls) -> 'ZeroAPIConfig':
        """从环境变量创建配置"""
        return cls()
    
    # 功能开关
    enable_news_analysis: bool = True      # 启用新闻分析（可用免费替代）
    enable_earnings_data: bool = True      # 启用财报数据（Yahoo免费）
    enable_analyst_ratings: bool = True    # 启用分析师评级（有限）
    enable_macro_data: bool = True         # 启用宏观数据（Yahoo免费）
    
    # 降级策略
    fallback_on_error: bool = True         # 错误时降级
    cache_enabled: bool = True             # 启用缓存
    cache_ttl_hours: int = 24              # 缓存有效期
    
    @property
    def effective_mode(self) -> DataSourceMode:
        """实际生效的模式"""
        if self.mode == DataSourceMode.AUTO:
            return DataSourceMode.ENHANCED if self.api_keys.has_any_key else DataSourceMode.FREE_ONLY
        return self.mode
    
    @property
    def is_free_mode(self) -> bool:
        """是否为免费模式"""
        return self.effective_mode == DataSourceMode.FREE_ONLY
    
    def get_data_source_priority(self) -> list:
        """获取数据源优先级列表"""
        if self.is_free_mode:
            return ['yahoo_finance', 'mock_data']
        else:
            return [
                'yahoo_finance',           # 1. 免费基础数据
                'financial_datasets',      # 2. 增强财务数据（如果有key）
                'alpha_vantage',          # 3. 备选数据源（如果有key）
                'mock_data'               # 4. 模拟数据（兜底）
            ]
    
    def print_config(self):
        """打印配置信息"""
        print("=" * 50)
        print("🚀 AI Hedge Fund - 配置信息")
        print("=" * 50)
        print(f"\n运行模式: {self.effective_mode.value.upper()}")
        print(self.api_keys.get_status_report())
        print(f"\n功能开关:")
        print(f"  新闻分析: {'✅' if self.enable_news_analysis else '❌'}")
        print(f"  财报数据: {'✅' if self.enable_earnings_data else '❌'}")
        print(f"  分析师评级: {'✅' if self.enable_analyst_ratings else '❌'}")
        print(f"  宏观数据: {'✅' if self.enable_macro_data else '❌'}")
        print(f"\n降级策略: {'启用' if self.fallback_on_error else '禁用'}")
        print("=" * 50)


# 全局配置实例
_config: Optional[ZeroAPIConfig] = None


def get_config() -> ZeroAPIConfig:
    """获取全局配置"""
    global _config
    if _config is None:
        _config = ZeroAPIConfig()
    return _config


def set_config(config: ZeroAPIConfig):
    """设置全局配置"""
    global _config
    _config = config


def init_zero_api_mode(force_free: bool = False):
    """
    初始化零 API Key 模式
    
    Args:
        force_free: 强制使用免费模式（忽略 API key）
    """
    config = ZeroAPIConfig.from_env()
    
    if force_free:
        config.mode = DataSourceMode.FREE_ONLY
        print("🆓 强制使用免费模式（忽略所有 API key）")
    
    set_config(config)
    config.print_config()
    
    return config


# 便捷函数
def is_free_mode() -> bool:
    """检查是否为免费模式"""
    return get_config().is_free_mode


def has_api_key(key_name: str) -> bool:
    """检查是否有特定 API key"""
    keys = get_config().api_keys
    return getattr(keys, key_name, None) is not None
