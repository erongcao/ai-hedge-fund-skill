#!/usr/bin/env python3
"""
AI Hedge Fund Skill - v3.0 Enhanced with Perspective Skills
Features:
- Multi-master roundtable (Buffett, Graham, Munger)
- Ensemble mode with consensus/divergence detection
- Feedback-driven weight optimization
- Integrated OKX technical analysis
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Literal, Optional, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum

# Import base classes
from base import AgentSignal, ConsensusResult, InvestmentAgent

# Import enhanced modules
from data_enhancement import EnhancedDataFetcher, EnhancedStockData
from enhanced_agents import EarningsAgent, AnalystConsensusAgent, MacroAgent, DividendAgent, FinancialHealthAgent
from smart_data_fetcher import SmartDataFetcher, StockData

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


class MasterInvestor(Enum):
    """Enum for master investors"""
    BUFFETT = "warren-buffett-perspective"
    GRAHAM = "ben-graham-perspective"
    MUNGER = "charlie-munger-perspective"
    LYNCH = "peter-lynch-perspective"
    BURRY = "michael-burry-perspective"


@dataclass
class MasterAnalysis:
    """Analysis from a master investor perspective"""
    master: str
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int
    reasoning: str
    key_principles: List[str]
    concerns: List[str]
    would_buy: bool
    position_size: str  # "large", "medium", "small", "none"


@dataclass
class RoundtableResult:
    """Result from roundtable discussion"""
    ticker: str
    master_analyses: List[MasterAnalysis]
    consensus_points: List[str]
    divergence_points: List[Dict]
    overall_signal: str
    overall_confidence: int
    synthesis: str
    recommendation: str


class MasterPerspectiveAgent:
    """Agent that uses perspective skill for analysis"""

    def __init__(self, master: MasterInvestor):
        self.master = master
        self.name = master.name.title().replace("_", " ")
        self.skill_path = f"~/.openclaw/skills/{master.value}/SKILL.md"

    def analyze(self, ticker: str, data: Dict) -> MasterAnalysis:
        """
        Simulate master investor analysis based on their principles
        In production, this would invoke the actual perspective skill
        """
        # Map master to analysis function
        analyzers = {
            MasterInvestor.BUFFETT: self._buffett_analysis,
            MasterInvestor.GRAHAM: self._graham_analysis,
            MasterInvestor.MUNGER: self._munger_analysis,
            MasterInvestor.LYNCH: self._lynch_analysis,
            MasterInvestor.BURRY: self._burry_analysis,
        }

        analyzer = analyzers.get(self.master, self._default_analysis)
        return analyzer(ticker, data)

    def _buffett_analysis(self, ticker: str, data: Dict) -> MasterAnalysis:
        """Warren Buffett style analysis"""
        score = 50
        principles = []
        concerns = []

        # Economic moat analysis
        roe = data.get("roe", 0)
        margin = data.get("operating_margin", 0)
        if roe > 0.15 and margin > 0.15:
            score += 20
            principles.append("Strong economic moat (high ROE + margins)")
        else:
            concerns.append("Unclear competitive advantage")

        # Circle of competence - prefer simple businesses
        sector = data.get("sector", "")
        if sector in ["Technology", "Financials"]:
            score -= 10
            concerns.append("Outside typical circle of competence")

        # Conservative debt
        debt = data.get("debt_to_equity", 0)
        if debt < 0.3:
            score += 15
            principles.append("Conservative balance sheet")
        elif debt > 1.0:
            score -= 15
            concerns.append("Too much leverage")

        # Reasonable price
        pe = data.get("pe_ratio", 0)
        if pe < 20:
            score += 15
            principles.append("Reasonable valuation")
        elif pe > 40:
            score -= 10
            concerns.append("Price may be too high")

        # Long-term hold quality
        market_cap = data.get("market_cap", 0)
        if market_cap > 50e9:
            score += 10
            principles.append("Large, stable business")

        signal = "bullish" if score >= 65 else "bearish" if score <= 35 else "neutral"

        return MasterAnalysis(
            master="Warren Buffett",
            signal=signal,
            confidence=min(95, max(10, score)),
            reasoning=f"{'; '.join(principles)} | Concerns: {'; '.join(concerns) if concerns else 'None'}",
            key_principles=principles,
            concerns=concerns,
            would_buy=score >= 60,
            position_size="large" if score >= 75 else "medium" if score >= 60 else "small" if score >= 45 else "none"
        )

    def _graham_analysis(self, ticker: str, data: Dict) -> MasterAnalysis:
        """Ben Graham style analysis"""
        score = 50
        principles = []
        concerns = []

        # Margin of safety - P/E
        pe = data.get("pe_ratio", 0)
        if pe < 15:
            score += 25
            principles.append(f"Attractive P/E: {pe:.1f}")
        elif pe < 25:
            score += 10
        else:
            concerns.append(f"High P/E: {pe:.1f}")

        # P/B ratio
        pb = data.get("pb_ratio", 0)
        if pb < 1.5:
            score += 20
            principles.append(f"Good P/B: {pb:.1f}")
        elif pb > 3:
            concerns.append(f"High P/B: {pb:.1f}")

        # Current ratio
        current_ratio = data.get("current_ratio", 0)
        if current_ratio > 2.0:
            score += 15
            principles.append("Strong liquidity (current ratio > 2)")
        elif current_ratio < 1.0:
            concerns.append("Liquidity concerns")

        # Net current asset value check
        if pe < 15 and pb < 1.5 and current_ratio > 1.5:
            score += 15
            principles.append("Net-net characteristics")

        signal = "bullish" if score >= 65 else "bearish" if score <= 35 else "neutral"

        return MasterAnalysis(
            master="Ben Graham",
            signal=signal,
            confidence=min(95, max(10, score)),
            reasoning=f"{'; '.join(principles)} | Concerns: {'; '.join(concerns) if concerns else 'None'}",
            key_principles=principles,
            concerns=concerns,
            would_buy=score >= 65,
            position_size="medium" if score >= 65 else "small" if score >= 50 else "none"
        )

    def _munger_analysis(self, ticker: str, data: Dict) -> MasterAnalysis:
        """Charlie Munger style analysis"""
        score = 50
        principles = []
        concerns = []
        mental_models = []

        # Multi-disciplinary: Check multiple factors
        checks_passed = 0
        checks_total = 0

        # ROE (quality check)
        roe = data.get("roe", 0)
        checks_total += 1
        if roe > 0.12:
            checks_passed += 1
            principles.append("Good returns on equity")

        # Consistency (low beta)
        beta = data.get("beta", 1.0)
        checks_total += 1
        if beta < 1.2:
            checks_passed += 1
            principles.append("Lower volatility than market")
        else:
            concerns.append("High beta - more volatile")
            mental_models.append("Invert: What could go wrong with high volatility?")

        # Competitive advantage (margins)
        margin = data.get("operating_margin", 0)
        checks_total += 1
        if margin > 0.10:
            checks_passed += 1
            principles.append("Sustainable margins")

        # Avoid commoditized businesses
        sector = data.get("sector", "")
        if sector in ["Utilities", "Materials"]:
            score -= 10
            concerns.append("Commodity-like business")
            mental_models.append("Circle of competence: Hard to differentiate")

        # Calculate score based on latticework of models
        score += (checks_passed / checks_total) * 40

        # Psychological check: Is it a quality business you'd hold forever?
        if score >= 60:
            principles.append("Lollapalooza effect: Multiple good factors align")

        signal = "bullish" if score >= 65 else "bearish" if score <= 35 else "neutral"

        return MasterAnalysis(
            master="Charlie Munger",
            signal=signal,
            confidence=min(95, max(10, score)),
            reasoning=f"{'; '.join(principles)} | Mental models: {'; '.join(mental_models) if mental_models else 'None'}",
            key_principles=principles + mental_models,
            concerns=concerns,
            would_buy=score >= 60,
            position_size="large" if score >= 75 else "medium" if score >= 60 else "none"
        )

    def _lynch_analysis(self, ticker: str, data: Dict) -> MasterAnalysis:
        """Peter Lynch style analysis - GARP and ten-bagger hunting"""
        score = 50
        principles = []
        concerns = []
        
        # GARP: Growth at Reasonable Price
        pe = data.get("pe_ratio", 0)
        revenue_growth = data.get("revenue_growth", 0)
        
        # PEG ratio calculation (simplified)
        growth_rate = max(1, abs(revenue_growth) * 100) if revenue_growth else 1
        peg = pe / growth_rate if growth_rate > 0 else 99
        
        if peg < 1.0:
            score += 25
            principles.append(f"PEG ratio {peg:.2f} < 1.0 (GARP)")
        elif peg < 1.5:
            score += 15
            principles.append(f"PEG ratio {peg:.2f} < 1.5")
        else:
            concerns.append(f"High PEG ratio: {peg:.2f}")
        
        # Growth rate
        if revenue_growth and revenue_growth > 0.15:
            score += 20
            principles.append(f"Strong revenue growth: {revenue_growth:.1%}")
        elif revenue_growth and revenue_growth > 0.10:
            score += 10
        else:
            concerns.append("Insufficient growth")
        
        # Check for value trap
        if pe < 10 and revenue_growth and revenue_growth < 0.05:
            score -= 15
            concerns.append("Low P/E with no growth (value trap?)")
        
        # Market cap preference (mid-cap has ten-bagger potential)
        market_cap = data.get("market_cap", 0)
        if market_cap and 5e9 < market_cap < 50e9:
            score += 15
            principles.append("Mid-cap with growth potential")
        elif market_cap and market_cap > 200e9:
            score -= 5
            concerns.append("Large cap - limited ten-bagger potential")
        
        # Profitability check
        profit_margin = data.get("profit_margin", 0)
        if profit_margin and profit_margin > 0.05:
            score += 10
            principles.append("Profitable business")
        elif profit_margin and profit_margin < 0:
            score -= 20
            concerns.append("Unprofitable")
        
        signal = "bullish" if score >= 65 else "bearish" if score <= 35 else "neutral"
        
        return MasterAnalysis(
            master="Peter Lynch",
            signal=signal,
            confidence=min(95, max(10, score)),
            reasoning=f"{'; '.join(principles)} | Concerns: {'; '.join(concerns) if concerns else 'None'}",
            key_principles=principles,
            concerns=concerns,
            would_buy=score >= 60,
            position_size="large" if score >= 75 else "medium" if score >= 60 else "small"
        )

    def _burry_analysis(self, ticker: str, data: Dict) -> MasterAnalysis:
        """Michael Burry style analysis - Deep value and catalyst hunting"""
        score = 50
        principles = []
        concerns = []
        
        # Deep value: Price vs intrinsic value
        pe = data.get("pe_ratio", 0)
        pb = data.get("pb_ratio", 0)
        ps = data.get("price_to_sales", 0)
        
        # NCAV-like check (simplified)
        current_ratio = data.get("current_ratio", 0)
        debt_to_equity = data.get("debt_to_equity", 0)
        cash = data.get("cash", 0)
        market_cap = data.get("market_cap", 0)
        
        # Deep value score
        value_factors = 0
        if pe < 10:
            value_factors += 1
            principles.append(f"P/E {pe:.1f} indicates deep value")
        if pb < 1.0:
            value_factors += 1
            principles.append(f"P/B {pb:.1f} < 1.0")
        if current_ratio and current_ratio > 1.5:
            value_factors += 1
            principles.append("Good liquidity position")
        if debt_to_equity and debt_to_equity < 0.5:
            value_factors += 1
            principles.append("Conservative leverage")
        
        if value_factors >= 3:
            score += 30
        elif value_factors >= 2:
            score += 15
        
        # Cash check (catalyst potential)
        if cash and market_cap and cash / market_cap > 0.2:
            score += 10
            principles.append("Cash-rich balance sheet")
        
        # Risk factors (value trap detection)
        if revenue_growth := data.get("revenue_growth", 0):
            if revenue_growth < -0.10:
                score -= 25
                concerns.append("Declining revenue (potential value trap)")
        
        # High short interest (contrarian signal)
        # This would need actual short interest data
        if pe < 5:
            principles.append("Extremely low P/E - market may be wrong")
        
        signal = "bullish" if score >= 60 else "bearish" if score <= 40 else "neutral"
        
        return MasterAnalysis(
            master="Michael Burry",
            signal=signal,
            confidence=min(95, max(10, score)),
            reasoning=f"{'; '.join(principles)} | Concerns: {'; '.join(concerns) if concerns else 'None'}",
            key_principles=principles,
            concerns=concerns,
            would_buy=score >= 60,
            position_size="large" if score >= 70 else "medium" if score >= 55 else "none"
        )

    def _default_analysis(self, ticker: str, data: Dict) -> MasterAnalysis:
        return MasterAnalysis(
            master=self.name,
            signal="neutral",
            confidence=50,
            reasoning="Default analysis",
            key_principles=[],
            concerns=["Unknown master"],
            would_buy=False,
            position_size="none"
        )


class RoundtableEnsemble:
    """
    Ensemble mode for master investor roundtable
    Implements consensus and divergence detection
    """

    def __init__(self):
        self.masters = [
            MasterPerspectiveAgent(MasterInvestor.BUFFETT),
            MasterPerspectiveAgent(MasterInvestor.GRAHAM),
            MasterPerspectiveAgent(MasterInvestor.MUNGER),
            MasterPerspectiveAgent(MasterInvestor.LYNCH),
            MasterPerspectiveAgent(MasterInvestor.BURRY),
        ]

    def analyze(self, ticker: str, data: Dict) -> RoundtableResult:
        """Run roundtable analysis with all masters"""

        # Get analysis from each master
        analyses = []
        for master_agent in self.masters:
            try:
                analysis = master_agent.analyze(ticker, data)
                analyses.append(analysis)
            except Exception as e:
                print(f"Master {master_agent.name} analysis failed: {e}", file=sys.stderr)

        # Find consensus points
        consensus = self._find_consensus(analyses)

        # Find divergence points
        divergence = self._find_divergence(analyses)

        # Calculate overall signal
        bullish_count = sum(1 for a in analyses if a.signal == "bullish")
        bearish_count = sum(1 for a in analyses if a.signal == "bearish")
        neutral_count = sum(1 for a in analyses if a.signal == "neutral")

        if bullish_count > bearish_count:
            overall_signal = "bullish"
            overall_confidence = int(sum(a.confidence for a in analyses if a.signal == "bullish") / bullish_count) if bullish_count > 0 else 50
        elif bearish_count > bullish_count:
            overall_signal = "bearish"
            overall_confidence = int(sum(a.confidence for a in analyses if a.signal == "bearish") / bearish_count) if bearish_count > 0 else 50
        else:
            overall_signal = "neutral"
            overall_confidence = 50

        # Generate synthesis
        synthesis = self._generate_synthesis(analyses, consensus, divergence)

        # Generate recommendation
        recommendation = self._generate_recommendation(analyses, overall_signal)

        return RoundtableResult(
            ticker=ticker,
            master_analyses=analyses,
            consensus_points=consensus,
            divergence_points=divergence,
            overall_signal=overall_signal,
            overall_confidence=overall_confidence,
            synthesis=synthesis,
            recommendation=recommendation
        )

    def _find_consensus(self, analyses: List[MasterAnalysis]) -> List[str]:
        """Find points of consensus among masters"""
        consensus = []

        # Check for shared principles
        all_principles = [set(a.key_principles) for a in analyses]
        if all_principles:
            shared = all_principles[0].intersection(*all_principles[1:])
            consensus.extend(list(shared)[:3])  # Top 3 shared principles

        # Check for shared signal direction
        signals = [a.signal for a in analyses]
        if signals.count("bullish") >= 2:
            consensus.append("Multiple masters bullish")
        elif signals.count("bearish") >= 2:
            consensus.append("Multiple masters bearish")

        # Check for shared concerns
        all_concerns = [set(a.concerns) for a in analyses]
        if all_concerns:
            shared_concerns = all_concerns[0].intersection(*all_concerns[1:])
            for concern in list(shared_concerns)[:2]:
                consensus.append(f"Shared concern: {concern}")

        return consensus

    def _find_divergence(self, analyses: List[MasterAnalysis]) -> List[Dict]:
        """Find points of divergence among masters"""
        divergence = []

        # Signal divergence
        signals = {a.master: a.signal for a in analyses}
        if len(set(signals.values())) > 1:
            divergence.append({
                "type": "signal",
                "description": "Masters disagree on direction",
                "details": signals
            })

        # Position size divergence
        sizes = {a.master: a.position_size for a in analyses}
        if len(set(sizes.values())) > 1:
            divergence.append({
                "type": "position_size",
                "description": "Different position sizing recommendations",
                "details": sizes
            })

        # Buy/no-buy divergence
        would_buy = {a.master: a.would_buy for a in analyses}
        if len(set(would_buy.values())) > 1:
            divergence.append({
                "type": "buy_decision",
                "description": "Masters split on whether to buy",
                "details": would_buy
            })

        return divergence

    def _generate_synthesis(self, analyses: List[MasterAnalysis],
                           consensus: List[str],
                           divergence: List[Dict]) -> str:
        """Generate synthesis of roundtable discussion"""
        synthesis = []

        synthesis.append("## Master Investor Roundtable Synthesis\n")

        # Summary of each master
        synthesis.append("### Individual Perspectives\n")
        for a in analyses:
            emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}[a.signal]
            synthesis.append(f"{emoji} **{a.master}**: {a.signal.upper()} ({a.confidence}%) - {a.reasoning[:100]}...")

        synthesis.append("")

        # Consensus
        if consensus:
            synthesis.append("### ✅ Points of Consensus\n")
            for point in consensus:
                synthesis.append(f"- {point}")
            synthesis.append("")

        # Divergence
        if divergence:
            synthesis.append("### ⚡ Points of Divergence\n")
            for div in divergence:
                synthesis.append(f"- **{div['description']}**")
                for master, value in div['details'].items():
                    synthesis.append(f"  - {master}: {value}")
            synthesis.append("")

        return "\n".join(synthesis)

    def _generate_recommendation(self, analyses: List[MasterAnalysis],
                                 overall_signal: str) -> str:
        """Generate final recommendation"""

        # Count would_buy
        would_buy_count = sum(1 for a in analyses if a.would_buy)

        # Get position sizes
        large_positions = sum(1 for a in analyses if a.position_size == "large")
        medium_positions = sum(1 for a in analyses if a.position_size == "medium")

        if overall_signal == "bullish":
            if would_buy_count >= 2 and large_positions >= 1:
                return "Strong Buy: Consider 5-10% position"
            elif would_buy_count >= 2:
                return "Buy: Consider 3-5% position"
            else:
                return "Cautious Buy: Consider 2-3% position with tight stops"
        elif overall_signal == "bearish":
            return "Avoid: Multiple masters express concerns"
        else:
            if would_buy_count == 0:
                return "Neutral/Skip: No strong conviction from any master"
            else:
                return "Watchlist: Wait for better entry or clearer signal"


class AIFundV3:
    """v3.0 AI Hedge Fund with master perspectives and ensemble"""

    def __init__(self, use_roundtable: bool = True):
        self.data_fetcher = SmartDataFetcher()
        self.use_roundtable = use_roundtable

        if use_roundtable:
            self.roundtable = RoundtableEnsemble()

        # Classic agents for additional analysis
        self.classic_agents = [
            # These would be from the original ai_hedge_fund.py
        ]

    def analyze(self, ticker: str, include_roundtable: bool = True) -> Dict:
        """Full analysis with master roundtable"""

        # Fetch data
        data = self.data_fetcher.fetch(ticker)

        result = {
            "ticker": ticker,
            "price": data.current_price,
            "data_source": data.data_source,
            "analysis": {}
        }

        # Master roundtable analysis
        if include_roundtable and self.use_roundtable:
            data_dict = data.to_dict()
            roundtable_result = self.roundtable.analyze(ticker, data_dict)
            result["roundtable"] = {
                "overall_signal": roundtable_result.overall_signal,
                "overall_confidence": roundtable_result.overall_confidence,
                "consensus_points": roundtable_result.consensus_points,
                "divergence_points": roundtable_result.divergence_points,
                "synthesis": roundtable_result.synthesis,
                "recommendation": roundtable_result.recommendation,
                "master_analyses": [
                    {
                        "master": a.master,
                        "signal": a.signal,
                        "confidence": a.confidence,
                        "would_buy": a.would_buy,
                        "position_size": a.position_size
                    }
                    for a in roundtable_result.master_analyses
                ]
            }

        return result


def format_roundtable_output(result: Dict) -> str:
    """Format roundtable result for display"""
    lines = []

    ticker = result["ticker"]
    price = result["price"]

    lines.append(f"\n{'='*70}")
    lines.append(f"🎯 {ticker} - Master Investor Roundtable Analysis")
    lines.append(f"{'='*70}")
    lines.append(f"Current Price: ${price:.2f}" if price else "Price: N/A")
    lines.append("")

    if "roundtable" in result:
        rt = result["roundtable"]

        # Overall signal
        signal = rt["overall_signal"]
        confidence = rt["overall_confidence"]
        emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}[signal]
        lines.append(f"{emoji} OVERALL: {signal.upper()} ({confidence}% confidence)")
        lines.append("")

        # Individual masters
        lines.append("📊 Master Perspectives:")
        lines.append("-" * 40)
        for a in rt["master_analyses"]:
            emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}[a["signal"]]
            buy_emoji = "✅" if a["would_buy"] else "❌"
            lines.append(f"{emoji} {a['master']}: {a['signal'].upper()} ({a['confidence']}%)")
            lines.append(f"   {buy_emoji} Would buy: {a['would_buy']} | Position: {a['position_size']}")
        lines.append("")

        # Consensus
        if rt["consensus_points"]:
            lines.append("✅ Consensus Points:")
            for point in rt["consensus_points"]:
                lines.append(f"  • {point}")
            lines.append("")

        # Divergence
        if rt["divergence_points"]:
            lines.append("⚡ Divergence Points:")
            for div in rt["divergence_points"]:
                lines.append(f"  • {div['description']}")
            lines.append("")

        # Recommendation
        lines.append(f"💡 RECOMMENDATION: {rt['recommendation']}")
        lines.append("")

        # Synthesis (truncated)
        lines.append("📝 SYNTHESIS:")
        synthesis_lines = rt["synthesis"].split("\n")[:15]  # First 15 lines
        lines.extend(synthesis_lines)
        if len(rt["synthesis"].split("\n")) > 15:
            lines.append("... [truncated]")

    lines.append(f"{'='*70}\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI Hedge Fund v3.0 - Master Investor Roundtable")
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--classic", action="store_true", help="Use classic agent mode only")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--masters", nargs="+", choices=["buffett", "graham", "munger", "lynch", "burry"],
                       help="Select specific masters for analysis")

    args = parser.parse_args()

    # Initialize fund
    fund = AIFundV3(use_roundtable=not args.classic)

    # Run analysis
    result = fund.analyze(args.ticker.upper(), include_roundtable=not args.classic)

    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_roundtable_output(result))


if __name__ == "__main__":
    main()
