#!/usr/bin/env python3
"""
AI Hedge Fund Skill - OpenClaw Integration
Uses parallel sub-agents to simulate legendary investors analyzing stocks.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Literal, Optional
from dataclasses import dataclass, asdict

# Try to import optional dependencies
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

@dataclass
class AgentSignal:
    """Signal from an investment agent"""
    agent_name: str
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int  # 0-100
    reasoning: str
    key_metrics: Optional[Dict] = None

@dataclass
class ConsensusResult:
    """Final consensus from all agents"""
    ticker: str
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int
    agreement: str
    agent_signals: List[AgentSignal]
    key_risks: List[str]
    recommendation: str
    analysis_date: str

class DataFetcher:
    """Fetch financial data from various sources"""
    
    def __init__(self):
        self.cache = {}
        
    def get_stock_data(self, ticker: str, period: str = "1y") -> Dict:
        """Fetch stock data from Yahoo Finance"""
        if not YFINANCE_AVAILABLE:
            return self._get_mock_data(ticker)
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period=period)
            
            # Calculate basic metrics
            current_price = hist['Close'].iloc[-1] if not hist.empty else None
            avg_50 = hist['Close'].rolling(50).mean().iloc[-1] if len(hist) >= 50 else None
            avg_200 = hist['Close'].rolling(200).mean().iloc[-1] if len(hist) >= 200 else None
            
            # Calculate RSI
            rsi = self._calculate_rsi(hist['Close']) if not hist.empty else None
            
            return {
                "ticker": ticker,
                "current_price": current_price,
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "pb_ratio": info.get("priceToBook"),
                "roe": info.get("returnOnEquity"),
                "debt_to_equity": info.get("debtToEquity"),
                "operating_margin": info.get("operatingMargins"),
                "current_ratio": info.get("currentRatio"),
                "dividend_yield": info.get("dividendYield"),
                "avg_50": avg_50,
                "avg_200": avg_200,
                "rsi": rsi,
                "beta": info.get("beta"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "business_summary": info.get("longBusinessSummary", "")[:500],
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}", file=sys.stderr)
            return self._get_mock_data(ticker)
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        if PANDAS_AVAILABLE and len(prices) >= period:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1]
        return 50.0  # Neutral
    
    def _get_mock_data(self, ticker: str) -> Dict:
        """Return mock data for testing"""
        return {
            "ticker": ticker,
            "current_price": 150.0,
            "market_cap": 2000000000000,
            "pe_ratio": 25.0,
            "pb_ratio": 3.0,
            "roe": 0.15,
            "debt_to_equity": 0.3,
            "operating_margin": 0.20,
            "current_ratio": 1.5,
            "dividend_yield": 0.02,
            "avg_50": 145.0,
            "avg_200": 140.0,
            "rsi": 55.0,
            "beta": 1.1,
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "business_summary": f"Leading technology company {ticker}",
        }

class InvestmentAgent:
    """Base class for investment agents"""
    
    def __init__(self, name: str, philosophy: str):
        self.name = name
        self.philosophy = philosophy
    
    def analyze(self, data: Dict) -> AgentSignal:
        """Analyze stock data and return signal - override in subclass"""
        raise NotImplementedError

class WarrenBuffettAgent(InvestmentAgent):
    """Warren Buffett value investing analysis"""
    
    def __init__(self):
        super().__init__(
            "Warren Buffett",
            "Wonderful companies at fair prices. Focus on moat, ROE, and margin of safety."
        )
    
    def analyze(self, data: Dict) -> AgentSignal:
        score = 0
        max_score = 100
        reasoning_parts = []
        
        # ROE analysis (most important for Buffett)
        roe = data.get("roe", 0)
        if roe and roe > 0.15:
            score += 25
            reasoning_parts.append(f"Strong ROE of {roe:.1%}")
        elif roe and roe > 0.10:
            score += 15
            reasoning_parts.append(f"Good ROE of {roe:.1%}")
        else:
            reasoning_parts.append("Weak or missing ROE")
        
        # Debt levels
        debt = data.get("debt_to_equity", 0)
        if debt and debt < 0.5:
            score += 15
            reasoning_parts.append("Conservative debt levels")
        elif debt and debt < 1.0:
            score += 5
        else:
            reasoning_parts.append("High debt levels")
        
        # Operating margin
        margin = data.get("operating_margin", 0)
        if margin and margin > 0.15:
            score += 20
            reasoning_parts.append("Strong operating margins")
        elif margin and margin > 0.10:
            score += 10
        
        # Price vs moving averages (trend)
        price = data.get("current_price", 0)
        avg200 = data.get("avg_200", 0)
        if price and avg200 and price > avg200:
            score += 10
            reasoning_parts.append("Price above 200-day MA (uptrend)")
        
        # Valuation check
        pe = data.get("pe_ratio", 0)
        if pe and pe < 20:
            score += 20
            reasoning_parts.append(f"Reasonable P/E of {pe:.1f}")
        elif pe and pe < 30:
            score += 10
        else:
            reasoning_parts.append(f"High P/E of {pe:.1f}")
        
        # Determine signal
        if score >= 70:
            signal = "bullish"
        elif score >= 40:
            signal = "neutral"
        else:
            signal = "bearish"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=score,
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "Insufficient data",
            key_metrics={"roe": roe, "debt_to_equity": debt, "operating_margin": margin, "pe_ratio": pe}
        )

class BenGrahamAgent(InvestmentAgent):
    """Ben Graham margin of safety analysis"""
    
    def __init__(self):
        super().__init__(
            "Ben Graham",
            "Margin of safety. Buy at discount to intrinsic value."
        )
    
    def analyze(self, data: Dict) -> AgentSignal:
        score = 0
        reasoning_parts = []
        
        pe = data.get("pe_ratio", 0)
        pb = data.get("pb_ratio", 0)
        current_ratio = data.get("current_ratio", 0)
        
        # P/E analysis
        if pe and pe < 15:
            score += 30
            reasoning_parts.append(f"Attractive P/E of {pe:.1f}")
        elif pe and pe < 25:
            score += 15
        else:
            reasoning_parts.append(f"High P/E of {pe:.1f}")
        
        # P/B analysis
        if pb and pb < 1.5:
            score += 25
            reasoning_parts.append(f"Good P/B of {pb:.1f}")
        elif pb and pb < 3.0:
            score += 10
        else:
            reasoning_parts.append(f"High P/B of {pb:.1f}")
        
        # Current ratio
        if current_ratio and current_ratio > 2.0:
            score += 20
            reasoning_parts.append("Strong liquidity")
        elif current_ratio and current_ratio > 1.0:
            score += 10
        
        # Margin of safety concept
        if score >= 60:
            signal = "bullish"
        elif score >= 30:
            signal = "neutral"
        else:
            signal = "bearish"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=score,
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "High valuation",
            key_metrics={"pe_ratio": pe, "pb_ratio": pb, "current_ratio": current_ratio}
        )

class TechnicalAnalyst(InvestmentAgent):
    """Technical analysis based on price action"""
    
    def __init__(self):
        super().__init__(
            "Technical Analyst",
            "Price action, trends, and momentum indicators."
        )
    
    def analyze(self, data: Dict) -> AgentSignal:
        score = 50  # Start neutral
        reasoning_parts = []
        
        price = data.get("current_price", 0)
        avg50 = data.get("avg_50", 0)
        avg200 = data.get("avg_200", 0)
        rsi = data.get("rsi", 50)
        
        # Trend analysis
        if price and avg50 and price > avg50:
            score += 15
            reasoning_parts.append("Price above 50-day MA")
        elif price and avg50:
            score -= 10
        
        if price and avg200 and price > avg200:
            score += 15
            reasoning_parts.append("Price above 200-day MA")
        elif price and avg200:
            score -= 15
        
        # Golden cross / Death cross
        if avg50 and avg200 and avg50 > avg200:
            score += 10
            reasoning_parts.append("Golden cross pattern")
        elif avg50 and avg200:
            score -= 10
        
        # RSI analysis
        if rsi and rsi < 30:
            score += 15
            reasoning_parts.append(f"Oversold (RSI {rsi:.1f})")
        elif rsi and rsi > 70:
            score -= 15
            reasoning_parts.append(f"Overbought (RSI {rsi:.1f})")
        elif rsi:
            reasoning_parts.append(f"RSI neutral at {rsi:.1f}")
        
        # Clamp score
        score = max(10, min(95, score))
        
        if score >= 65:
            signal = "bullish"
        elif score <= 35:
            signal = "bearish"
        else:
            signal = "neutral"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=score,
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "Mixed signals",
            key_metrics={"rsi": rsi, "price_vs_50ma": price > avg50 if price and avg50 else None}
        )

class RiskManager(InvestmentAgent):
    """Risk assessment and position sizing"""
    
    def __init__(self):
        super().__init__(
            "Risk Manager",
            "Risk metrics, volatility, and position sizing."
        )
    
    def analyze(self, data: Dict) -> AgentSignal:
        score = 50
        risks = []
        
        beta = data.get("beta", 1.0)
        pe = data.get("pe_ratio", 0)
        
        # Beta risk
        if beta and beta > 1.5:
            score -= 20
            risks.append(f"High beta ({beta:.1f})")
        elif beta and beta < 0.8:
            score += 10
            risks.append(f"Low beta ({beta:.1f})")
        else:
            risks.append(f"Market beta ({beta:.1f})")
        
        # Valuation risk
        if pe and pe > 40:
            score -= 20
            risks.append("Very high valuation")
        elif pe and pe > 25:
            score -= 10
            risks.append("Elevated valuation")
        
        # Sector concentration (mock check)
        sector = data.get("sector", "")
        if sector in ["Technology", "Biotechnology"]:
            risks.append(f"Volatile sector: {sector}")
        
        if score >= 60:
            signal = "bullish"
        elif score >= 40:
            signal = "neutral"
        else:
            signal = "bearish"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=abs(score - 50) + 50,
            reasoning=f"Risk factors: {', '.join(risks)}",
            key_metrics={"beta": beta, "risks": risks}
        )

class CathieWoodAgent(InvestmentAgent):
    """Cathie Wood growth/innovation analysis"""
    
    def __init__(self):
        super().__init__(
            "Cathie Wood",
            "Disruptive innovation and exponential growth."
        )
    
    def analyze(self, data: Dict) -> AgentSignal:
        score = 50
        reasoning_parts = []
        
        sector = data.get("sector", "")
        pe = data.get("pe_ratio", 0)
        
        # Growth sectors
        growth_sectors = ["Technology", "Healthcare", "Communication Services"]
        if sector in growth_sectors:
            score += 20
            reasoning_parts.append(f"{sector} is innovation-friendly")
        
        # High P/E acceptable for growth
        if pe and pe > 30:
            score += 10
            reasoning_parts.append("Premium valuation acceptable for growth")
        elif pe and pe < 15:
            score -= 10
            reasoning_parts.append("Low P/E suggests mature/declining business")
        
        if score >= 65:
            signal = "bullish"
        elif score <= 35:
            signal = "bearish"
        else:
            signal = "neutral"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=score,
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "Neutral on innovation potential"
        )

class AIHedgeFund:
    """Main hedge fund orchestrator"""
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.agents = [
            WarrenBuffettAgent(),
            BenGrahamAgent(),
            TechnicalAnalyst(),
            RiskManager(),
            CathieWoodAgent(),
        ]
    
    def analyze(self, ticker: str, detailed: bool = False) -> ConsensusResult:
        """Run all agents and generate consensus"""
        
        # Fetch data once
        data = self.data_fetcher.get_stock_data(ticker)
        
        # Run all agents
        agent_signals = []
        for agent in self.agents:
            try:
                signal = agent.analyze(data)
                agent_signals.append(signal)
            except Exception as e:
                print(f"Agent {agent.name} failed: {e}", file=sys.stderr)
        
        # Calculate consensus
        bullish_count = sum(1 for s in agent_signals if s.signal == "bullish")
        bearish_count = sum(1 for s in agent_signals if s.signal == "bearish")
        neutral_count = sum(1 for s in agent_signals if s.signal == "neutral")
        total = len(agent_signals)
        
        # Weighted confidence calculation
        total_confidence = sum(s.confidence for s in agent_signals)
        avg_confidence = total_confidence / total if total > 0 else 50
        
        # Determine consensus signal
        if bullish_count > bearish_count and bullish_count > neutral_count:
            consensus_signal = "bullish"
            consensus_confidence = int(avg_confidence * (bullish_count / total))
        elif bearish_count > bullish_count and bearish_count > neutral_count:
            consensus_signal = "bearish"
            consensus_confidence = int(avg_confidence * (bearish_count / total))
        else:
            consensus_signal = "neutral"
            consensus_confidence = int(avg_confidence * 0.7)
        
        # Collect risks
        key_risks = []
        for signal in agent_signals:
            if signal.key_metrics and "risks" in signal.key_metrics:
                key_risks.extend(signal.key_metrics["risks"])
        if not key_risks:
            key_risks = ["Market volatility", "Sector risks"]
        
        # Position sizing recommendation
        if consensus_signal == "bullish" and consensus_confidence > 70:
            recommendation = "Consider 5-10% position size"
        elif consensus_signal == "bullish":
            recommendation = "Consider 3-5% position size"
        elif consensus_signal == "neutral":
            recommendation = "Watchlist candidate, no position"
        else:
            recommendation = "Avoid or reduce position"
        
        return ConsensusResult(
            ticker=ticker,
            signal=consensus_signal,
            confidence=consensus_confidence,
            agreement=f"{bullish_count}/{total} bullish, {bearish_count}/{total} bearish",
            agent_signals=agent_signals,
            key_risks=key_risks[:5],  # Top 5 risks
            recommendation=recommendation,
            analysis_date=datetime.now().isoformat()
        )
    
    def analyze_multiple(self, tickers: List[str]) -> List[ConsensusResult]:
        """Analyze multiple stocks"""
        results = []
        for ticker in tickers:
            result = self.analyze(ticker)
            results.append(result)
        return results

def format_output(result: ConsensusResult, detailed: bool = False) -> str:
    """Format analysis result for display"""
    lines = []
    
    # Header
    signal_emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}[result.signal]
    lines.append(f"\n{'='*60}")
    lines.append(f"{signal_emoji} {result.ticker} Analysis - {result.signal.upper()} ({result.confidence}% confidence)")
    lines.append(f"{'='*60}")
    lines.append(f"Agreement: {result.agreement}")
    lines.append(f"Date: {result.analysis_date[:10]}")
    lines.append("")
    
    # Agent details
    if detailed:
        lines.append("📊 Agent Analysis:")
        lines.append("-" * 40)
        for signal in result.agent_signals:
            emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}[signal.signal]
            lines.append(f"{emoji} {signal.agent_name}: {signal.signal} ({signal.confidence}%)")
            lines.append(f"   Reason: {signal.reasoning}")
            lines.append("")
    else:
        lines.append("📊 Agent Signals:")
        for signal in result.agent_signals:
            emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}[signal.signal]
            lines.append(f"  {emoji} {signal.agent_name}: {signal.signal} ({signal.confidence}%)")
        lines.append("")
    
    # Risks
    lines.append("⚠️  Key Risks:")
    for risk in result.key_risks:
        lines.append(f"  • {risk}")
    lines.append("")
    
    # Recommendation
    lines.append(f"💡 Recommendation: {result.recommendation}")
    lines.append(f"{'='*60}\n")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="AI Hedge Fund Stock Analysis")
    parser.add_argument("ticker", help="Stock ticker symbol(s), comma-separated for multiple")
    parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed agent reasoning")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--compare", "-c", action="store_true", help="Compare multiple stocks")
    
    args = parser.parse_args()
    
    # Parse tickers
    tickers = [t.strip().upper() for t in args.ticker.split(",")]
    
    # Initialize hedge fund
    hedge_fund = AIHedgeFund()
    
    # Run analysis
    if len(tickers) == 1:
        result = hedge_fund.analyze(tickers[0], detailed=args.detailed)
        
        if args.json:
            # Convert to dict for JSON serialization
            result_dict = {
                "ticker": result.ticker,
                "signal": result.signal,
                "confidence": result.confidence,
                "agreement": result.agreement,
                "key_risks": result.key_risks,
                "recommendation": result.recommendation,
                "analysis_date": result.analysis_date,
                "agents": [
                    {
                        "name": s.agent_name,
                        "signal": s.signal,
                        "confidence": s.confidence,
                        "reasoning": s.reasoning
                    }
                    for s in result.agent_signals
                ]
            }
            print(json.dumps(result_dict, indent=2))
        else:
            print(format_output(result, detailed=args.detailed))
    else:
        # Multiple tickers
        results = hedge_fund.analyze_multiple(tickers)
        
        if args.compare:
            # Comparison table
            print("\n" + "="*80)
            print(f"{'Ticker':<10} {'Signal':<10} {'Confidence':<12} {'Bullish':<10} {'Recommendation'}")
            print("="*80)
            for r in results:
                bullish = int(r.agreement.split("/")[0])
                print(f"{r.ticker:<10} {r.signal.upper():<10} {r.confidence}%{'':<6} {bullish} agents{'':<3} {r.recommendation[:30]}")
            print("="*80 + "\n")
        else:
            for result in results:
                print(format_output(result, detailed=args.detailed))

if __name__ == "__main__":
    main()
