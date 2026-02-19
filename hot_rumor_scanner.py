"""
🔥 HOT SCANNER & RUMOR DETECTOR
Find trending stocks and early signals
Simplified version for ai-hedge-fund integration
"""

import json
import urllib.request
import ssl
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

SSL_CONTEXT = ssl.create_default_context()


@dataclass
class TrendingStock:
    """A trending stock entry"""
    ticker: str
    name: str
    change_pct: float
    volume_ratio: float  # vs average
    source: str
    sentiment: str  # bullish, bearish, neutral


@dataclass
class MarketRumor:
    """A market rumor or early signal"""
    ticker: str
    rumor_type: str  # merger, insider, upgrade, downgrade, general
    description: str
    confidence: str  # high, medium, low
    source: str


class HotScanner:
    """Scan for trending stocks and crypto"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        }
    
    def _fetch_json(self, url: str) -> Optional[Dict]:
        """Fetch JSON from URL"""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=15, context=SSL_CONTEXT) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            return None
    
    def get_trending_crypto(self, limit: int = 10) -> List[TrendingStock]:
        """Get trending crypto from CoinGecko"""
        results = []
        
        try:
            url = "https://api.coingecko.com/api/v3/search/trending"
            data = self._fetch_json(url)
            
            if data and "coins" in data:
                for item in data["coins"][:limit]:
                    coin = item.get("item", {})
                    price_data = coin.get("data", {})
                    price_change = price_data.get("price_change_percentage_24h", {}).get("usd", 0)
                    
                    results.append(TrendingStock(
                        ticker=f"{coin.get('symbol', '').upper()}-USD",
                        name=coin.get("name", ""),
                        change_pct=price_change or 0,
                        volume_ratio=2.0,  # Trending implies high volume
                        source="CoinGecko Trending",
                        sentiment="bullish" if (price_change or 0) > 0 else "bearish"
                    ))
        except Exception as e:
            pass
        
        return results
    
    def get_yahoo_movers(self) -> Dict[str, List[TrendingStock]]:
        """Get Yahoo Finance gainers, losers, most active"""
        results = {
            "gainers": [],
            "losers": [],
            "most_active": []
        }
        
        try:
            import yfinance as yf
            
            # Get S&P 500 components for scanning
            # Use a predefined list of popular stocks
            tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", 
                      "AMD", "CRM", "UBER", "COIN", "PLTR", "SOFI", "HOOD", "INTC",
                      "DIS", "BA", "JPM", "BAC", "XOM", "CVX", "PFE", "JNJ"]
            
            for ticker in tickers[:15]:  # Limit to avoid rate limits
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    hist = stock.history(period="2d")
                    
                    if len(hist) >= 2 and info:
                        current = hist['Close'].iloc[-1]
                        prev = hist['Close'].iloc[-2]
                        change_pct = ((current - prev) / prev) * 100
                        
                        # High volume indicator
                        avg_vol = info.get('averageVolume', 0)
                        recent_vol = info.get('volume', 0)
                        vol_ratio = (recent_vol / avg_vol) if avg_vol > 0 else 1.0
                        
                        entry = TrendingStock(
                            ticker=ticker,
                            name=info.get('shortName', ticker),
                            change_pct=change_pct,
                            volume_ratio=vol_ratio,
                            source="Yahoo Finance",
                            sentiment="bullish" if change_pct > 0 else "bearish"
                        )
                        
                        if change_pct > 3:
                            results["gainers"].append(entry)
                        elif change_pct < -3:
                            results["losers"].append(entry)
                        
                        if vol_ratio > 2.0:
                            results["most_active"].append(entry)
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            pass
        
        return results
    
    def get_hot_stocks(self) -> List[TrendingStock]:
        """Get combined hot stocks list"""
        hot = []
        
        # Add crypto
        hot.extend(self.get_trending_crypto(limit=5))
        
        # Add stock movers
        movers = self.get_yahoo_movers()
        hot.extend(movers["gainers"][:5])
        
        # Sort by absolute change
        hot.sort(key=lambda x: abs(x.change_pct), reverse=True)
        
        return hot[:15]


class RumorScanner:
    """Scan for market rumors and early signals"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/536.36",
        }
    
    def scan_for_ticker(self, ticker: str) -> List[MarketRumor]:
        """Scan for rumors about specific ticker"""
        rumors = []
        
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            news = stock.news
            
            if news:
                for item in news[:5]:
                    title = item.get('title', '')
                    content = item.get('summary', '')
                    publisher = item.get('publisher', 'Unknown')
                    
                    # Detect rumor types
                    rumor_type = self._detect_rumor_type(title + " " + content)
                    
                    if rumor_type:
                        confidence = self._assess_confidence(title, content, publisher)
                        
                        rumors.append(MarketRumor(
                            ticker=ticker,
                            rumor_type=rumor_type,
                            description=title,
                            confidence=confidence,
                            source=publisher
                        ))
                        
        except Exception as e:
            pass
        
        return rumors
    
    def _detect_rumor_type(self, text: str) -> Optional[str]:
        """Detect rumor type from text"""
        text_lower = text.lower()
        
        # M&A keywords
        if any(kw in text_lower for kw in ['merger', 'acquisition', 'acquire', 'takeover', 'buyout', 'm&a']):
            return 'merger'
        
        # Insider keywords
        if any(kw in text_lower for kw in ['insider buying', 'insider selling', 'insider trading', '13f', 'form 4']):
            return 'insider'
        
        # Upgrade/Downgrade
        if any(kw in text_lower for kw in ['upgrade', 'upgraded', 'raised to', 'price target raised']):
            return 'upgrade'
        if any(kw in text_lower for kw in ['downgrade', 'downgraded', 'lowered to', 'price target cut']):
            return 'downgrade'
        
        # Earnings
        if any(kw in text_lower for kw in ['earnings beat', 'earnings miss', 'eps surprise', 'guidance raised']):
            return 'earnings'
        
        # Partnership
        if any(kw in text_lower for kw in ['partnership', 'collaboration', 'deal with', 'contract']):
            return 'partnership'
        
        return None
    
    def _assess_confidence(self, title: str, content: str, publisher: str) -> str:
        """Assess rumor confidence"""
        # Reputable sources
        high_credibility = ['Reuters', 'Bloomberg', 'CNBC', 'WSJ', 'Financial Times', 'MarketWatch']
        
        if any(source in publisher for source in high_credibility):
            return 'high'
        
        # Specific keywords indicating higher confidence
        confidence_keywords = ['confirmed', 'announces', 'official', 'sec filing', 'reports']
        text_lower = (title + " " + content).lower()
        
        if any(kw in text_lower for kw in confidence_keywords):
            return 'medium'
        
        return 'low'
    
    def get_market_rumors(self, tickers: List[str] = None) -> Dict[str, List[MarketRumor]]:
        """Get market-wide rumors"""
        if tickers is None:
            tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "GOOGL", "AMZN", "META", "AMD"]
        
        all_rumors = {}
        
        for ticker in tickers:
            rumors = self.scan_for_ticker(ticker)
            if rumors:
                all_rumors[ticker] = rumors
        
        return all_rumors


def format_hot_scanner_results(hot_stocks: List[TrendingStock]) -> str:
    """Format hot scanner results for display"""
    lines = []
    lines.append("\n" + "="*70)
    lines.append("🔥 HOT SCANNER - Trending Stocks & Crypto")
    lines.append("="*70)
    
    if not hot_stocks:
        lines.append("\n  No hot stocks detected right now.")
        return "\n".join(lines)
    
    lines.append(f"\n  Found {len(hot_stocks)} trending assets\n")
    
    # Separate crypto and stocks
    crypto = [s for s in hot_stocks if s.ticker.endswith('-USD')]
    stocks = [s for s in hot_stocks if not s.ticker.endswith('-USD')]
    
    if stocks:
        lines.append("  📈 STOCKS:")
        lines.append("  " + "-"*50)
        for s in stocks[:10]:
            emoji = "🟢" if s.change_pct > 0 else "🔴"
            vol_ind = "🔥" if s.volume_ratio > 3 else "📊" if s.volume_ratio > 1.5 else ""
            lines.append(f"    {emoji} {s.ticker:<6} {s.change_pct:+6.2f}% {vol_ind}")
            lines.append(f"       {s.name[:30]} | {s.source}")
        lines.append("")
    
    if crypto:
        lines.append("  🪙 CRYPTO:")
        lines.append("  " + "-"*50)
        for c in crypto[:5]:
            emoji = "🚀" if c.change_pct > 0 else "📉"
            lines.append(f"    {emoji} {c.ticker:<10} {c.change_pct:+6.2f}%")
            lines.append(f"       {c.name} | {c.source}")
        lines.append("")
    
    lines.append("="*70 + "\n")
    return "\n".join(lines)


def format_rumor_results(rumors: Dict[str, List[MarketRumor]]) -> str:
    """Format rumor scanner results"""
    lines = []
    lines.append("\n" + "="*70)
    lines.append("🔮 RUMOR SCANNER - Early Signals & Market Whispers")
    lines.append("="*70)
    
    if not rumors:
        lines.append("\n  No significant rumors detected.")
        return "\n".join(lines)
    
    lines.append(f"\n  Detected rumors for {len(rumors)} tickers\n")
    
    for ticker, ticker_rumors in rumors.items():
        lines.append(f"  📰 {ticker}:")
        for r in ticker_rumors[:3]:  # Limit to 3 per ticker
            conf_emoji = {"high": "🔴", "medium": "🟡", "low": "⚪"}[r.confidence]
            type_emoji = {
                'merger': '🤝', 'insider': '👤', 'upgrade': '⬆️',
                'downgrade': '⬇️', 'earnings': '📊', 'partnership': '🤝'
            }.get(r.rumor_type, '💬')
            
            lines.append(f"    {conf_emoji} {type_emoji} [{r.rumor_type.upper()}] {r.description[:60]}...")
            lines.append(f"       Source: {r.source} | Confidence: {r.confidence}")
        lines.append("")
    
    lines.append("="*70 + "\n")
    return "\n".join(lines)


if __name__ == "__main__":
    # Test hot scanner
    scanner = HotScanner()
    hot = scanner.get_hot_stocks()
    print(format_hot_scanner_results(hot))
    
    # Test rumor scanner
    rumor_scanner = RumorScanner()
    rumors = rumor_scanner.get_market_rumors(["AAPL", "TSLA", "NVDA"])
    print(format_rumor_results(rumors))
