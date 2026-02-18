#!/usr/bin/env python3
"""
AI Hedge Fund - Rebalancing Alert System
Monitors portfolios and alerts when rebalancing is needed
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ai_hedge_fund_advanced import AIHedgeFundAdvanced, DataFetcher

@dataclass
class RebalanceAlert:
    ticker: str
    current_weight: float
    target_weight: float
    drift: float
    signal: str
    action: str  # INCREASE, DECREASE, REMOVE, ADD
    urgency: str  # HIGH, MEDIUM, LOW
    reason: str

@dataclass
class PortfolioHealth:
    portfolio_id: str
    last_rebalanced: str
    days_since_rebalance: int
    total_drift: float
    max_position_drift: float
    alerts: List[RebalanceAlert]
    recommendations: List[str]
    health_score: int  # 0-100

class RebalancingMonitor:
    """Monitor portfolio and generate rebalancing alerts"""
    
    def __init__(self, drift_threshold: float = 0.05):
        self.drift_threshold = drift_threshold  # 5% drift triggers alert
        self.data_fetcher = DataFetcher()
        self.hedge_fund = AIHedgeFundAdvanced(use_subagents=False)
    
    def check_portfolio(self, holdings: Dict[str, float], 
                       last_rebalanced: Optional[str] = None) -> PortfolioHealth:
        """
        Check portfolio health and generate alerts
        
        Args:
            holdings: {ticker: current_weight}
            last_rebalanced: Date of last rebalance (YYYY-MM-DD)
        """
        print(f"\n🔍 Checking portfolio with {len(holdings)} positions...\n", file=sys.stderr)
        
        # Calculate days since rebalance
        if last_rebalanced:
            last_date = datetime.strptime(last_rebalanced, '%Y-%m-%d')
            days_since = (datetime.now() - last_date).days
        else:
            days_since = 30  # Assume 30 if unknown
        
        alerts = []
        
        # Check each holding
        total_weight = sum(holdings.values())
        
        for ticker, current_weight in holdings.items():
            try:
                # Get current signal
                result = self.hedge_fund.analyze(ticker)
                data = self.data_fetcher.get_comprehensive_data(ticker)
                
                # Determine target weight based on signal
                if result.signal == "bullish":
                    target_weight = min(0.20, 0.10 + result.confidence / 1000)
                elif result.signal == "neutral":
                    target_weight = 0.05
                else:  # bearish
                    target_weight = 0
                
                # Calculate drift
                drift = current_weight - target_weight
                
                # Determine action and urgency
                if abs(drift) > self.drift_threshold:
                    if drift > 0:
                        action = "DECREASE"
                        urgency = "HIGH" if result.signal == "bearish" else "MEDIUM"
                    else:
                        action = "INCREASE"
                        urgency = "HIGH" if result.signal == "bullish" and result.confidence > 75 else "MEDIUM"
                    
                    alerts.append(RebalanceAlert(
                        ticker=ticker,
                        current_weight=current_weight,
                        target_weight=target_weight,
                        drift=drift,
                        signal=result.signal,
                        action=action,
                        urgency=urgency,
                        reason=f"{result.signal.upper()} signal ({result.confidence}% confidence)"
                    ))
                
                print(f"{'⚠️' if abs(drift) > self.drift_threshold else '✅'} {ticker}: {current_weight:.1%} vs target {target_weight:.1%}", file=sys.stderr)
                
            except Exception as e:
                print(f"❌ {ticker}: Error - {e}", file=sys.stderr)
        
        # Calculate health metrics
        total_drift = sum(abs(a.drift) for a in alerts)
        max_drift = max((abs(a.drift) for a in alerts), default=0)
        
        # Health score (0-100)
        health_score = max(0, 100 - int(total_drift * 200) - int(days_since / 2))
        
        # Generate recommendations
        recommendations = self._generate_recommendations(alerts, days_since, holdings)
        
        return PortfolioHealth(
            portfolio_id="portfolio_1",
            last_rebalanced=last_rebalanced or "Unknown",
            days_since_rebalance=days_since,
            total_drift=total_drift,
            max_position_drift=max_drift,
            alerts=alerts,
            recommendations=recommendations,
            health_score=health_score
        )
    
    def _generate_recommendations(self, alerts: List[RebalanceAlert], 
                                  days_since: int, 
                                  holdings: Dict[str, float]) -> List[str]:
        """Generate rebalancing recommendations"""
        recommendations = []
        
        # Time-based recommendation
        if days_since > 90:
            recommendations.append(f"⚠️  Portfolio hasn't been rebalanced in {days_since} days. Consider rebalancing.")
        elif days_since > 30:
            recommendations.append(f"💡 {days_since} days since last rebalance. Review recommended.")
        
        # High urgency alerts
        high_urgency = [a for a in alerts if a.urgency == "HIGH"]
        if high_urgency:
            recommendations.append(f"🔴 {len(high_urgency)} positions need immediate attention:")
            for alert in high_urgency[:3]:
                recommendations.append(f"   - {alert.ticker}: {alert.action} by {abs(alert.drift):.1%}")
        
        # Concentration check
        max_pos = max(holdings.values()) if holdings else 0
        if max_pos > 0.20:
            max_ticker = max(holdings.items(), key=lambda x: x[1])[0]
            recommendations.append(f"⚠️  High concentration: {max_ticker} at {max_pos:.1%}. Consider reducing.")
        
        # Cash recommendation
        total_invested = sum(holdings.values())
        if total_invested > 0.95:
            recommendations.append("💡 Portfolio fully invested. Consider keeping 5-10% cash for opportunities.")
        
        # Sector check (simplified)
        # Would need sector data here
        
        return recommendations
    
    def schedule_rebalance(self, portfolio_health: PortfolioHealth) -> Dict:
        """Generate rebalancing schedule"""
        schedule = {
            "immediate_actions": [],
            "this_week": [],
            "this_month": [],
            "monitor": []
        }
        
        for alert in portfolio_health.alerts:
            if alert.urgency == "HIGH":
                schedule["immediate_actions"].append({
                    "ticker": alert.ticker,
                    "action": alert.action,
                    "target_weight": alert.target_weight,
                    "reason": alert.reason
                })
            elif alert.urgency == "MEDIUM":
                schedule["this_week"].append({
                    "ticker": alert.ticker,
                    "action": alert.action,
                    "adjustment": f"{abs(alert.drift):.1%}"
                })
            else:
                schedule["monitor"].append(alert.ticker)
        
        return schedule

def format_rebalance_report(health: PortfolioHealth) -> str:
    """Format rebalancing report"""
    lines = [
        f"\n{'='*80}",
        f"🔔 Portfolio Rebalancing Report",
        f"{'='*80}",
        f"Last Rebalanced: {health.last_rebalanced} ({health.days_since_rebalance} days ago)",
        f"Health Score: {health.health_score}/100",
        ""
    ]
    
    # Alerts
    if health.alerts:
        lines.append("⚠️  Rebalancing Alerts:")
        lines.append("-" * 80)
        lines.append(f"{'Ticker':<10} {'Current':<10} {'Target':<10} {'Drift':<10} {'Action':<10} {'Urgency'}")
        lines.append("-" * 80)
        
        for alert in sorted(health.alerts, key=lambda x: abs(x.drift), reverse=True):
            urgency_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}[alert.urgency]
            lines.append(
                f"{alert.ticker:<10} {alert.current_weight:>8.1%}  {alert.target_weight:>8.1%}  "
                f"{alert.drift:>+8.1%}  {alert.action:<10} {urgency_emoji} {alert.urgency}"
            )
        lines.append("")
    else:
        lines.append("✅ No rebalancing needed at this time.")
        lines.append("")
    
    # Recommendations
    if health.recommendations:
        lines.append("💡 Recommendations:")
        lines.append("-" * 40)
        for rec in health.recommendations:
            lines.append(f"  {rec}")
        lines.append("")
    
    # Summary
    lines.append("📊 Summary:")
    lines.append("-" * 40)
    lines.append(f"  Total Drift:         {health.total_drift:.1%}")
    lines.append(f"  Max Position Drift:  {health.max_position_drift:.1%}")
    lines.append(f"  Alerts:              {len(health.alerts)}")
    lines.append(f"{'='*80}\n")
    
    return "\n".join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Hedge Fund - Rebalancing Monitor")
    parser.add_argument("holdings", help="Holdings as ticker:weight pairs (e.g., AAPL:0.3,MSFT:0.2)")
    parser.add_argument("--last-rebalanced", "-l", help="Last rebalance date (YYYY-MM-DD)")
    parser.add_argument("--threshold", "-t", type=float, default=0.05,
                       help="Drift threshold (default 0.05 = 5%)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Parse holdings
    holdings = {}
    for item in args.holdings.split(","):
        if ":" in item:
            ticker, weight = item.split(":")
            holdings[ticker.strip().upper()] = float(weight)
        else:
            # Equal weight if not specified
            tickers = [t.strip().upper() for t in args.holdings.split(",")]
            holdings = {t: 1.0/len(tickers) for t in tickers}
    
    monitor = RebalancingMonitor(drift_threshold=args.threshold)
    
    try:
        health = monitor.check_portfolio(holdings, args.last_rebalanced)
        
        if args.json:
            result = {
                "health_score": health.health_score,
                "days_since_rebalance": health.days_since_rebalance,
                "total_drift": health.total_drift,
                "alerts": [
                    {
                        "ticker": a.ticker,
                        "current_weight": a.current_weight,
                        "target_weight": a.target_weight,
                        "drift": a.drift,
                        "action": a.action,
                        "urgency": a.urgency
                    }
                    for a in health.alerts
                ],
                "recommendations": health.recommendations
            }
            print(json.dumps(result, indent=2))
        else:
            print(format_rebalance_report(health))
            
            # Also print schedule
            schedule = monitor.schedule_rebalance(health)
            if schedule["immediate_actions"]:
                print("\n🚨 Immediate Actions Required:")
                for action in schedule["immediate_actions"]:
                    print(f"   {action['action']} {action['ticker']} to {action['target_weight']:.1%}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()