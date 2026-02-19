"""
Two-Tier AI Hedge Fund Architecture
Tier 1: Data Analysts (5 enhanced agents) - Research & Analysis
Tier 2: Investment Masters (5 classic agents) - Decision Making
"""

import sys
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from base import AgentSignal, InvestmentAgent
from data_enhancement import EnhancedStockData, EnhancedDataFetcher
from enhanced_agents import (
    EarningsAgent, AnalystConsensusAgent, MacroAgent, 
    DividendAgent, FinancialHealthAgent
)


@dataclass
class AnalystReport:
    """Comprehensive research report from Tier 1 analysts"""
    # Earnings Analysis
    earnings_signal: str = "neutral"
    earnings_confidence: int = 50
    eps_surprise: Optional[float] = None
    beat_rate: int = 0
    earnings_summary: str = ""
    
    # Analyst Consensus
    wall_street_signal: str = "neutral"
    wall_street_confidence: int = 50
    num_analysts: int = 0
    consensus_rating: str = "unknown"
    upside_potential: Optional[float] = None
    analyst_summary: str = ""
    
    # Macro Environment
    macro_signal: str = "neutral"
    macro_confidence: int = 50
    vix_level: Optional[float] = None
    market_regime: str = "unknown"
    macro_summary: str = ""
    
    # Dividend Analysis
    dividend_signal: str = "neutral"
    dividend_confidence: int = 50
    dividend_yield: Optional[float] = None
    payout_safety: str = "unknown"
    dividend_summary: str = ""
    
    # Financial Health
    health_signal: str = "neutral"
    health_confidence: int = 50
    health_score: int = 50
    operating_margin: Optional[float] = None
    debt_to_equity: Optional[float] = None
    roe: Optional[float] = None
    free_cash_flow: Optional[float] = None
    health_summary: str = ""
    
    # Overall Research Summary
    overall_bullish_count: int = 0
    overall_bearish_count: int = 0
    overall_neutral_count: int = 0
    key_findings: List[str] = field(default_factory=list)
    major_risks: List[str] = field(default_factory=list)


class DataAnalystTeam:
    """Tier 1: Research Team - 5 Enhanced Analysts"""
    
    def __init__(self):
        self.analysts = {
            'earnings': EarningsAgent(),
            'wall_street': AnalystConsensusAgent(),
            'macro': MacroAgent(),
            'dividend': DividendAgent(),
            'financial_health': FinancialHealthAgent()
        }
    
    def generate_research_report(self, data: EnhancedStockData) -> AnalystReport:
        """Generate comprehensive research report"""
        report = AnalystReport()
        
        # Run all analysts
        earnings_signal = self.analysts['earnings'].analyze_enhanced(data)
        wall_street_signal = self.analysts['wall_street'].analyze_enhanced(data)
        macro_signal = self.analysts['macro'].analyze_enhanced(data)
        dividend_signal = self.analysts['dividend'].analyze_enhanced(data)
        health_signal = self.analysts['financial_health'].analyze_enhanced(data)
        
        # Compile Earnings Analysis
        report.earnings_signal = earnings_signal.signal
        report.earnings_confidence = earnings_signal.confidence
        report.eps_surprise = data.earnings.surprise_pct
        report.beat_rate = data.earnings.beats_last_4q
        report.earnings_summary = earnings_signal.reasoning
        
        # Compile Wall Street Analysis
        report.wall_street_signal = wall_street_signal.signal
        report.wall_street_confidence = wall_street_signal.confidence
        report.num_analysts = data.analyst.num_analysts
        report.consensus_rating = data.analyst.consensus_rating
        report.upside_potential = data.analyst.upside_pct
        report.analyst_summary = wall_street_signal.reasoning
        
        # Compile Macro Analysis
        report.macro_signal = macro_signal.signal
        report.macro_confidence = macro_signal.confidence
        report.vix_level = data.macro.vix_level
        report.market_regime = data.macro.market_regime
        report.macro_summary = macro_signal.reasoning
        
        # Compile Dividend Analysis
        report.dividend_signal = dividend_signal.signal
        report.dividend_confidence = dividend_signal.confidence
        report.dividend_yield = data.dividend.yield_pct
        report.payout_safety = data.dividend.payout_status
        report.dividend_summary = dividend_signal.reasoning
        
        # Compile Financial Health
        report.health_signal = health_signal.signal
        report.health_confidence = health_signal.confidence
        report.health_score = data.financials.financial_health_score
        report.operating_margin = data.financials.operating_margin
        report.debt_to_equity = data.financials.debt_to_equity
        report.roe = data.financials.return_on_equity
        report.free_cash_flow = data.financials.free_cash_flow
        report.health_summary = health_signal.reasoning
        
        # Calculate overall sentiment
        signals = [earnings_signal, wall_street_signal, macro_signal, 
                   dividend_signal, health_signal]
        report.overall_bullish_count = sum(1 for s in signals if s.signal == "bullish")
        report.overall_bearish_count = sum(1 for s in signals if s.signal == "bearish")
        report.overall_neutral_count = sum(1 for s in signals if s.signal == "neutral")
        
        # Extract key findings
        report.key_findings = self._extract_key_findings(data, signals)
        report.major_risks = self._extract_major_risks(data, signals)
        
        return report
    
    def _extract_key_findings(self, data: EnhancedStockData, signals: List[AgentSignal]) -> List[str]:
        """Extract key positive findings"""
        findings = []
        
        # Earnings findings
        if data.earnings.surprise_pct and data.earnings.surprise_pct > 5:
            findings.append(f"Strong earnings beat: +{data.earnings.surprise_pct:.1f}%")
        if data.earnings.beats_last_4q >= 3:
            findings.append(f"Consistent earnings performer: {data.earnings.beats_last_4q}/4 beats")
        
        # Analyst findings
        if data.analyst.upside_pct and data.analyst.upside_pct > 20:
            findings.append(f"Significant upside potential: +{data.analyst.upside_pct:.1f}%")
        if data.analyst.consensus_rating in ['strong_buy', 'buy'] and data.analyst.num_analysts > 10:
            findings.append(f"Strong analyst support: {data.analyst.num_analysts} analysts, {data.analyst.consensus_rating}")
        
        # Financial health findings
        if data.financials.operating_margin and data.financials.operating_margin > 20:
            findings.append(f"Excellent margins: {data.financials.operating_margin:.1f}% operating margin")
        if data.financials.return_on_equity and data.financials.return_on_equity > 20:
            findings.append(f"High ROE: {data.financials.return_on_equity:.1f}%")
        if data.financials.free_cash_flow and data.financials.free_cash_flow > 1000:
            findings.append(f"Strong cash generation: ${data.financials.free_cash_flow:,.0f}M FCF")
        
        return findings[:5]  # Top 5 findings
    
    def _extract_major_risks(self, data: EnhancedStockData, signals: List[AgentSignal]) -> List[str]:
        """Extract major risks from all analysts"""
        risks = []
        
        for signal in signals:
            if signal.key_metrics and "risks" in signal.key_metrics:
                risks.extend(signal.key_metrics["risks"])
        
        # Add data-based risks
        if data.financials.debt_to_equity and data.financials.debt_to_equity > 1.5:
            risks.append(f"High debt burden (D/E {data.financials.debt_to_equity:.2f}x)")
        if data.beta and data.beta > 1.5:
            risks.append(f"High volatility (Beta {data.beta:.1f})")
        if data.earnings.surprise_pct and data.earnings.surprise_pct < -10:
            risks.append(f"Recent earnings miss ({data.earnings.surprise_pct:.1f}%)")
        
        return list(set(risks))[:5]  # Top 5 unique risks


class WarrenBuffettWithResearch(InvestmentAgent):
    """Warren Buffett with access to analyst research reports"""
    
    def __init__(self):
        super().__init__(
            "Warren Buffett (Research-Informed)",
            "Value investing informed by comprehensive analyst research."
        )
    
    def analyze_with_report(self, data: EnhancedStockData, report: AnalystReport) -> AgentSignal:
        """Analyze based on both raw data and analyst research"""
        score = 50
        reasoning_parts = []
        
        # Consider Financial Health Analyst findings
        if report.health_score >= 80:
            score += 20
            reasoning_parts.append(f"Excellent financial health ({report.health_score}/100)")
        elif report.health_score >= 60:
            score += 10
            reasoning_parts.append(f"Good financial health ({report.health_score}/100)")
        elif report.health_score < 40:
            score -= 20
            reasoning_parts.append(f"Poor financial health ({report.health_score}/100)")
        
        # Consider margins from research
        if report.operating_margin and report.operating_margin > 20:
            score += 15
            reasoning_parts.append(f"Wide moat indicated by {report.operating_margin:.1f}% margins")
        
        # Consider debt analysis
        if report.debt_to_equity and report.debt_to_equity < 0.5:
            score += 10
            reasoning_parts.append("Conservative debt levels")
        elif report.debt_to_equity and report.debt_to_equity > 1.5:
            score -= 15
            reasoning_parts.append(f"High debt concerns ({report.debt_to_equity:.2f}x)")
        
        # Consider ROE
        if report.roe and report.roe > 15:
            score += 15
            reasoning_parts.append(f"Strong ROE of {report.roe:.1f}%")
        
        # Consider Wall Street consensus (but with skepticism)
        if report.wall_street_signal == "bullish" and report.wall_street_confidence > 70:
            score += 5  # Small boost, Buffett is independent
            reasoning_parts.append("Analysts agree, but I do my own analysis")
        
        # Consider earnings quality
        if report.beat_rate >= 3:
            score += 10
            reasoning_parts.append(f"Reliable earnings: {report.beat_rate}/4 beats")
        
        # Consider macro (market timing not important for Buffett, but extremes matter)
        if report.market_regime == "bear" and report.vix_level and report.vix_level > 30:
            score += 10  # Opportunities in fear
            reasoning_parts.append("Market fear may create opportunity")
        
        # Clamp and determine signal
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
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "Awaiting clearer signals",
            key_metrics={
                "health_score": report.health_score,
                "operating_margin": report.operating_margin,
                "roe": report.roe,
                "debt_to_equity": report.debt_to_equity
            }
        )


class BenGrahamWithResearch(InvestmentAgent):
    """Ben Graham with access to analyst research"""
    
    def __init__(self):
        super().__init__(
            "Ben Graham (Research-Informed)",
            "Deep value investing with quantitative research support."
        )
    
    def analyze_with_report(self, data: EnhancedStockData, report: AnalystReport) -> AgentSignal:
        """Graham analysis informed by research"""
        score = 50
        reasoning_parts = []
        
        # Financial health is critical for Graham
        if report.health_score >= 70:
            score += 15
            reasoning_parts.append("Strong financial position")
        elif report.health_score < 40:
            score -= 25
            reasoning_parts.append("Financial instability - avoid")
        
        # Current ratio check
        if data.financials.current_ratio and data.financials.current_ratio > 2:
            score += 15
            reasoning_parts.append("Excellent liquidity (current ratio > 2)")
        elif data.financials.current_ratio and data.financials.current_ratio < 1:
            score -= 20
            reasoning_parts.append("Liquidity concerns")
        
        # Debt levels
        if report.debt_to_equity and report.debt_to_equity > 1.0:
            score -= 20
            reasoning_parts.append(f"Excessive leverage: {report.debt_to_equity:.2f}x")
        elif report.debt_to_equity and report.debt_to_equity < 0.3:
            score += 10
            reasoning_parts.append("Conservative capital structure")
        
        # Consistent earnings important for Graham
        if report.beat_rate >= 3:
            score += 10
            reasoning_parts.append("Predictable earnings history")
        elif report.beat_rate <= 1:
            score -= 10
            reasoning_parts.append("Erratic earnings")
        
        # Dividend safety (Graham liked dividends)
        if report.dividend_signal == "bullish":
            score += 10
            reasoning_parts.append("Reliable dividend income")
        
        # Margin of safety - analyst upside helps
        if report.upside_potential and report.upside_potential > 30:
            score += 10
            reasoning_parts.append(f"Potential margin of safety (+{report.upside_potential:.1f}% upside)")
        
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
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "No clear value opportunity",
            key_metrics={
                "health_score": report.health_score,
                "current_ratio": data.financials.current_ratio,
                "debt_to_equity": report.debt_to_equity
            }
        )


class TechnicalAnalystWithResearch(InvestmentAgent):
    """Technical Analyst with research context"""
    
    def __init__(self):
        super().__init__(
            "Technical Analyst (Research-Informed)",
            "Technical analysis combined with fundamental research insights."
        )
    
    def analyze_with_report(self, data: EnhancedStockData, report: AnalystReport) -> AgentSignal:
        """Technical analysis with fundamental confirmation"""
        score = 50
        reasoning_parts = []
        
        price = data.current_price
        avg50 = data.avg_50
        avg200 = data.avg_200
        
        # Trend analysis (original)
        if price and avg50 and price > avg50:
            score += 15
            reasoning_parts.append("Price above 50-day MA")
        
        if price and avg200 and price > avg200:
            score += 15
            reasoning_parts.append("Price above 200-day MA")
        
        # Golden cross
        if avg50 and avg200 and avg50 > avg200:
            score += 10
            reasoning_parts.append("Golden cross pattern")
        
        # Fundamental confirmation from research
        if report.wall_street_signal == "bullish":
            score += 10
            reasoning_parts.append("Wall Street bullish - fundamental support")
        
        if report.earnings_signal == "bullish":
            score += 15
            reasoning_parts.append("Strong earnings momentum")
        
        # Volume confirmation (if data available)
        if data.volume and data.avg_volume and data.volume > data.avg_volume * 1.5:
            score += 5
            reasoning_parts.append("Above-average volume")
        
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
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "Mixed technical signals",
            key_metrics={"price_vs_200ma": price > avg200 if price and avg200 else None}
        )


class RiskManagerWithResearch(InvestmentAgent):
    """Risk Manager with comprehensive research"""
    
    def __init__(self):
        super().__init__(
            "Risk Manager (Research-Informed)",
            "Risk assessment using all available research data."
        )
    
    def analyze_with_report(self, data: EnhancedStockData, report: AnalystReport) -> AgentSignal:
        """Comprehensive risk assessment"""
        score = 50
        risks = []
        
        # Financial health risk
        if report.health_score < 50:
            score -= 20
            risks.append(f"Poor financial health ({report.health_score}/100)")
        elif report.health_score >= 80:
            score += 15
            risks.append("Strong financial health")
        
        # Debt risk
        if report.debt_to_equity and report.debt_to_equity > 1.5:
            score -= 20
            risks.append(f"High debt burden (D/E {report.debt_to_equity:.2f}x)")
        elif report.debt_to_equity and report.debt_to_equity < 0.5:
            score += 10
            risks.append("Low debt risk")
        
        # Volatility risk
        if data.beta and data.beta > 1.5:
            score -= 15
            risks.append(f"High volatility (Beta {data.beta:.1f})")
        elif data.beta and data.beta < 0.8:
            score += 10
            risks.append("Low volatility/defensive")
        
        # Earnings risk
        if report.beat_rate <= 1:
            score -= 15
            risks.append("Unreliable earnings history")
        elif report.beat_rate >= 3:
            score += 10
            risks.append("Consistent earnings performer")
        
        # Analyst divergence risk
        if report.num_analysts > 0 and report.wall_street_confidence < 50:
            score -= 10
            risks.append("Analyst disagreement")
        
        # Macro risk
        if report.market_regime == "bear":
            score -= 10
            risks.append("Bear market environment")
        
        score = max(10, min(95, score))
        
        if score >= 65:
            signal = "bullish"  # Low risk
        elif score <= 35:
            signal = "bearish"  # High risk
        else:
            signal = "neutral"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=abs(score - 50) + 50,
            reasoning=f"Risk assessment: {', '.join(risks)}",
            key_metrics={
                "health_score": report.health_score,
                "beta": data.beta,
                "debt_to_equity": report.debt_to_equity,
                "risks": risks
            }
        )


class CathieWoodWithResearch(InvestmentAgent):
    """Cathie Wood with research insights"""
    
    def __init__(self):
        super().__init__(
            "Cathie Wood (Research-Informed)",
            "Disruptive innovation investing with data-driven insights."
        )
    
    def analyze_with_report(self, data: EnhancedStockData, report: AnalystReport) -> AgentSignal:
        """Innovation-focused analysis"""
        score = 50
        reasoning_parts = []
        
        # Innovation score from research
        innovation_score = data.financials.innovation_score
        if innovation_score >= 70:
            score += 25
            reasoning_parts.append(f"High innovation investment ({innovation_score}/100)")
        elif innovation_score >= 50:
            score += 15
            reasoning_parts.append(f"Moderate innovation focus ({innovation_score}/100)")
        elif innovation_score < 30:
            score -= 15
            reasoning_parts.append("Limited innovation investment")
        
        # R&D intensity
        rd_ratio = data.financials.rd_to_revenue
        if rd_ratio and rd_ratio > 15:
            score += 20
            reasoning_parts.append(f"Heavy R&D: {rd_ratio:.1f}% of revenue")
        elif rd_ratio and rd_ratio > 8:
            score += 10
            reasoning_parts.append(f"Strong R&D: {rd_ratio:.1f}%")
        
        # Growth metrics
        if data.financials.revenue_growth_yoy and data.financials.revenue_growth_yoy > 20:
            score += 15
            reasoning_parts.append(f"Rapid growth: {data.financials.revenue_growth_yoy:.1f}%")
        elif data.financials.revenue_growth_yoy and data.financials.revenue_growth_yoy < 0:
            score -= 10
            reasoning_parts.append("Revenue decline")
        
        # Earnings growth
        if data.financials.earnings_growth_yoy and data.financials.earnings_growth_yoy > 25:
            score += 10
            reasoning_parts.append("Explosive earnings growth")
        
        # Sector preference
        if data.sector in ['Technology', 'Healthcare', 'Biotechnology', 'Communications']:
            score += 15
            reasoning_parts.append(f"Innovation sector: {data.sector}")
        else:
            score -= 10
            reasoning_parts.append(f"Traditional sector: {data.sector}")
        
        # Wall Street support helps
        if report.wall_street_signal == "bullish":
            score += 10
            reasoning_parts.append("Institutional support")
        
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
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "Neutral on innovation potential",
            key_metrics={
                "innovation_score": innovation_score,
                "rd_ratio": rd_ratio,
                "revenue_growth": data.financials.revenue_growth_yoy,
                "sector": data.sector
            }
        )


class TwoTierAIHedgeFund:
    """Two-tier AI Hedge Fund: Analysts → Investment Masters"""
    
    def __init__(self):
        self.data_fetcher = EnhancedDataFetcher()
        self.analyst_team = DataAnalystTeam()
        
        # Tier 2: Investment Masters (informed by research)
        self.investment_masters = [
            WarrenBuffettWithResearch(),
            BenGrahamWithResearch(),
            TechnicalAnalystWithResearch(),
            RiskManagerWithResearch(),
            CathieWoodWithResearch()
        ]
    
    def analyze(self, ticker: str, detailed: bool = False):
        """Two-tier analysis process"""
        
        # Step 1: Fetch all data
        data = self.data_fetcher.get_enhanced_data(ticker)
        
        # Step 2: Tier 1 - Analysts generate research report
        research_report = self.analyst_team.generate_research_report(data)
        
        # Step 3: Tier 2 - Investment Masters review research and decide
        master_signals = []
        for master in self.investment_masters:
            try:
                signal = master.analyze_with_report(data, research_report)
                master_signals.append(signal)
            except Exception as e:
                print(f"Master {master.name} failed: {e}", file=sys.stderr)
        
        # Step 4: Generate consensus from masters' decisions
        bullish_count = sum(1 for s in master_signals if s.signal == "bullish")
        bearish_count = sum(1 for s in master_signals if s.signal == "bearish")
        neutral_count = sum(1 for s in master_signals if s.signal == "neutral")
        total = len(master_signals)
        
        total_confidence = sum(s.confidence for s in master_signals)
        avg_confidence = total_confidence / total if total > 0 else 50
        
        # Determine consensus
        if bullish_count > bearish_count and bullish_count > neutral_count:
            consensus_signal = "bullish"
            consensus_confidence = int(avg_confidence * (bullish_count / total))
        elif bearish_count > bullish_count and bearish_count > neutral_count:
            consensus_signal = "bearish"
            consensus_confidence = int(avg_confidence * (bearish_count / total))
        else:
            consensus_signal = "neutral"
            consensus_confidence = int(avg_confidence * 0.7)
        
        # Position sizing recommendation
        if consensus_signal == "bullish" and consensus_confidence > 70:
            recommendation = "Consider 5-10% position size"
        elif consensus_signal == "bullish":
            recommendation = "Consider 3-5% position size"
        elif consensus_signal == "neutral":
            recommendation = "Watchlist candidate, no position"
        else:
            recommendation = "Avoid or reduce position"
        
        return {
            "ticker": ticker,
            "signal": consensus_signal,
            "confidence": consensus_confidence,
            "agreement": f"{bullish_count}/{total} bullish, {bearish_count}/{total} bearish",
            "master_signals": master_signals,
            "research_report": research_report,
            "recommendation": recommendation
        }
