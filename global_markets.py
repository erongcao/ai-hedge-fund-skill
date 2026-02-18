#!/usr/bin/env python3
"""
AI Hedge Fund - Global Markets Module
Support for international stock markets (Hong Kong, China A-shares, Europe, etc.)
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ai_hedge_fund_advanced import DataFetcher as BaseDataFetcher

@dataclass
class MarketInfo:
    """Information about a stock market"""
    code: str
    name: str
    country: str
    timezone: str
    currency: str
    trading_hours: str
    tick_size_rules: str
    min_lot_size: int
    supported: bool

@dataclass
class StockInfo:
    """Universal stock information"""
    ticker: str
    local_ticker: str
    name: str
    market: str
    currency: str
    sector: str
    industry: str
    market_cap_usd: float
    pe_ratio: float
    pb_ratio: float
    ytd_return: float

class GlobalMarketRegistry:
    """Registry of global stock markets"""
    
    MARKETS = {
        # United States
        "US": MarketInfo("US", "US Stocks", "USA", "EST", "USD", "09:30-16:00", "0.01", 1, True),
        "NYSE": MarketInfo("NYSE", "New York Stock Exchange", "USA", "EST", "USD", "09:30-16:00", "0.01", 1, True),
        "NASDAQ": MarketInfo("NASDAQ", "NASDAQ", "USA", "EST", "USD", "09:30-16:00", "0.01", 1, True),
        
        # China A-Shares
        "SS": MarketInfo("SS", "Shanghai Stock Exchange", "China", "CST", "CNY", "09:30-15:00", "0.01", 100, True),
        "SZ": MarketInfo("SZ", "Shenzhen Stock Exchange", "China", "CST", "CNY", "09:30-15:00", "0.01", 100, True),
        
        # Hong Kong
        "HK": MarketInfo("HK", "Hong Kong Stock Exchange", "Hong Kong", "HKT", "HKD", "09:30-16:00", "0.01-0.05", 100, True),
        
        # Europe
        "L": MarketInfo("L", "London Stock Exchange", "UK", "GMT", "GBP", "08:00-16:30", "0.01", 1, True),
        "PA": MarketInfo("PA", "Euronext Paris", "France", "CET", "EUR", "09:00-17:30", "0.01", 1, True),
        "DE": MarketInfo("DE", "Deutsche Börse", "Germany", "CET", "EUR", "09:00-17:30", "0.01", 1, True),
        
        # Japan
        "T": MarketInfo("T", "Tokyo Stock Exchange", "Japan", "JST", "JPY", "09:00-15:00", "1", 100, True),
        
        # Other Asia
        "KS": MarketInfo("KS", "Korea Exchange", "South Korea", "KST", "KRW", "09:00-15:30", "1", 1, True),
        "SI": MarketInfo("SI", "Singapore Exchange", "Singapore", "SGT", "SGD", "09:00-17:00", "0.01", 100, True),
        "AU": MarketInfo("AU", "Australian Securities Exchange", "Australia", "AET", "AUD", "10:00-16:00", "0.01", 1, True),
        
        # Canada
        "TO": MarketInfo("TO", "Toronto Stock Exchange", "Canada", "EST", "CAD", "09:30-16:00", "0.01", 1, True),
        
        # India
        "NS": MarketInfo("NS", "National Stock Exchange of India", "India", "IST", "INR", "09:15-15:30", "0.05", 1, True),
        "BO": MarketInfo("BO", "Bombay Stock Exchange", "India", "IST", "INR", "09:15-15:30", "0.05", 1, True),
    }
    
    @classmethod
    def get_market(cls, code: str) -> Optional[MarketInfo]:
        """Get market info by code"""
        return cls.MARKETS.get(code.upper())
    
    @classmethod
    def list_markets(cls) -> List[MarketInfo]:
        """List all supported markets"""
        return list(cls.MARKETS.values())
    
    @classmethod
    def detect_market(cls, ticker: str) -> Tuple[str, str]:
        """
        Detect market from ticker format
        Returns: (market_code, local_ticker)
        """
        ticker = ticker.upper().strip()
        
        # US stocks (no suffix)
        if re.match(r'^[A-Z]{1,5}$', ticker):
            return "US", ticker
        
        # Hong Kong (4 digits .HK)
        if re.match(r'^\d{4,5}\.HK$', ticker):
            return "HK", ticker.replace('.HK', '')
        
        # Shanghai (.SS)
        if ticker.endswith('.SS'):
            return "SS", ticker.replace('.SS', '')
        
        # Shenzhen (.SZ)
        if ticker.endswith('.SZ'):
            return "SZ", ticker.replace('.SZ', '')
        
        # London (.L)
        if ticker.endswith('.L'):
            return "L", ticker.replace('.L', '')
        
        # Tokyo (.T)
        if ticker.endswith('.T'):
            return "T", ticker.replace('.T', '')
        
        # Toronto (.TO)
        if ticker.endswith('.TO'):
            return "TO", ticker.replace('.TO', '')
        
        # India (.NS, .BO)
        if ticker.endswith('.NS'):
            return "NS", ticker.replace('.NS', '')
        if ticker.endswith('.BO'):
            return "BO", ticker.replace('.BO', '')
        
        # Korea (.KS)
        if ticker.endswith('.KS'):
            return "KS", ticker.replace('.KS', '')
        
        # Singapore (.SI)
        if ticker.endswith('.SI'):
            return "SI", ticker.replace('.SI', '')
        
        # Australia (.AX)
        if ticker.endswith('.AX'):
            return "AU", ticker.replace('.AX', '')
        
        # Paris (.PA)
        if ticker.endswith('.PA'):
            return "PA", ticker.replace('.PA', '')
        
        # Default to US
        return "US", ticker

class GlobalDataFetcher:
    """Fetch data for global markets"""
    
    def __init__(self):
        self.base_fetcher = BaseDataFetcher()
        self.registry = GlobalMarketRegistry()
    
    def get_stock_data(self, ticker: str) -> Dict:
        """Get stock data with market detection"""
        market_code, local_ticker = self.registry.detect_market(ticker)
        market = self.registry.get_market(market_code)
        
        print(f"📍 Detected market: {market.name if market else 'Unknown'} ({market_code})", file=sys.stderr)
        
        # Fetch using yfinance with proper ticker format
        yf_ticker = self._format_for_yfinance(ticker, market_code)
        data = self._fetch_from_yfinance(yf_ticker)
        
        # Add market info
        if data:
            data['market'] = market_code
            data['market_name'] = market.name if market else 'Unknown'
            data['currency'] = market.currency if market else 'USD'
            data['local_ticker'] = local_ticker
        
        return data
    
    def _format_for_yfinance(self, ticker: str, market: str) -> str:
        """Format ticker for yfinance"""
        # yfinance uses different suffixes
        suffix_map = {
            "SS": ".SS",
            "SZ": ".SZ",
            "HK": ".HK",
            "L": ".L",
            "T": ".T",
            "PA": ".PA",
            "DE": ".DE",
            "TO": ".TO",
            "NS": ".NS",
            "BO": ".BO",
            "KS": ".KS",
            "SI": ".SI",
            "AU": ".AX",
        }
        
        if market in suffix_map:
            # Extract base ticker and add correct suffix
            base = ticker.split('.')[0]
            return base + suffix_map[market]
        
        return ticker
    
    def _fetch_from_yfinance(self, ticker: str) -> Dict:
        """Fetch data using yfinance"""
        try:
            import yfinance as yf
            
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1y")
            
            current_price = hist['Close'].iloc[-1] if not hist.empty else None
            
            # Calculate moving averages
            avg_50 = hist['Close'].rolling(50).mean().iloc[-1] if len(hist) >= 50 else None
            avg_200 = hist['Close'].rolling(200).mean().iloc[-1] if len(hist) >= 200 else None
            
            return {
                "ticker": ticker,
                "current_price": current_price,
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "pb_ratio": info.get("priceToBook"),
                "roe": info.get("returnOnEquity"),
                "debt_to_equity": info.get("debtToEquity"),
                "operating_margin": info.get("operatingMargins"),
                "dividend_yield": info.get("dividendYield"),
                "beta": info.get("beta"),
                "avg_50": avg_50,
                "avg_200": avg_200,
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "name": info.get("longName"),
                "business_summary": info.get("longBusinessSummary", "")[:1000],
            }
        except Exception as e:
            print(f"Error fetching {ticker}: {e}", file=sys.stderr)
            return {}
    
    def get_market_summary(self, market_code: str) -> Dict:
        """Get market summary for a specific market"""
        market = self.registry.get_market(market_code)
        if not market:
            return {"error": f"Unknown market: {market_code}"}
        
        # Fetch market index
        index_tickers = {
            "US": "^GSPC",      # S&P 500
            "HK": "^HSI",       # Hang Seng
            "SS": "000001.SS",  # Shanghai Composite
            "SZ": "399001.SZ",  # Shenzhen Component
            "T": "^N225",       # Nikkei 225
            "L": "^FTSE",       # FTSE 100
            "DE": "^GDAXI",     # DAX
            "PA": "^FCHI",      # CAC 40
            "KS": "^KS11",      # KOSPI
            "AU": "^AXJO",      # ASX 200
            "NS": "^NSEI",      # Nifty 50
        }
        
        index_ticker = index_tickers.get(market_code)
        index_data = {}
        
        if index_ticker:
            try:
                import yfinance as yf
                index = yf.Ticker(index_ticker)
                hist = index.history(period="1mo")
                if not hist.empty:
                    latest = hist['Close'].iloc[-1]
                    prev = hist['Close'].iloc[-2] if len(hist) > 1 else latest
                    change = (latest - prev) / prev if prev > 0 else 0
                    index_data = {
                        "index_name": index_tickers.get(market_code, ""),
                        "latest_value": latest,
                        "daily_change": change
                    }
            except:
                pass
        
        return {
            "market": market.__dict__,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "index": index_data
        }
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str = "USD") -> float:
        """Convert currency using approximate rates (in production, use real-time rates)"""
        # Approximate rates (should use real API in production)
        rates = {
            "USD": 1.0,
            "CNY": 0.14,
            "HKD": 0.13,
            "JPY": 0.0067,
            "EUR": 1.09,
            "GBP": 1.27,
            "KRW": 0.00075,
            "SGD": 0.74,
            "AUD": 0.65,
            "CAD": 0.74,
            "INR": 0.012,
        }
        
        from_rate = rates.get(from_currency, 1.0)
        to_rate = rates.get(to_currency, 1.0)
        
        return amount * (from_rate / to_rate)

class GlobalStockAnalyzer:
    """Analyze stocks across global markets"""
    
    def __init__(self):
        self.fetcher = GlobalDataFetcher()
    
    def analyze_stock(self, ticker: str) -> Dict:
        """Analyze a stock from any market"""
        market_code, local_ticker = GlobalMarketRegistry.detect_market(ticker)
        data = self.fetcher.get_stock_data(ticker)
        
        if not data:
            return {"error": f"Could not fetch data for {ticker}"}
        
        # Add market context
        market = GlobalMarketRegistry.get_market(market_code)
        
        analysis = {
            "ticker": ticker,
            "local_ticker": local_ticker,
            "market": market_code,
            "market_name": market.name if market else "Unknown",
            "currency": data.get("currency", "USD"),
            "company_name": data.get("name", ""),
            "current_price": data.get("current_price"),
            "market_cap_usd": self._convert_market_cap(data.get("market_cap"), data.get("currency", "USD")),
            "valuation": {
                "pe_ratio": data.get("pe_ratio"),
                "pb_ratio": data.get("pb_ratio"),
            },
            "profitability": {
                "roe": data.get("roe"),
                "operating_margin": data.get("operating_margin"),
            },
            "risk": {
                "beta": data.get("beta"),
                "debt_to_equity": data.get("debt_to_equity"),
            },
            "sector": data.get("sector"),
            "industry": data.get("industry"),
        }
        
        return analysis
    
    def _convert_market_cap(self, market_cap: float, currency: str) -> float:
        """Convert market cap to USD"""
        if not market_cap:
            return None
        return self.fetcher.convert_currency(market_cap, currency, "USD")
    
    def compare_across_markets(self, tickers: List[str]) -> List[Dict]:
        """Compare stocks from different markets"""
        results = []
        for ticker in tickers:
            try:
                analysis = self.analyze_stock(ticker)
                results.append(analysis)
            except Exception as e:
                print(f"Error analyzing {ticker}: {e}", file=sys.stderr)
        
        return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Hedge Fund - Global Markets")
    parser.add_argument("command", choices=["analyze", "market", "list-markets", "convert"],
                       help="Command to execute")
    parser.add_argument("--ticker", "-t", help="Stock ticker")
    parser.add_argument("--market", "-m", help="Market code")
    parser.add_argument("--tickers", help="Comma-separated tickers for comparison")
    parser.add_argument("--amount", type=float, help="Amount to convert")
    parser.add_argument("--from-currency", help="Source currency")
    parser.add_argument("--to-currency", default="USD", help="Target currency")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    try:
        if args.command == "list-markets":
            markets = GlobalMarketRegistry.list_markets()
            if args.json:
                print(json.dumps([m.__dict__ for m in markets], indent=2))
            else:
                print("\n🌍 Supported Global Markets:\n")
                print(f"{'Code':<8} {'Name':<30} {'Country':<15} {'Currency':<8} {'Hours'}")
                print("-" * 90)
                for m in markets:
                    if m.supported:
                        print(f"{m.code:<8} {m.name:<30} {m.country:<15} {m.currency:<8} {m.trading_hours}")
                print()
        
        elif args.command == "analyze":
            if not args.ticker:
                print("Error: --ticker required", file=sys.stderr)
                sys.exit(1)
            
            analyzer = GlobalStockAnalyzer()
            result = analyzer.analyze_stock(args.ticker)
            
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n📊 Analysis: {result['company_name'] or result['ticker']}")
                print(f"Market: {result['market_name']} ({result['market']})")
                print(f"Price: {result['current_price']} {result['currency']}")
                if result['market_cap_usd']:
                    print(f"Market Cap: ${result['market_cap_usd']/1e9:.1f}B USD")
                print(f"P/E: {result['valuation']['pe_ratio']}")
                print()
        
        elif args.command == "market":
            if not args.market:
                print("Error: --market required", file=sys.stderr)
                sys.exit(1)
            
            fetcher = GlobalDataFetcher()
            summary = fetcher.get_market_summary(args.market)
            
            if args.json:
                print(json.dumps(summary, indent=2))
            else:
                print(f"\n📈 Market Summary: {summary['market']['name']}")
                print(f"Currency: {summary['market']['currency']}")
                print(f"Trading Hours: {summary['market']['trading_hours']}")
                if summary.get('index'):
                    idx = summary['index']
                    print(f"Index: {idx.get('index_name', 'N/A')}")
                    print(f"Latest: {idx.get('latest_value', 'N/A')}")
                print()
        
        elif args.command == "convert":
            if not all([args.amount, args.from_currency]):
                print("Error: --amount and --from-currency required", file=sys.stderr)
                sys.exit(1)
            
            fetcher = GlobalDataFetcher()
            result = fetcher.convert_currency(args.amount, args.from_currency, args.to_currency)
            
            if args.json:
                print(json.dumps({
                    "amount": args.amount,
                    "from": args.from_currency,
                    "to": args.to_currency,
                    "result": result
                }))
            else:
                print(f"{args.amount:,.2f} {args.from_currency} = {result:,.2f} {args.to_currency}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()