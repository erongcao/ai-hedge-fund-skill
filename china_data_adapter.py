"""
🇨🇳 China Stock Data Adapter
Integrates AKShare and Tushare for Chinese A-share analysis
"""

import os
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

# Try to import Chinese data libraries
try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False

try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    TUSHARE_AVAILABLE = False


@dataclass
class ChinaStockData:
    """Chinese stock data structure"""
    ticker: str
    name: str = ""
    current_price: Optional[float] = None
    change_pct: Optional[float] = None
    volume: Optional[float] = None
    turnover: Optional[float] = None
    
    # Valuation
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    market_cap: Optional[float] = None  # in billions
    
    # Financials
    revenue: Optional[float] = None
    net_profit: Optional[float] = None
    gross_margin: Optional[float] = None
    net_margin: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    debt_ratio: Optional[float] = None
    
    # Growth
    revenue_growth: Optional[float] = None
    profit_growth: Optional[float] = None
    
    # Technical
    ma5: Optional[float] = None
    ma10: Optional[float] = None
    ma20: Optional[float] = None
    ma60: Optional[float] = None
    rsi: Optional[float] = None
    macd: Optional[float] = None
    
    # Sector & Industry
    sector: str = ""
    industry: str = ""
    province: str = ""
    
    # Additional info
    listing_date: str = ""
    total_shares: Optional[float] = None
    float_shares: Optional[float] = None


class ChinaDataAdapter:
    """Adapter for Chinese stock data sources"""
    
    def __init__(self, tushare_token: Optional[str] = None):
        self.tushare_token = tushare_token or os.getenv('TUSHARE_TOKEN')
        if TUSHARE_AVAILABLE and self.tushare_token:
            ts.set_token(self.tushare_token)
            self.tushare_pro = ts.pro_api()
        else:
            self.tushare_pro = None
    
    def normalize_ticker(self, ticker: str) -> str:
        """Normalize ticker format for Chinese stocks"""
        # Remove .SZ, .SH suffixes if present
        ticker = ticker.upper().replace('.SZ', '').replace('.SH', '')
        
        # Add exchange prefix based on ticker rules
        if ticker.startswith('6'):
            return f"{ticker}.SH"  # Shanghai
        elif ticker.startswith('0') or ticker.startswith('3'):
            return f"{ticker}.SZ"  # Shenzhen
        return ticker
    
    def get_realtime_data(self, ticker: str) -> Optional[ChinaStockData]:
        """Get real-time stock data using AKShare"""
        if not AKSHARE_AVAILABLE:
            print("AKShare not available", file=sys.stderr)
            return None
        
        try:
            # Normalize ticker
            ticker_clean = ticker.upper().replace('.SZ', '').replace('.SH', '')
            
            # Get real-time data from AKShare
            df = ak.stock_zh_a_spot_em()
            
            # Find the stock
            stock_row = df[df['代码'] == ticker_clean]
            
            if stock_row.empty:
                return None
            
            row = stock_row.iloc[0]
            
            data = ChinaStockData(
                ticker=ticker,
                name=row.get('名称', ''),
                current_price=float(row['最新价']) if pd.notna(row['最新价']) else None,
                change_pct=float(row['涨跌幅']) if pd.notna(row['涨跌幅']) else None,
                volume=float(row['成交量']) / 10000 if pd.notna(row['成交量']) else None,  # in 万股
                turnover=float(row['成交额']) / 10000 if pd.notna(row['成交额']) else None,  # in 万元
                pe_ratio=float(row['市盈率-动态']) if pd.notna(row.get('市盈率-动态')) else None,
                pb_ratio=float(row['市净率']) if pd.notna(row.get('市净率')) else None,
                total_shares=float(row['总市值']) / 100000000 if pd.notna(row.get('总市值')) else None,  # in 亿
                market_cap=float(row['总市值']) / 100000000 if pd.notna(row.get('总市值')) else None,
                sector=row.get('所属行业', ''),
            )
            
            return data
            
        except Exception as e:
            print(f"AKShare error: {e}", file=sys.stderr)
            return None
    
    def get_financial_data(self, ticker: str) -> Optional[Dict]:
        """Get financial data using AKShare"""
        if not AKSHARE_AVAILABLE:
            return None
        
        try:
            import pandas as pd
            ticker_clean = ticker.upper().replace('.SZ', '').replace('.SH', '')
            
            # Get financial indicators
            try:
                df = ak.stock_financial_analysis_indicator(symbol=ticker_clean)
                if not df.empty:
                    latest = df.iloc[0]
                    return {
                        'roe': float(latest['净资产收益率(%)']) if '净资产收益率(%)' in latest else None,
                        'gross_margin': float(latest['销售毛利率(%)']) if '销售毛利率(%)' in latest else None,
                        'net_margin': float(latest['销售净利率(%)']) if '销售净利率(%)' in latest else None,
                        'debt_ratio': float(latest['资产负债率(%)']) if '资产负债率(%)' in latest else None,
                        'revenue_growth': float(latest['营业收入同比增长率(%)']) if '营业收入同比增长率(%)' in latest else None,
                        'profit_growth': float(latest['净利润同比增长率(%)']) if '净利润同比增长率(%)' in latest else None,
                    }
            except:
                pass
            
            # Fallback: Get basic financials
            try:
                df = ak.stock_financial_report_sina(stock=ticker_clean, symbol="利润表")
                if not df.empty:
                    latest = df.iloc[0]
                    return {
                        'revenue': float(latest.get('营业收入', 0)) / 100000000 if '营业收入' in latest else None,
                        'net_profit': float(latest.get('净利润', 0)) / 100000000 if '净利润' in latest else None,
                    }
            except:
                pass
            
            return None
            
        except Exception as e:
            print(f"Financial data error: {e}", file=sys.stderr)
            return None
    
    def get_historical_data(self, ticker: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """Get historical price data"""
        if not AKSHARE_AVAILABLE:
            return None
        
        try:
            import pandas as pd
            ticker_clean = ticker.upper().replace('.SZ', '').replace('.SH', '')
            
            # Get daily data
            df = ak.stock_zh_a_hist(symbol=ticker_clean, period="daily", 
                                    start_date="20240101", adjust="qfq")
            
            if df.empty:
                return None
            
            # Calculate technical indicators
            df['MA5'] = df['收盘'].rolling(5).mean()
            df['MA10'] = df['收盘'].rolling(10).mean()
            df['MA20'] = df['收盘'].rolling(20).mean()
            df['MA60'] = df['收盘'].rolling(60).mean()
            
            # Simple RSI calculation
            delta = df['收盘'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            return df
            
        except Exception as e:
            print(f"Historical data error: {e}", file=sys.stderr)
            return None
    
    def get_company_info(self, ticker: str) -> Optional[Dict]:
        """Get company basic information"""
        if not AKSHARE_AVAILABLE:
            return None
        
        try:
            ticker_clean = ticker.upper().replace('.SZ', '').replace('.SH', '')
            
            # Get individual stock info
            df = ak.stock_individual_info_em(symbol=ticker_clean)
            
            if df.empty:
                return None
            
            info = {}
            for _, row in df.iterrows():
                info[row['item']] = row['value']
            
            return {
                'name': info.get('股票简称', ''),
                'industry': info.get('行业', ''),
                'sector': info.get('行业', ''),
                'listing_date': info.get('上市时间', ''),
                'total_shares': info.get('总股本', ''),
                'float_shares': info.get('流通股', ''),
            }
            
        except Exception as e:
            print(f"Company info error: {e}", file=sys.stderr)
            return None
    
    def get_full_data(self, ticker: str) -> Optional[ChinaStockData]:
        """Get complete stock data"""
        # Get realtime data
        data = self.get_realtime_data(ticker)
        if not data:
            return None
        
        # Get financial data
        fin_data = self.get_financial_data(ticker)
        if fin_data:
            for key, value in fin_data.items():
                setattr(data, key, value)
        
        # Get company info
        comp_info = self.get_company_info(ticker)
        if comp_info:
            data.name = comp_info.get('name', data.name)
            data.industry = comp_info.get('industry', '')
            data.sector = comp_info.get('sector', '')
        
        # Get historical data for technicals
        hist = self.get_historical_data(ticker)
        if hist is not None and not hist.empty:
            latest = hist.iloc[-1]
            data.ma5 = float(latest['MA5']) if 'MA5' in latest and pd.notna(latest['MA5']) else None
            data.ma10 = float(latest['MA10']) if 'MA10' in latest and pd.notna(latest['MA10']) else None
            data.ma20 = float(latest['MA20']) if 'MA20' in latest and pd.notna(latest['MA20']) else None
            data.ma60 = float(latest['MA60']) if 'MA60' in latest and pd.notna(latest['MA60']) else None
            data.rsi = float(latest['RSI']) if 'RSI' in latest and pd.notna(latest['RSI']) else None
        
        return data
    
    def convert_to_enhanced_format(self, china_data: ChinaStockData) -> Dict:
        """Convert ChinaStockData to EnhancedStockData format"""
        return {
            'ticker': china_data.ticker,
            'name': china_data.name,
            'current_price': china_data.current_price,
            'pe_ratio': china_data.pe_ratio,
            'pb_ratio': china_data.pb_ratio,
            'market_cap': china_data.market_cap * 100000000 if china_data.market_cap else None,  # Convert back
            'sector': china_data.sector or china_data.industry,
            'roe': china_data.roe / 100 if china_data.roe else None,
            'gross_margin': china_data.gross_margin,
            'net_margin': china_data.net_margin,
            'debt_ratio': china_data.debt_ratio,
            'revenue_growth': china_data.revenue_growth,
            'profit_growth': china_data.profit_growth,
            'ma5': china_data.ma5,
            'ma10': china_data.ma10,
            'ma20': china_data.ma20,
            'ma60': china_data.ma60,
            'rsi': china_data.rsi,
        }


# Standalone test
if __name__ == "__main__":
    adapter = ChinaDataAdapter()
    
    # Test with 网宿科技
    print("Fetching data for 网宿科技 (300017)...")
    data = adapter.get_full_data("300017")
    
    if data:
        print(f"\n股票名称: {data.name}")
        print(f"当前价格: {data.current_price}")
        print(f"涨跌幅: {data.change_pct}%")
        print(f"市盈率: {data.pe_ratio}")
        print(f"市净率: {data.pb_ratio}")
        print(f"总市值: {data.market_cap}亿")
        print(f"行业: {data.industry}")
        print(f"ROE: {data.roe}%" if data.roe else "ROE: N/A")
        print(f"毛利率: {data.gross_margin}%" if data.gross_margin else "毛利率: N/A")
    else:
        print("Failed to fetch data")
