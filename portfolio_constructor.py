#!/usr/bin/env python3
"""
AI Hedge Fund - Portfolio Construction Module
Modern Portfolio Theory (Markowitz) optimization with risk parity
"""

import os
import sys
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# Import from main module
sys.path.insert(0, str(Path(__file__).parent))
from ai_hedge_fund_advanced import AIHedgeFundAdvanced, DataFetcher, ConsensusResult

@dataclass
class PortfolioAsset:
    """Asset in portfolio"""
    ticker: str
    weight: float  # Target weight (0-1)
    signal: str  # bullish/bearish/neutral
    confidence: int  # 0-100
    expected_return: float  # Annual expected return
    volatility: float  # Annual volatility
    beta: float
    sector: str
    reasoning: str

@dataclass
class PortfolioAnalysis:
    """Portfolio analysis result"""
    assets: List[PortfolioAsset]
    total_expected_return: float
    total_volatility: float
    sharpe_ratio: float
    beta: float
    max_drawdown_estimate: float
    diversification_score: float  # 0-100
    sector_concentration: Dict[str, float]
    rebalancing_needed: bool
    recommendations: List[str]

class PortfolioOptimizer:
    """Portfolio optimization using Modern Portfolio Theory"""
    
    def __init__(self, risk_free_rate: float = 0.04):
        self.risk_free_rate = risk_free_rate  # 4% annual
        self.data_fetcher = DataFetcher()
    
    def build_portfolio(self, tickers: List[str], 
                       target_risk: str = "moderate",
                       max_position: float = 0.20,
                       min_position: float = 0.02) -> PortfolioAnalysis:
        """
        Build optimized portfolio from list of tickers
        
        Args:
            tickers: List of stock tickers to consider
            target_risk: "conservative", "moderate", or "aggressive"
            max_position: Maximum weight for single position (default 20%)
            min_position: Minimum weight for any position (default 2%)
        """
        print(f"\n📊 Building {target_risk} portfolio from {len(tickers)} candidates...\n", file=sys.stderr)
        
        # 1. Analyze each stock
        hedge_fund = AIHedgeFundAdvanced(use_subagents=False)  # Use rules for speed
        analyses = []
        
        for ticker in tickers:
            try:
                result = hedge_fund.analyze(ticker)
                data = self.data_fetcher.get_comprehensive_data(ticker)
                
                # Calculate historical returns/volatility
                hist_returns = self._get_historical_returns(ticker)
                
                analyses.append({
                    "ticker": ticker,
                    "result": result,
                    "data": data,
                    "historical": hist_returns
                })
                
                emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}[result.signal]
                print(f"{emoji} {ticker:6} {result.signal.upper():8} ({result.confidence:2}%)", file=sys.stderr)
            except Exception as e:
                print(f"❌ {ticker}: Analysis failed - {e}", file=sys.stderr)
        
        if len(analyses) < 2:
            raise ValueError("Need at least 2 valid stocks for portfolio construction")
        
        # 2. Filter based on signal quality
        qualified = [a for a in analyses if a["result"].signal != "bearish"]
        if len(qualified) < 2:
            print("⚠️  Few bullish stocks, including neutrals", file=sys.stderr)
            qualified = analyses[:10]  # Take top 10
        
        # 3. Calculate expected returns based on signals
        for a in qualified:
            a["expected_return"] = self._estimate_return(a["result"], a["historical"])
            a["volatility"] = a["historical"]["volatility"] if a["historical"] else 0.30
            a["beta"] = a["data"].get("beta", 1.0) or 1.0
        
        # 4. Optimize weights
        weights = self._optimize_weights(qualified, target_risk, max_position, min_position)
        
        # 5. Build portfolio assets
        assets = []
        for i, a in enumerate(qualified):
            if weights[i] >= min_position:
                assets.append(PortfolioAsset(
                    ticker=a["ticker"],
                    weight=weights[i],
                    signal=a["result"].signal,
                    confidence=a["result"].confidence,
                    expected_return=a["expected_return"],
                    volatility=a["volatility"],
                    beta=a["beta"],
                    sector=a["data"].get("sector", "Unknown"),
                    reasoning=a["result"].recommendation
                ))
        
        # 6. Calculate portfolio metrics
        return self._calculate_portfolio_metrics(assets, target_risk)
    
    def _get_historical_returns(self, ticker: str) -> Optional[Dict]:
        """Get historical price data and calculate returns/volatility"""
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2y")
            
            if len(hist) < 252:  # Need at least 1 year of data
                return None
            
            # Calculate daily returns
            daily_returns = hist['Close'].pct_change().dropna()
            
            # Annualized metrics
            annual_return = daily_returns.mean() * 252
            annual_volatility = daily_returns.std() * np.sqrt(252)
            
            # Calculate max drawdown
            cumulative = (1 + daily_returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown = drawdown.min()
            
            return {
                "annual_return": annual_return,
                "annual_volatility": annual_volatility,
                "max_drawdown": max_drawdown,
                "sharpe": (annual_return - self.risk_free_rate) / annual_volatility if annual_volatility > 0 else 0,
                "volatility": annual_volatility
            }
        except Exception as e:
            print(f"Warning: Could not get historical data for {ticker}: {e}", file=sys.stderr)
            return None
    
    def _estimate_return(self, analysis: ConsensusResult, historical: Optional[Dict]) -> float:
        """Estimate expected annual return based on analysis and historical data"""
        
        # Base return estimate from signal
        if analysis.signal == "bullish":
            base_return = 0.12 + (analysis.confidence / 100) * 0.08  # 12-20%
        elif analysis.signal == "neutral":
            base_return = 0.06 + (analysis.confidence / 100) * 0.04  # 6-10%
        else:  # bearish
            base_return = -0.05  # -5%
        
        # Blend with historical if available
        if historical:
            # Weight: 60% AI prediction, 40% historical
            blended = 0.6 * base_return + 0.4 * historical["annual_return"]
            return blended
        
        return base_return
    
    def _optimize_weights(self, assets: List[Dict], target_risk: str, 
                         max_position: float, min_position: float) -> np.ndarray:
        """
        Optimize portfolio weights using mean-variance optimization
        """
        n = len(assets)
        
        # Expected returns and volatilities
        returns = np.array([a["expected_return"] for a in assets])
        vols = np.array([a["volatility"] for a in assets])
        
        # Simplified covariance matrix (assume 0.3 correlation for now)
        # In production, calculate from historical returns
        corr = 0.3
        cov = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i == j:
                    cov[i, j] = vols[i] ** 2
                else:
                    cov[i, j] = corr * vols[i] * vols[j]
        
        # Risk tolerance
        risk_multiplier = {
            "conservative": 0.5,
            "moderate": 1.0,
            "aggressive": 1.5
        }.get(target_risk, 1.0)
        
        # Simplified optimization: maximize Sharpe ratio with constraints
        # Using inverse volatility weighting as a simple heuristic
        inv_vols = 1.0 / (vols + 0.01)  # Add small constant to avoid division by zero
        weights = inv_vols / inv_vols.sum()
        
        # Adjust based on expected returns (higher return = higher weight)
        return_adjustment = (returns - returns.min()) / (returns.max() - returns.min() + 0.001)
        weights = weights * (1 + return_adjustment)
        weights = weights / weights.sum()
        
        # Apply constraints
        weights = np.clip(weights, min_position, max_position)
        weights = weights / weights.sum()  # Re-normalize
        
        return weights
    
    def _calculate_portfolio_metrics(self, assets: List[PortfolioAsset], 
                                    target_risk: str) -> PortfolioAnalysis:
        """Calculate portfolio-level metrics"""
        
        weights = np.array([a.weight for a in assets])
        returns = np.array([a.expected_return for a in assets])
        vols = np.array([a.volatility for a in assets])
        betas = np.array([a.beta for a in assets])
        
        # Portfolio expected return (weighted average)
        total_return = np.dot(weights, returns)
        
        # Portfolio volatility (simplified - assumes 0.3 correlation)
        # In production, use full covariance matrix
        portfolio_var = 0
        for i in range(len(assets)):
            for j in range(len(assets)):
                corr = 1.0 if i == j else 0.3
                portfolio_var += weights[i] * weights[j] * vols[i] * vols[j] * corr
        
        total_volatility = np.sqrt(portfolio_var)
        
        # Sharpe ratio
        sharpe = (total_return - self.risk_free_rate) / total_volatility if total_volatility > 0 else 0
        
        # Portfolio beta
        portfolio_beta = np.dot(weights, betas)
        
        # Estimated max drawdown (rough estimate: 2.5x volatility)
        max_dd_estimate = -2.5 * total_volatility
        
        # Diversification score (based on number of positions and sector spread)
        sectors = {}
        for a in assets:
            sectors[a.sector] = sectors.get(a.sector, 0) + a.weight
        
        # Herfindahl index for sector concentration
        sector_hhi = sum(w**2 for w in sectors.values())
        diversification_score = int((1 - sector_hhi) * 100)
        
        # Check if rebalancing needed
        rebalancing_needed = any(
            a.weight > 0.15 or a.weight < 0.03 or a.signal == "bearish"
            for a in assets
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            assets, total_return, total_volatility, sharpe, sectors, target_risk
        )
        
        return PortfolioAnalysis(
            assets=assets,
            total_expected_return=total_return,
            total_volatility=total_volatility,
            sharpe_ratio=sharpe,
            beta=portfolio_beta,
            max_drawdown_estimate=max_dd_estimate,
            diversification_score=diversification_score,
            sector_concentration=sectors,
            rebalancing_needed=rebalancing_needed,
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, assets: List[PortfolioAsset], 
                                  total_return: float, total_vol: float,
                                  sharpe: float, sectors: Dict[str, float],
                                  target_risk: str) -> List[str]:
        """Generate portfolio recommendations"""
        recommendations = []
        
        # Risk/return assessment
        if total_vol > 0.25 and target_risk != "aggressive":
            recommendations.append(f"⚠️  High volatility ({total_vol:.1%}). Consider reducing position sizes or adding defensive stocks.")
        
        if sharpe < 0.5:
            recommendations.append(f"⚠️  Low Sharpe ratio ({sharpe:.2f}). Risk-adjusted returns could be improved.")
        elif sharpe > 1.0:
            recommendations.append(f"✅ Excellent Sharpe ratio ({sharpe:.2f}). Good risk-adjusted returns.")
        
        # Sector concentration
        max_sector = max(sectors.items(), key=lambda x: x[1])
        if max_sector[1] > 0.40:
            recommendations.append(f"⚠️  High concentration in {max_sector[0]} ({max_sector[1]:.1%}). Consider diversifying.")
        
        # Individual position recommendations
        for asset in assets:
            if asset.signal == "bearish" and asset.weight > 0.05:
                recommendations.append(f"🔴 Reduce {asset.ticker} ({asset.weight:.1%}) - bearish signal")
            elif asset.signal == "bullish" and asset.confidence > 80 and asset.weight < 0.10:
                recommendations.append(f"🟢 Consider increasing {asset.ticker} - strong bullish signal")
        
        # Minimum positions
        small_positions = [a for a in assets if a.weight < 0.03]
        if len(small_positions) > 0:
            recommendations.append(f"💡 {len(small_positions)} positions under 3% - consider consolidating")
        
        return recommendations
    
    def analyze_existing_portfolio(self, holdings: Dict[str, float]) -> PortfolioAnalysis:
        """
        Analyze existing portfolio and provide recommendations
        
        Args:
            holdings: Dict of {ticker: current_weight}
        """
        print(f"\n📊 Analyzing existing portfolio with {len(holdings)} positions...\n", file=sys.stderr)
        
        # Analyze each holding
        hedge_fund = AIHedgeFundAdvanced(use_subagents=False)
        assets = []
        
        for ticker, weight in holdings.items():
            try:
                result = hedge_fund.analyze(ticker)
                data = self.data_fetcher.get_comprehensive_data(ticker)
                hist = self._get_historical_returns(ticker)
                
                assets.append(PortfolioAsset(
                    ticker=ticker,
                    weight=weight,
                    signal=result.signal,
                    confidence=result.confidence,
                    expected_return=self._estimate_return(result, hist),
                    volatility=hist["volatility"] if hist else 0.30,
                    beta=data.get("beta", 1.0) or 1.0,
                    sector=data.get("sector", "Unknown"),
                    reasoning=result.recommendation
                ))
                
                emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}[result.signal]
                print(f"{emoji} {ticker:6} {weight:5.1%} {result.signal.upper():8}", file=sys.stderr)
            except Exception as e:
                print(f"❌ {ticker}: {e}", file=sys.stderr)
        
        return self._calculate_portfolio_metrics(assets, "moderate")

def format_portfolio_output(analysis: PortfolioAnalysis, title: str = "Portfolio Analysis") -> str:
    """Format portfolio analysis for display"""
    lines = [
        f"\n{'='*80}",
        f"📊 {title}",
        f"{'='*80}",
        ""
    ]
    
    # Asset allocation
    lines.append("💼 Recommended Allocation:")
    lines.append("-" * 60)
    lines.append(f"{'Ticker':<10} {'Weight':<10} {'Signal':<10} {'Exp Return':<12} {'Volatility':<12}")
    lines.append("-" * 60)
    
    for asset in sorted(analysis.assets, key=lambda x: x.weight, reverse=True):
        exp_ret = asset.expected_return if asset.expected_return is not None else 0
        vol = asset.volatility if asset.volatility is not None else 0
        lines.append(
            f"{asset.ticker:<10} {asset.weight:>8.1%}   {asset.signal.upper():<8} "
            f"{exp_ret:>9.1%}     {vol:>9.1%}"
        )
    
    lines.append("")
    
    # Portfolio metrics
    lines.append("📈 Portfolio Metrics:")
    lines.append("-" * 40)
    lines.append(f"  Expected Annual Return:  {analysis.total_expected_return or 0:>8.1%}")
    lines.append(f"  Expected Volatility:     {analysis.total_volatility or 0:>8.1%}")
    lines.append(f"  Sharpe Ratio:            {analysis.sharpe_ratio or 0:>8.2f}")
    lines.append(f"  Portfolio Beta:          {analysis.beta or 1.0:>8.2f}")
    lines.append(f"  Est. Max Drawdown:       {analysis.max_drawdown_estimate or 0:>8.1%}")
    lines.append(f"  Diversification Score:   {analysis.diversification_score or 0:>8.0f}/100")
    lines.append("")
    
    # Sector breakdown
    lines.append("🏭 Sector Allocation:")
    lines.append("-" * 40)
    for sector, weight in sorted(analysis.sector_concentration.items(), key=lambda x: x[1] or 0, reverse=True):
        w = weight or 0
        s = sector or "Unknown"
        bar = "█" * int(w * 30)
        lines.append(f"  {s:<25} {w:>6.1%} {bar}")
    lines.append("")
    
    # Recommendations
    lines.append("💡 Recommendations:")
    lines.append("-" * 40)
    for rec in analysis.recommendations:
        lines.append(f"  {rec}")
    
    if not analysis.recommendations:
        lines.append("  ✅ Portfolio looks well-balanced")
    
    lines.append(f"\n{'='*80}\n")
    
    return "\n".join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Hedge Fund - Portfolio Construction")
    parser.add_argument("tickers", help="Comma-separated stock tickers")
    parser.add_argument("--risk", "-r", choices=["conservative", "moderate", "aggressive"], 
                       default="moderate", help="Target risk profile")
    parser.add_argument("--max-position", "-p", type=float, default=0.20,
                       help="Maximum position size as decimal (default 0.20 for 20 percent)")
    parser.add_argument("--existing", "-e", action="store_true",
                       help="Analyze existing portfolio (provide weights in tickers)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    optimizer = PortfolioOptimizer()
    
    try:
        if args.existing:
            # Parse existing holdings (format: AAPL:0.3,MSFT:0.2,...)
            holdings = {}
            for item in args.tickers.split(","):
                if ":" in item:
                    ticker, weight = item.split(":")
                    holdings[ticker.strip().upper()] = float(weight)
                else:
                    # Equal weight if no weight specified
                    tickers = [t.strip().upper() for t in args.tickers.split(",")]
                    equal_weight = 1.0 / len(tickers)
                    holdings = {t: equal_weight for t in tickers}
            
            analysis = optimizer.analyze_existing_portfolio(holdings)
            title = "Existing Portfolio Analysis"
        else:
            # Build new portfolio
            tickers = [t.strip().upper() for t in args.tickers.split(",")]
            analysis = optimizer.build_portfolio(
                tickers, 
                target_risk=args.risk,
                max_position=args.max_position
            )
            title = f"Optimized {args.risk.title()} Portfolio"
        
        if args.json:
            result = {
                "assets": [
                    {
                        "ticker": a.ticker,
                        "weight": a.weight,
                        "signal": a.signal,
                        "expected_return": a.expected_return,
                        "volatility": a.volatility,
                        "sector": a.sector
                    }
                    for a in analysis.assets
                ],
                "metrics": {
                    "expected_return": analysis.total_expected_return,
                    "volatility": analysis.total_volatility,
                    "sharpe_ratio": analysis.sharpe_ratio,
                    "beta": analysis.beta,
                    "max_drawdown_estimate": analysis.max_drawdown_estimate,
                    "diversification_score": analysis.diversification_score
                },
                "sector_allocation": analysis.sector_concentration,
                "recommendations": analysis.recommendations
            }
            print(json.dumps(result, indent=2))
        else:
            print(format_portfolio_output(analysis, title))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()