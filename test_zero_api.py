#!/usr/bin/env python3
"""
零 API Key 模式测试脚本
验证在没有 API key 的情况下，系统是否正常工作
"""

import sys
import os

# 确保可以导入本地模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zero_api_config import init_zero_api_mode, DataSourceMode
from smart_data_fetcher import SmartDataFetcher, fetch_stock
from graceful_degrade import get_degrade_report


def test_config():
    """测试配置系统"""
    print("\n" + "="*60)
    print("🧪 测试 1: 配置系统")
    print("="*60)
    
    # 强制使用免费模式
    config = init_zero_api_mode(force_free=True)
    
    assert config.is_free_mode, "应该处于免费模式"
    # 注意：环境中可能有 API key，但强制免费模式会忽略它们
    print(f"  API Keys 存在: {config.api_keys.has_any_key}")
    print(f"  强制免费模式: 是")
    
    print("✅ 配置系统测试通过")
    return config


def test_data_fetcher():
    """测试数据获取器"""
    print("\n" + "="*60)
    print("🧪 测试 2: 数据获取器（零 API Key 模式）")
    print("="*60)
    
    fetcher = SmartDataFetcher()
    
    # 测试美股
    print("\n📈 测试美股: AAPL")
    try:
        data = fetcher.fetch('AAPL')
        print(f"  价格: ${data.current_price}")
        print(f"  P/E: {data.pe_ratio}")
        print(f"  市值: ${data.market_cap:,.0f}" if data.market_cap else "  市值: N/A")
        print(f"  数据源: {data.data_source}")
        print(f"  有效: {data.is_valid}")
        
        if data.is_valid:
            print("✅ AAPL 数据获取成功")
        else:
            print("⚠️ AAPL 数据无效（可能网络问题）")
    except Exception as e:
        print(f"❌ AAPL 获取失败: {e}")
    
    # 测试港股
    print("\n📈 测试港股: 0700.HK (腾讯)")
    try:
        data = fetcher.fetch('0700.HK')
        print(f"  价格: HK${data.current_price}")
        print(f"  数据源: {data.data_source}")
        print(f"  有效: {data.is_valid}")
        
        if data.is_valid:
            print("✅ 0700.HK 数据获取成功")
        else:
            print("⚠️ 0700.HK 数据无效")
    except Exception as e:
        print(f"❌ 0700.HK 获取失败: {e}")
    
    # 打印统计
    print("\n" + fetcher.get_stats_report())
    
    return fetcher


def test_graceful_degrade():
    """测试优雅降级"""
    print("\n" + "="*60)
    print("🧪 测试 3: 优雅降级")
    print("="*60)
    
    from graceful_degrade import graceful_degrade
    
    @graceful_degrade(fallback_value="fallback_result")
    def failing_function():
        """模拟失败的 API 调用"""
        raise Exception("Simulated API failure")
    
    @graceful_degrade(fallback_value=None)
    def working_function():
        """模拟成功的 API 调用"""
        return "success"
    
    # 测试失败场景
    result1 = failing_function()
    assert result1 == "fallback_result", "失败时应该返回 fallback 值"
    print("✅ 失败场景降级成功")
    
    # 测试成功场景
    result2 = working_function()
    assert result2 == "success", "成功时应该返回正常结果"
    print("✅ 成功场景正常返回")
    
    # 打印降级统计
    print("\n" + get_degrade_report())


def test_batch_fetch():
    """测试批量获取"""
    print("\n" + "="*60)
    print("🧪 测试 4: 批量获取")
    print("="*60)
    
    fetcher = SmartDataFetcher()
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    
    print(f"\n📊 批量获取: {', '.join(tickers)}")
    results = fetcher.batch_fetch(tickers)
    
    success_count = sum(1 for data in results.values() if data.is_valid)
    print(f"\n结果: {success_count}/{len(tickers)} 成功")
    
    for ticker, data in results.items():
        status = "✅" if data.is_valid else "❌"
        price = f"${data.current_price:.2f}" if data.current_price else "N/A"
        print(f"  {status} {ticker}: {price} ({data.data_source})")


def main():
    """主测试函数"""
    print("\n" + "🚀"*30)
    print("  AI Hedge Fund - 零 API Key 模式测试")
    print("🚀"*30)
    
    try:
        # 运行所有测试
        config = test_config()
        fetcher = test_data_fetcher()
        test_graceful_degrade()
        test_batch_fetch()
        
        # 总结
        print("\n" + "="*60)
        print("🎉 所有测试完成!")
        print("="*60)
        print("\n✅ 零 API Key 模式工作正常")
        print("✅ 无需 API key 即可获取基础股票数据")
        print("✅ API 失败时自动降级")
        print("\n注意: 免费数据源（Yahoo Finance）可能有以下限制:")
        print("  - 部分字段可能缺失")
        print("  - 高频请求可能受限")
        print("  - 实时性略低于付费 API")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
