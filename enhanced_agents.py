"""
Enhanced Investment Agents
New agents based on stock-analysis features
"""

from typing import Dict, List
from data_enhancement import EnhancedStockData
from base import AgentSignal, InvestmentAgent


class EarningsAgent(InvestmentAgent):
    """Analyze earnings surprises and trends"""
    
    def __init__(self):
        super().__init__(
            "Earnings Analyst",
            "Focus on EPS surprises, beat rates, and earnings quality."
        )
    
    def analyze_enhanced(self, data: EnhancedStockData) -> AgentSignal:
        score = 50
        reasoning_parts = []
        
        earnings = data.earnings
        
        # Recent earnings surprise
        if earnings.surprise_pct is not None:
            if earnings.surprise_pct > 10:
                score += 25
                reasoning_parts.append(f"Huge beat: +{earnings.surprise_pct:.1f}%")
            elif earnings.surprise_pct > 5:
                score += 15
                reasoning_parts.append(f"Strong beat: +{earnings.surprise_pct:.1f}%")
            elif earnings.surprise_pct > 0:
                score += 5
                reasoning_parts.append(f"Beat: +{earnings.surprise_pct:.1f}%")
            elif earnings.surprise_pct > -5:
                score -= 10
                reasoning_parts.append(f"Miss: {earnings.surprise_pct:.1f}%")
            else:
                score -= 25
                reasoning_parts.append(f"Big miss: {earnings.surprise_pct:.1f}%")
        else:
            reasoning_parts.append("No recent earnings data")
        
        # Historical beat rate
        if earnings.beats_last_4q > 0:
            if earnings.beats_last_4q >= 3:
                score += 15
                reasoning_parts.append(f"Consistent: beat {earnings.beats_last_4q}/4 quarters")
            elif earnings.beats_last_4q >= 2:
                score += 5
                reasoning_parts.append(f"Beat {earnings.beats_last_4q}/4 quarters")
            else:
                score -= 10
                reasoning_parts.append(f"Struggling: only {earnings.beats_last_4q}/4 beats")
        
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
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "No earnings data",
            key_metrics={"eps_surprise": earnings.surprise_pct, "beats_4q": earnings.beats_last_4q}
        )


class AnalystConsensusAgent(InvestmentAgent):
    """Analyze Wall Street analyst consensus"""
    
    def __init__(self):
        super().__init__(
            "Wall Street Consensus",
            "Aggregate analyst ratings, price targets, and institutional sentiment."
        )
    
    def analyze_enhanced(self, data: EnhancedStockData) -> AgentSignal:
        score = 50
        reasoning_parts = []
        
        analyst = data.analyst
        
        # Consensus rating
        rating_scores = {
            'strong_buy': 90,
            'buy': 75,
            'hold': 50,
            'sell': 25,
            'strong_sell': 10,
        }
        
        if analyst.consensus_rating in rating_scores:
            rating_score = rating_scores[analyst.consensus_rating]
            score = (score + rating_score) / 2  # Blend with base
            reasoning_parts.append(f"Consensus: {analyst.consensus_rating.replace('_', ' ')}")
        
        # Number of analysts (more = more reliable)
        if analyst.num_analysts > 0:
            if analyst.num_analysts >= 15:
                reasoning_parts.append(f"Strong coverage: {analyst.num_analysts} analysts")
            elif analyst.num_analysts >= 5:
                reasoning_parts.append(f"Moderate coverage: {analyst.num_analysts} analysts")
            else:
                reasoning_parts.append(f"Limited coverage: {analyst.num_analysts} analysts")
        
        # Upside potential
        if analyst.upside_pct is not None:
            if analyst.upside_pct > 20:
                score += 15
                reasoning_parts.append(f"Big upside: {analyst.upside_pct:+.1f}% to target")
            elif analyst.upside_pct > 10:
                score += 10
                reasoning_parts.append(f"Good upside: {analyst.upside_pct:+.1f}%")
            elif analyst.upside_pct > 0:
                score += 5
                reasoning_parts.append(f"Some upside: {analyst.upside_pct:+.1f}%")
            elif analyst.upside_pct > -10:
                score -= 10
                reasoning_parts.append(f"Downside: {analyst.upside_pct:+.1f}%")
            else:
                score -= 20
                reasoning_parts.append(f"Big downside: {analyst.upside_pct:+.1f}%")
        
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
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "No analyst data",
            key_metrics={
                "consensus": analyst.consensus_rating,
                "num_analysts": analyst.num_analysts,
                "upside": analyst.upside_pct
            }
        )


class MacroAgent(InvestmentAgent):
    """Analyze macro environment impact"""
    
    def __init__(self):
        super().__init__(
            "Macro Strategist",
            "Assess VIX, market trends, and risk-off/risk-on environment."
        )
    
    def analyze_enhanced(self, data: EnhancedStockData) -> AgentSignal:
        score = 50
        reasoning_parts = []
        
        macro = data.macro
        
        # VIX analysis (lower is better for stocks)
        if macro.vix_level is not None:
            if macro.vix_level < 15:
                score += 15
                reasoning_parts.append(f"VIX {macro.vix_level:.1f}: Calm market")
            elif macro.vix_level < 20:
                score += 5
                reasoning_parts.append(f"VIX {macro.vix_level:.1f}: Normal volatility")
            elif macro.vix_level < 25:
                score -= 5
                reasoning_parts.append(f"VIX {macro.vix_level:.1f}: Elevated caution")
            elif macro.vix_level < 35:
                score -= 15
                reasoning_parts.append(f"VIX {macro.vix_level:.1f}: Fear in market")
            else:
                score -= 25
                reasoning_parts.append(f"VIX {macro.vix_level:.1f}: High panic!")
        
        # Market regime
        if macro.market_regime == 'bull':
            score += 10
            reasoning_parts.append("Bull market regime")
        elif macro.market_regime == 'bear':
            score -= 15
            reasoning_parts.append("Bear market regime")
        else:
            reasoning_parts.append("Choppy market")
        
        # SPY trend
        if macro.spy_trend_10d > 3:
            score += 10
            reasoning_parts.append(f"SPY strong: +{macro.spy_trend_10d:.1f}% (10d)")
        elif macro.spy_trend_10d < -3:
            score -= 10
            reasoning_parts.append(f"SPY weak: {macro.spy_trend_10d:.1f}% (10d)")
        
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
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "No macro data",
            key_metrics={
                "vix": macro.vix_level,
                "market_regime": macro.market_regime,
                "spy_trend": macro.spy_trend_10d
            }
        )


class DividendAgent(InvestmentAgent):
    """Analyze dividend quality for income investors"""
    
    def __init__(self):
        super().__init__(
            "Dividend Investor",
            "Focus on dividend yield, safety, growth, and income quality."
        )
    
    def analyze_enhanced(self, data: EnhancedStockData) -> AgentSignal:
        score = 50
        reasoning_parts = []
        
        dividend = data.dividend
        
        # No dividend = neutral for this agent
        if dividend.income_rating == 'no_dividend':
            return AgentSignal(
                agent_name=self.name,
                signal="neutral",
                confidence=50,
                reasoning="No dividend paid - not an income stock",
                key_metrics={"yield": None, "safety": 0}
            )
        
        # Yield analysis
        if dividend.yield_pct is not None:
            if dividend.yield_pct > 5:
                score += 10
                reasoning_parts.append(f"High yield: {dividend.yield_pct:.2f}%")
            elif dividend.yield_pct > 3:
                score += 20
                reasoning_parts.append(f"Good yield: {dividend.yield_pct:.2f}%")
            elif dividend.yield_pct > 2:
                score += 15
                reasoning_parts.append(f"Decent yield: {dividend.yield_pct:.2f}%")
            elif dividend.yield_pct > 0:
                score += 5
                reasoning_parts.append(f"Low yield: {dividend.yield_pct:.2f}%")
        
        # Safety analysis
        if dividend.payout_status == 'safe':
            score += 25
            reasoning_parts.append(f"Safe payout: {dividend.payout_ratio:.1f}%")
        elif dividend.payout_status == 'moderate':
            score += 15
            reasoning_parts.append(f"Moderate payout: {dividend.payout_ratio:.1f}%")
        elif dividend.payout_status == 'high':
            score -= 5
            reasoning_parts.append(f"High payout risk: {dividend.payout_ratio:.1f}%")
        elif dividend.payout_status == 'unsustainable':
            score -= 25
            reasoning_parts.append(f"Unsustainable payout: {dividend.payout_ratio:.1f}%!")
        
        # Growth
        if dividend.growth_5y is not None:
            if dividend.growth_5y > 10:
                score += 15
                reasoning_parts.append(f"Strong growth: {dividend.growth_5y:.1f}% (5Y)")
            elif dividend.growth_5y > 5:
                score += 10
                reasoning_parts.append(f"Good growth: {dividend.growth_5y:.1f}% (5Y)")
            elif dividend.growth_5y > 0:
                score += 5
                reasoning_parts.append(f"Slow growth: {dividend.growth_5y:.1f}% (5Y)")
            else:
                score -= 10
                reasoning_parts.append(f"Declining dividend: {dividend.growth_5y:.1f}%")
        
        # Consecutive years
        if dividend.consecutive_years is not None:
            if dividend.consecutive_years >= 25:
                score += 15
                reasoning_parts.append(f"Dividend aristocrat: {dividend.consecutive_years} years!")
            elif dividend.consecutive_years >= 10:
                score += 10
                reasoning_parts.append(f"Consistent: {dividend.consecutive_years} years")
            elif dividend.consecutive_years >= 5:
                score += 5
                reasoning_parts.append(f"{dividend.consecutive_years} years of increases")
        
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
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "No dividend data",
            key_metrics={
                "yield": dividend.yield_pct,
                "safety_score": dividend.safety_score,
                "payout_ratio": dividend.payout_ratio
            }
        )


class FinancialHealthAgent(InvestmentAgent):
    """Analyze comprehensive financial health"""
    
    def __init__(self):
        super().__init__(
            "Financial Health Analyst",
            "Deep dive into margins, debt, cash flow, and financial stability."
        )
    
    def analyze_enhanced(self, data: EnhancedStockData) -> AgentSignal:
        score = 50
        reasoning_parts = []
        risks = []
        
        fin = data.financials
        
        # Profitability Analysis
        if fin.operating_margin is not None:
            if fin.operating_margin > 25:
                score += 15
                reasoning_parts.append(f"Excellent margin: {fin.operating_margin:.1f}%")
            elif fin.operating_margin > 15:
                score += 10
                reasoning_parts.append(f"Strong margin: {fin.operating_margin:.1f}%")
            elif fin.operating_margin > 8:
                score += 5
                reasoning_parts.append(f"Moderate margin: {fin.operating_margin:.1f}%")
            elif fin.operating_margin < 3:
                score -= 15
                reasoning_parts.append(f"Low margin: {fin.operating_margin:.1f}%")
                risks.append("Low operating margin")
        
        if fin.gross_margin is not None:
            if fin.gross_margin > 50:
                score += 10
                reasoning_parts.append(f"High gross margin: {fin.gross_margin:.1f}%")
            elif fin.gross_margin < 20:
                score -= 10
                risks.append("Low gross margin")
        
        # ROE Analysis (with leverage quality check)
        if fin.return_on_equity is not None:
            roe = fin.return_on_equity
            roa = fin.return_on_assets if hasattr(fin, 'return_on_assets') else None
            
            # Check if ROE is leverage-driven
            is_leverage_driven = False
            if roa and roa > 0 and roe / roa > 5:
                is_leverage_driven = True
            if fin.debt_to_equity and fin.debt_to_equity > 2.0 and roe > 30:
                is_leverage_driven = True
            
            if is_leverage_driven:
                # High ROE from leverage is RISKY, not good
                if roa and roa > 0:
                    score -= 10
                    reasoning_parts.append(f"ROE {roe:.1f}% is leverage-driven (ROA only {roa:.1f}%) - risky!")
                    risks.append(f"High ROE ({roe:.1f}%) driven by debt, not quality")
                else:
                    score -= 5
                    reasoning_parts.append(f"High ROE {roe:.1f}% with high debt - quality questionable")
            elif roe > 20:
                score += 15
                reasoning_parts.append(f"Excellent ROE: {roe:.1f}% (quality-driven)")
            elif roe > 12:
                score += 10
                reasoning_parts.append(f"Good ROE: {roe:.1f}%")
            elif roe < 5:
                score -= 10
                reasoning_parts.append(f"Weak ROE: {roe:.1f}%")
                risks.append("Poor ROE")
        
        # Debt Analysis
        if fin.debt_to_equity is not None:
            if fin.debt_to_equity < 0.3:
                score += 15
                reasoning_parts.append(f"Low debt: D/E {fin.debt_to_equity:.2f}x")
            elif fin.debt_to_equity < 0.8:
                score += 5
                reasoning_parts.append(f"Manageable debt: D/E {fin.debt_to_equity:.2f}x")
            elif fin.debt_to_equity < 1.5:
                score -= 10
                reasoning_parts.append(f"Elevated debt: D/E {fin.debt_to_equity:.2f}x")
                risks.append(f"Elevated debt level (D/E {fin.debt_to_equity:.2f}x)")
            else:
                score -= 20
                reasoning_parts.append(f"High debt: D/E {fin.debt_to_equity:.2f}x!")
                risks.append(f"High debt burden (D/E {fin.debt_to_equity:.2f}x)")
        
        # Liquidity
        if fin.current_ratio is not None:
            if fin.current_ratio > 2:
                score += 10
                reasoning_parts.append(f"Strong liquidity: CR {fin.current_ratio:.2f}")
            elif fin.current_ratio < 1:
                score -= 15
                reasoning_parts.append(f"Weak liquidity: CR {fin.current_ratio:.2f}")
                risks.append("Liquidity concerns")
        
        # Cash Flow
        if fin.free_cash_flow is not None:
            if fin.free_cash_flow > 1000:  # > $1B
                score += 15
                reasoning_parts.append(f"Strong FCF: ${fin.free_cash_flow:.0f}M")
            elif fin.free_cash_flow > 0:
                score += 10
                reasoning_parts.append(f"Positive FCF: ${fin.free_cash_flow:.0f}M")
            elif fin.free_cash_flow < -500:
                score -= 15
                reasoning_parts.append(f"Negative FCF: ${fin.free_cash_flow:.0f}M")
                risks.append("Negative free cash flow")
        
        # Revenue Growth
        if fin.revenue_growth_yoy is not None:
            if fin.revenue_growth_yoy > 15:
                score += 10
                reasoning_parts.append(f"Strong growth: {fin.revenue_growth_yoy:.1f}%")
            elif fin.revenue_growth_yoy < -5:
                score -= 10
                reasoning_parts.append(f"Declining revenue: {fin.revenue_growth_yoy:.1f}%")
                risks.append("Revenue decline")
        
        # Clamp score
        score = max(10, min(95, score))
        
        if score >= 65:
            signal = "bullish"
        elif score <= 40:
            signal = "bearish"
        else:
            signal = "neutral"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=score,
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "Average financial health",
            key_metrics={
                "operating_margin": fin.operating_margin,
                "debt_to_equity": fin.debt_to_equity,
                "roe": fin.return_on_equity,
                "fcf": fin.free_cash_flow,
                "health_score": fin.financial_health_score,
                "risks": risks
            }
        )
