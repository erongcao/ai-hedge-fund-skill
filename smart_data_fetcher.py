"""
智能数据获取器 - 零 API Key 模式
优先使用免费数据源，API key 仅作为增强
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from functools import lru_cache

# 导入配置和降级工具
from zero_api_config import get_config, is_free_mode, DataSourceMode
from graceful_degrade import graceful_degrade, FALLBACK_VALUES

# 尝试导入可选依赖
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("Warning: yfinance not installed. Install with: pip3 install yfinance")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


@dataclass
class StockData:
    """标准化股票数据结构"""
    ticker: str
    current_price: Optional[float] = None
    currency: str = "USD"
    
    # 基础财务指标
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    ev_ebitda: Optional[float] = None
    
    # 盈利能力
    roe: Optional[float] = None
    roa: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    profit_margin: Optional[float] = None
    
    # 财务健康
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    interest_coverage: Optional[float] = None
    
    # 成长性
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None
    
    # 估值
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    beta: Optional[float] = None
    
    # 股息
    dividend_yield: Optional[float] = None
    dividend_rate: Optional[float] = None
    payout_ratio: Optional[float] = None
    
    # 技术数据
    fifty_day_avg: Optional[float] = None
    two_hundred_day_avg: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    
    # 公司信息
    company_name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    employees: Optional[int] = None
    
    # 元数据
    data_source: str = "unknown"
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    is_mock: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'ticker': self.ticker,
            'current_price': self.current_price,
            'currency': self.currency,
            'pe_ratio': self.pe_ratio,
            'pb_ratio': self.pb_ratio,
            'roe': self.roe,
            'debt_to_equity': self.debt_to_equity,
            'operating_margin': self.operating_margin,
            'revenue_growth': self.revenue_growth,
            'market_cap': self.market_cap,
            'beta': self.beta,
            'dividend_yield': self.dividend_yield,
            'sector': self.sector,
            'industry': self.industry,
            'data_source': self.data_source,
            'last_updated': self.last_updated,
            'is_mock': self.is_mock
        }
    
    @property
    def is_valid(self) -> bool:
        """检查数据是否有效（至少有价格）"""
        return self.current_price is not None and self.current_price > 0


class SmartDataFetcher:
    """
    智能数据获取器
    
    特性：
    1. 零 API Key 模式 - 优先使用 Yahoo Finance（免费）
    2. 自动降级 - API 失败时使用备用方案
    3. 智能缓存 - 减少重复请求
    4. 多数据源聚合 - 合并多个来源的数据
    """
    
    def __init__(self, config=None):
        self.config = config or get_config()
        self.cache = {}
        self.cache_ttl = timedelta(hours=self.config.cache_ttl_hours)
        
        # 统计信息
        self.stats = {
            'yahoo_calls': 0,
            'alpha_calls': 0,
            'cache_hits': 0,
            'fallbacks': 0
        }
    
    def fetch(self, ticker: str, use_cache: bool = True) -> StockData:
        """
        获取股票数据（智能路由）
        
        Args:
            ticker: 股票代码（如 AAPL, MSFT）
            use_cache: 是否使用缓存
            
        Returns:
            StockData 对象
        """
        # 检查缓存
        if use_cache and ticker in self.cache:
            cached_data, cached_time = self.cache[ticker]
            if datetime.now() - cached_time < self.cache_ttl:
                self.stats['cache_hits'] += 1
                print(f"📦 Cache hit for {ticker}")
                return cached_data
        
        # 获取数据（按优先级）
        data = self._fetch_with_fallback(ticker)
        
        # 更新缓存
        if use_cache:
            self.cache[ticker] = (data, datetime.now())
        
        return data
    
    def _fetch_with_fallback(self, ticker: str) -> StockData:
        """带降级的数据获取"""
        sources = self.config.get_data_source_priority()
        errors = []
        
        for source in sources:
            try:
                if source == 'yahoo_finance':
                    data = self._fetch_yahoo_finance(ticker)
                    if data.is_valid:
                        return data
                elif source == 'alpha_vantage' and not is_free_mode():
                    data = self._fetch_alpha_vantage(ticker)
                    if data.is_valid:
                        return data
                elif source == 'financial_datasets' and not is_free_mode():
                    data = self._fetch_financial_datasets(ticker)
                    if data.is_valid:
                        return data
                elif source == 'mock_data':
                    return self._generate_mock_data(ticker, errors)
                    
            except Exception as e:
                errors.append(f"{source}: {e}")
                continue
        
        # 所有来源都失败，返回空数据
        return StockData(
            ticker=ticker,
            data_source="failed",
            is_mock=True
        )
    
    @graceful_degrade(fallback_value=None)
    def _fetch_yahoo_finance(self, ticker: str) -> Optional[StockData]:
        """从 Yahoo Finance 获取数据（免费）"""
        if not YFINANCE_AVAILABLE:
            raise ImportError("yfinance not installed")
        
        self.stats['yahoo_calls'] += 1
        print(f"📡 Fetching {ticker} from Yahoo Finance...")
        
        stock = yf.Ticker(ticker)
        info = stock.info
        
        display_ticker = ticker
        
        return StockData(
            ticker=display_ticker,
            current_price=info.get('currentPrice') or info.get('regularMarketPrice'),
            currency=info.get('currency', 'USD'),
            
            pe_ratio=info.get('trailingPE'),
            pb_ratio=info.get('priceToBook'),
            ps_ratio=info.get('priceToSalesTrailing12Months'),
            
            roe=info.get('returnOnEquity'),
            roa=info.get('returnOnAssets'),
            gross_margin=info.get('grossMargins'),
            operating_margin=info.get('operatingMargins'),
            profit_margin=info.get('profitMargins'),
            
            debt_to_equity=info.get('debtToEquity'),
            current_ratio=info.get('currentRatio'),
            quick_ratio=info.get('quickRatio'),
            
            revenue_growth=info.get('revenueGrowth'),
            earnings_growth=info.get('earningsGrowth'),
            
            market_cap=info.get('marketCap'),
            enterprise_value=info.get('enterpriseValue'),
            beta=info.get('beta'),
            
            dividend_yield=info.get('dividendYield'),
            dividend_rate=info.get('dividendRate'),
            payout_ratio=info.get('payoutRatio'),
            
            fifty_day_avg=info.get('fiftyDayAverage'),
            two_hundred_day_avg=info.get('twoHundredDayAverage'),
            fifty_two_week_high=info.get('fiftyTwoWeekHigh'),
            fifty_two_week_low=info.get('fiftyTwoWeekLow'),
            
            company_name=info.get('longName') or info.get('shortName'),
            sector=info.get('sector'),
            industry=info.get('industry'),
            country=info.get('country'),
            employees=info.get('fullTimeEmployees'),
            
            data_source="Yahoo Finance",
            is_mock=False
        )
    
    @graceful_degrade(fallback_value=None)
    def _fetch_alpha_vantage(self, ticker: str) -> Optional[StockData]:
        """从 Alpha Vantage 获取数据（需要 API key）"""
        self.stats['alpha_calls'] += 1
        
        api_key = self.config.api_keys.alpha_vantage
        if not api_key:
            raise ValueError("Alpha Vantage API key not configured")
        
        print(f"📡 Fetching {ticker} from Alpha Vantage...")
        
        # 这里实现 Alpha Vantage API 调用
        # 简化示例
        import requests
        
        url = f"https://www.alphavantage.co/query"
        params = {
            'function': 'OVERVIEW',
            'symbol': ticker,
            'apikey': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'Note' in data:
            raise Exception("API call limit reached")
        
        # 转换为 StockData
        return StockData(
            ticker=ticker,
            current_price=None,  # 需要单独获取价格
            pe_ratio=float(data.get('PERatio', 0)) or None,
            pb_ratio=float(data.get('PriceToBookRatio', 0)) or None,
            roe=float(data.get('ReturnOnEquityTTM', 0)) or None,
            data_source="Alpha Vantage"
        )
    
    @graceful_degrade(fallback_value=None)
    def _fetch_financial_datasets(self, ticker: str) -> Optional[StockData]:
        """从 Financial Datasets 获取数据（需要 API key）"""
        api_key = self.config.api_keys.financial_datasets
        if not api_key:
            raise ValueError("Financial Datasets API key not configured")
        
        print(f"📡 Fetching {ticker} from Financial Datasets...")
        
        # 实现 Financial Datasets API 调用
        # 简化示例
        return None  # 占位
    
    def _generate_mock_data(self, ticker: str, errors: List[str]) -> StockData:
        """生成模拟数据（最后的兜底方案）"""
        self.stats['fallbacks'] += 1
        print(f"⚠️  Using mock data for {ticker} (all sources failed)")
        print(f"   Errors: {errors}")
        
        return StockData(
            ticker=ticker,
            current_price=None,
            data_source="mock",
            is_mock=True
        )
    
    def batch_fetch(self, tickers: List[str], max_workers: int = 5) -> Dict[str, StockData]:
        """
        批量获取股票数据
        
        Args:
            tickers: 股票代码列表
            max_workers: 最大并发数
            
        Returns:
            Dict[股票代码, StockData]
        """
        results = {}
        
        # 串行获取（避免触发 API 限制）
        for ticker in tickers:
            try:
                results[ticker] = self.fetch(ticker)
                time.sleep(0.5)  # 礼貌延迟
            except Exception as e:
                print(f"Error fetching {ticker}: {e}")
                results[ticker] = StockData(ticker=ticker, is_mock=True)
        
        return results
    
    def get_stats_report(self) -> str:
        """获取统计报告"""
        total_calls = self.stats['yahoo_calls'] + self.stats['alpha_calls']
        cache_hit_rate = (self.stats['cache_hits'] / max(total_calls, 1)) * 100
        
        return f"""
📊 SmartDataFetcher 统计:
  Yahoo Finance 调用: {self.stats['yahoo_calls']}
  Alpha Vantage 调用: {self.stats['alpha_calls']}
  缓存命中: {self.stats['cache_hits']} ({cache_hit_rate:.1f}%)
  降级次数: {self.stats['fallbacks']}
  运行模式: {self.config.effective_mode.value}
"""
    
    def clear_cache(self):
        """清除缓存"""
        self.cache.clear()
        print("Cache cleared")


# 便捷函数
def fetch_stock(ticker: str) -> StockData:
    """便捷函数：获取单只股票数据"""
    fetcher = SmartDataFetcher()
    return fetcher.fetch(ticker)


def fetch_stocks(tickers: List[str]) -> Dict[str, StockData]:
    """便捷函数：批量获取股票数据"""
    fetcher = SmartDataFetcher()
    return fetcher.batch_fetch(tickers)


# 测试代码
if __name__ == "__main__":
    print("🚀 Testing SmartDataFetcher...")
    print("=" * 50)
    
    # 初始化配置
    from zero_api_config import init_zero_api_mode
    config = init_zero_api_mode(force_free=True)
    
    # 创建获取器
    fetcher = SmartDataFetcher(config)
    
    # 测试获取
    test_tickers = ['AAPL', 'MSFT', 'GOOGL']
    
    for ticker in test_tickers:
        print(f"\n📈 Fetching {ticker}...")
        try:
            data = fetcher.fetch(ticker)
            print(f"  Price: {data.current_price}")
            print(f"  P/E: {data.pe_ratio}")
            print(f"  Source: {data.data_source}")
            print(f"  Valid: {data.is_valid}")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + fetcher.get_stats_report())
