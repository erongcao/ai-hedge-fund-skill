#!/usr/bin/env python3
"""
AI Hedge Fund Skill - Enhanced Edition v2.1
Integrates features from stock-analysis skill:
- Earnings surprise analysis
- Analyst consensus
- Macro environment
- Dividend analysis
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Literal, Optional
from dataclasses import dataclass, asdict

# Import base classes
from base import AgentSignal, ConsensusResult, InvestmentAgent

# Import enhanced modules
from data_enhancement import EnhancedDataFetcher, EnhancedStockData
from enhanced_agents import EarningsAgent, AnalystConsensusAgent, MacroAgent, DividendAgent, FinancialHealthAgent

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
        elif pe:
            reasoning_parts.append(f"High P/E of {pe:.1f}")
        else:
            reasoning_parts.append("P/E data not available")
        
        # Market cap (Buffett prefers large caps)
        market_cap = data.get("market_cap", 0)
        if market_cap and market_cap > 100e9:
            score += 10
            reasoning_parts.append("Large cap - stable business")
        
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
            key_metrics={"roe": roe, "pe": pe, "debt": debt}
        )


class BenGrahamAgent(InvestmentAgent):
    """Ben Graham deep value analysis"""
    
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
        elif pe:
            reasoning_parts.append(f"High P/E of {pe:.1f}")
        else:
            reasoning_parts.append("P/E data not available")
        
        # P/B analysis
        if pb and pb < 1.5:
            score += 25
            reasoning_parts.append(f"Good P/B of {pb:.1f}")
        elif pb and pb < 3.0:
            score += 10
        elif pb:
            reasoning_parts.append(f"High P/B of {pb:.1f}")
        else:
            reasoning_parts.append("P/B data not available")
        
        # Current ratio
        if current_ratio and current_ratio > 2.0:
            score += 20
            reasoning_parts.append("Strong liquidity")
        elif current_ratio and current_ratio > 1.0:
            score += 10
        
        # Margin of safety concept
        if score >= 60:
            reasoning_parts.append("Good margin of safety")
        
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
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "No clear value signal",
            key_metrics={"pe": pe, "pb": pb, "current_ratio": current_ratio}
        )


class TechnicalAnalyst(InvestmentAgent):
    """Technical analysis using price action"""
    
    def __init__(self):
        super().__init__(
            "Technical Analyst",
            "Price action, trends, support/resistance, momentum."
        )
    
    def analyze(self, data: Dict) -> AgentSignal:
        score = 50
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
        else:
            reasoning_parts.append("RSI data not available")
        
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
        elif beta:
            risks.append(f"Market beta ({beta:.1f})")
        else:
            risks.append("Beta data not available")
        
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
        growth_sectors = ["Technology", "Healthcare", "Biotechnology", "Communications"]
        
        # Sector preference
        if sector in growth_sectors:
            score += 20
            reasoning_parts.append(f"Growth sector: {sector}")
        else:
            score -= 15
            reasoning_parts.append(f"Traditional sector: {sector}")
        
        # High valuation tolerance (for growth)
        pe = data.get("pe_ratio", 0)
        if pe and pe > 50:
            score += 10
            reasoning_parts.append("High P/E acceptable for growth")
        elif pe and pe < 20:
            score -= 10
            reasoning_parts.append("Low P/E suggests limited growth")
        
        # Innovation indicators
        market_cap = data.get("market_cap", 0)
        if market_cap and market_cap < 50e9:
            score += 15
            reasoning_parts.append("Mid-cap with growth potential")
        
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
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "Neutral on growth potential",
            key_metrics={"sector": sector, "growth_potential": score > 60}
        )


class EnhancedAIHedgeFund:
    """Enhanced AI Hedge Fund with additional agents"""
    
    def __init__(self):
        self.data_fetcher = EnhancedDataFetcher()
        
        # Classic agents
        self.classic_agents: List[InvestmentAgent] = [
            WarrenBuffettAgent(),
            BenGrahamAgent(),
            TechnicalAnalyst(),
            RiskManager(),
            CathieWoodAgent(),
        ]
        
        # Enhanced agents (from stock-analysis)
        self.enhanced_agents = [
            EarningsAgent(),
            AnalystConsensusAgent(),
            MacroAgent(),
            DividendAgent(),
            FinancialHealthAgent(),  # NEW: Financial health analysis
        ]
    
    def analyze(self, ticker: str, detailed: bool = False) -> ConsensusResult:
        """Run all agents and generate consensus"""
        
        # Fetch enhanced data
        enhanced_data = self.data_fetcher.get_enhanced_data(ticker)
        
        # Convert to dict for classic agents
        data_dict = {
            "current_price": enhanced_data.current_price,
            "pe_ratio": enhanced_data.pe_ratio,
            "pb_ratio": enhanced_data.pb_ratio,
            "beta": enhanced_data.beta,
            "roe": enhanced_data.roe,
            "debt_to_equity": enhanced_data.debt_to_equity,
            "operating_margin": enhanced_data.operating_margin,
            "current_ratio": enhanced_data.current_ratio,
            "sector": enhanced_data.sector,
            "market_cap": enhanced_data.market_cap,
            "avg_50": enhanced_data.avg_50,
            "avg_200": enhanced_data.avg_200,
            "rsi": enhanced_data.rsi,
        }
        
        # Run all agents
        agent_signals = []
        
        # Classic agents
        for agent in self.classic_agents:
            try:
                signal = agent.analyze(data_dict)
                agent_signals.append(signal)
            except Exception as e:
                print(f"Classic agent {agent.name} failed: {e}", file=sys.stderr)
        
        # Enhanced agents
        for agent in self.enhanced_agents:
            try:
                signal = agent.analyze_enhanced(enhanced_data)
                agent_signals.append(signal)
            except Exception as e:
                print(f"Enhanced agent {agent.name} failed: {e}", file=sys.stderr)
        
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
        
        # Build enhanced data dict for output
        enhanced_data_dict = {
            "earnings": {
                "actual_eps": enhanced_data.earnings.actual_eps,
                "expected_eps": enhanced_data.earnings.expected_eps,
                "surprise_pct": enhanced_data.earnings.surprise_pct,
                "beats_last_4q": enhanced_data.earnings.beats_last_4q,
            },
            "analyst": {
                "consensus": enhanced_data.analyst.consensus_rating,
                "num_analysts": enhanced_data.analyst.num_analysts,
                "price_target": enhanced_data.analyst.price_target,
                "upside_pct": enhanced_data.analyst.upside_pct,
            },
            "dividend": {
                "yield_pct": enhanced_data.dividend.yield_pct,
                "payout_ratio": enhanced_data.dividend.payout_ratio,
                "payout_status": enhanced_data.dividend.payout_status,
                "income_rating": enhanced_data.dividend.income_rating,
            },
            "macro": {
                "vix": enhanced_data.macro.vix_level,
                "vix_status": enhanced_data.macro.vix_status,
                "market_regime": enhanced_data.macro.market_regime,
                "spy_trend_10d": enhanced_data.macro.spy_trend_10d,
            },
            "financials": {
                "operating_margin": enhanced_data.financials.operating_margin,
                "gross_margin": enhanced_data.financials.gross_margin,
                "debt_to_equity": enhanced_data.financials.debt_to_equity,
                "return_on_equity": enhanced_data.financials.return_on_equity,
                "free_cash_flow": enhanced_data.financials.free_cash_flow,
                "revenue_growth_yoy": enhanced_data.financials.revenue_growth_yoy,
                "financial_health_score": enhanced_data.financials.financial_health_score,
            },
        }
        
        return ConsensusResult(
            ticker=ticker,
            signal=consensus_signal,
            confidence=consensus_confidence,
            agreement=f"{bullish_count}/{total} bullish, {bearish_count}/{total} bearish",
            agent_signals=agent_signals,
            key_risks=key_risks,
            recommendation=recommendation,
            analysis_date=datetime.now().isoformat(),
            enhanced_data=enhanced_data_dict
        )


def format_output(result: ConsensusResult, detailed: bool = False) -> str:
    """Format analysis result for display"""
    lines = []
    
    # Header
    signal_emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}[result.signal]
    lines.append(f"\n{'='*70}")
    lines.append(f"{signal_emoji} {result.ticker} Analysis - {result.signal.upper()} ({result.confidence}% confidence)")
    lines.append(f"{'='*70}")
    lines.append(f"Agreement: {result.agreement}")
    date_str = result.analysis_date[:10] if result.analysis_date else "N/A"
    lines.append(f"Date: {date_str}")
    lines.append("")
    
    # Enhanced Data Summary
    if result.enhanced_data:
        lines.append("📊 Enhanced Data Summary:")
        lines.append("-" * 40)
        
        # Earnings
        earnings = result.enhanced_data.get("earnings", {})
        if earnings.get("surprise_pct") is not None:
            surprise = earnings["surprise_pct"]
            emoji = "📈" if surprise > 0 else "📉"
            lines.append(f"  {emoji} Earnings Surprise: {surprise:+.1f}%")
        if earnings.get("beats_last_4q") is not None:
            lines.append(f"  📊 Beat Rate: {earnings['beats_last_4q']}/4 quarters")
        
        # Analyst
        analyst = result.enhanced_data.get("analyst", {})
        if analyst.get("num_analysts", 0) > 0:
            lines.append(f"  🎯 Analysts: {analyst['num_analysts']} | Consensus: {analyst.get('consensus', 'N/A')}")
        if analyst.get("upside_pct") is not None:
            upside = analyst["upside_pct"]
            emoji = "🚀" if upside > 10 else "📊" if upside > 0 else "⚠️"
            lines.append(f"  {emoji} Upside to Target: {upside:+.1f}%")
        
        # Dividend
        dividend = result.enhanced_data.get("dividend", {})
        if dividend.get("yield_pct") is not None and dividend.get("yield_pct") > 0:
            lines.append(f"  💰 Dividend: {dividend['yield_pct']:.2f}% ({dividend.get('income_rating', 'N/A')})")
        else:
            lines.append(f"  💰 Dividend: None (no dividend)")
        
        # Macro
        macro = result.enhanced_data.get("macro", {})
        if macro.get("vix"):
            vix_status = macro.get("vix_status", "unknown")
            emoji = {"calm": "😌", "elevated": "😐", "fear": "😰", "panic": "😱"}.get(vix_status, "❓")
            lines.append(f"  {emoji} VIX: {macro['vix']:.1f} ({vix_status})")
        if macro.get("market_regime"):
            lines.append(f"  📈 Market: {macro['market_regime'].upper()}")
        
        # Financial Metrics (NEW)
        financials = result.enhanced_data.get("financials", {})
        if financials:
            lines.append("")
            lines.append("  📈 Financial Health:")
            if financials.get("operating_margin") is not None:
                lines.append(f"    💵 Operating Margin: {financials['operating_margin']:.1f}%")
            if financials.get("debt_to_equity") is not None:
                debt_emoji = "✅" if financials['debt_to_equity'] < 0.5 else "⚠️" if financials['debt_to_equity'] < 1.0 else "❌"
                lines.append(f"    {debt_emoji} Debt/Equity: {financials['debt_to_equity']:.2f}x")
            if financials.get("return_on_equity") is not None:
                lines.append(f"    📊 ROE: {financials['return_on_equity']:.1f}%")
            if financials.get("free_cash_flow") is not None:
                fcf = financials['free_cash_flow']
                fcf_emoji = "✅" if fcf > 0 else "❌"
                lines.append(f"    {fcf_emoji} Free Cash Flow: ${fcf:.0f}M")
            if financials.get("financial_health_score"):
                score = financials['financial_health_score']
                score_emoji = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
                lines.append(f"    {score_emoji} Health Score: {score}/100")
        
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
    lines.append(f"{'='*70}\n")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI Hedge Fund Stock Analysis - Enhanced Edition")
    parser.add_argument("ticker", help="Stock ticker symbol(s), comma-separated for multiple")
    parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed agent reasoning")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--compare", "-c", action="store_true", help="Compare multiple stocks")
    parser.add_argument("--hot", action="store_true", help="Include trending stocks check")
    parser.add_argument("--rumor", action="store_true", help="Include rumor scanner for this ticker")
    
    args = parser.parse_args()
    
    # Parse tickers
    tickers = [t.strip().upper() for t in args.ticker.split(",")]
    
    # Initialize hedge fund
    hedge_fund = EnhancedAIHedgeFund()
    
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
                "recommendation": result.recommendation,
                "agent_signals": [
                    {
                        "agent": s.agent_name,
                        "signal": s.signal,
                        "confidence": s.confidence,
                        "reasoning": s.reasoning
                    }
                    for s in result.agent_signals
                ],
                "enhanced_data": result.enhanced_data,
            }
            print(json.dumps(result_dict, indent=2))
        else:
            print(format_output(result, detailed=args.detailed))
            
            # Optional: Hot scanner
            if args.hot:
                from hot_rumor_scanner import HotScanner, format_hot_scanner_results
                scanner = HotScanner()
                hot = scanner.get_hot_stocks()
                print(format_hot_scanner_results(hot))
            
            # Optional: Rumor scanner
            if args.rumor:
                from hot_rumor_scanner import RumorScanner, format_rumor_results
                scanner = RumorScanner()
                rumors = scanner.scan_for_ticker(tickers[0])
                if rumors:
                    print(format_rumor_results({tickers[0]: rumors}))
                else:
                    print(f"\n🔮 No rumors detected for {tickers[0]}\n")
    else:
        # Compare mode
        results = []
        for ticker in tickers:
            result = hedge_fund.analyze(ticker)
            results.append(result)
            print(format_output(result, detailed=False))
        
        # Summary comparison
        print("\n" + "="*70)
        print("📊 COMPARISON SUMMARY")
        print("="*70)
        for r in results:
            emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}[r.signal]
            print(f"{emoji} {r.ticker}: {r.signal.upper()} ({r.confidence}%) - {r.recommendation}")


if __name__ == "__main__":
    main()
