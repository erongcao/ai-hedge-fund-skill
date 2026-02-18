#!/usr/bin/env python3
"""
AI Hedge Fund - Tax Optimization Module
Tax-loss harvesting and tax-efficient portfolio management
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ai_hedge_fund_advanced import AIHedgeFundAdvanced, DataFetcher

@dataclass
class TaxLot:
    """Individual tax lot"""
    ticker: str
    shares: float
    purchase_date: str
    purchase_price: float
    current_price: float
    cost_basis: float
    current_value: float
    unrealized_gain: float
    gain_percent: float
    is_long_term: bool
    days_held: int

@dataclass
class TaxLossOpportunity:
    """Tax loss harvesting opportunity"""
    ticker: str
    shares: float
    unrealized_loss: float
    loss_percent: float
    days_held: int
    replacement_candidates: List[str]
    wash_sale_risk: bool
    tax_savings: float
    recommendation: str

@dataclass
class TaxReport:
    """Tax optimization report"""
    short_term_gains: float
    short_term_losses: float
    long_term_gains: float
    long_term_losses: float
    net_short_term: float
    net_long_term: float
    estimated_tax_liability: float
    harvesting_opportunities: List[TaxLossOpportunity]
    total_tax_savings_potential: float
    year_end_recommendations: List[str]

class TaxOptimizer:
    """Tax optimization and loss harvesting"""
    
    def __init__(self, tax_rate_short: float = 0.35, tax_rate_long: float = 0.20):
        self.tax_rate_short = tax_rate_short  # Short-term capital gains rate
        self.tax_rate_long = tax_rate_long    # Long-term capital gains rate
        self.long_term_threshold = 365        # Days for long-term status
        self.wash_sale_window = 30            # Days to avoid wash sale
        self.data_fetcher = DataFetcher()
        self.hedge_fund = AIHedgeFundAdvanced(use_subagents=False)
    
    def analyze_tax_position(self, lots: List[Dict]) -> TaxReport:
        """
        Analyze tax position and find optimization opportunities
        
        Args:
            lots: List of tax lots with {ticker, shares, purchase_date, purchase_price}
        """
        print(f"\n💰 Analyzing tax position for {len(lots)} lots...\n", file=sys.stderr)
        
        # Enrich lots with current data
        enriched_lots = []
        for lot in lots:
            try:
                data = self.data_fetcher.get_comprehensive_data(lot['ticker'])
                current_price = data.get('current_price', lot['purchase_price'])
                
                purchase_date = datetime.strptime(lot['purchase_date'], '%Y-%m-%d')
                days_held = (datetime.now() - purchase_date).days
                
                cost_basis = lot['shares'] * lot['purchase_price']
                current_value = lot['shares'] * current_price
                unrealized_gain = current_value - cost_basis
                
                enriched_lots.append(TaxLot(
                    ticker=lot['ticker'],
                    shares=lot['shares'],
                    purchase_date=lot['purchase_date'],
                    purchase_price=lot['purchase_price'],
                    current_price=current_price,
                    cost_basis=cost_basis,
                    current_value=current_value,
                    unrealized_gain=unrealized_gain,
                    gain_percent=(unrealized_gain / cost_basis) if cost_basis > 0 else 0,
                    is_long_term=days_held >= self.long_term_threshold,
                    days_held=days_held
                ))
            except Exception as e:
                print(f"❌ Error processing {lot['ticker']}: {e}", file=sys.stderr)
        
        # Calculate gains/losses
        short_term_gains = sum(l.unrealized_gain for l in enriched_lots 
                              if not l.is_long_term and l.unrealized_gain > 0)
        short_term_losses = sum(l.unrealized_gain for l in enriched_lots 
                               if not l.is_long_term and l.unrealized_gain < 0)
        long_term_gains = sum(l.unrealized_gain for l in enriched_lots 
                             if l.is_long_term and l.unrealized_gain > 0)
        long_term_losses = sum(l.unrealized_gain for l in enriched_lots 
                              if l.is_long_term and l.unrealized_gain < 0)
        
        net_short_term = short_term_gains + short_term_losses
        net_long_term = long_term_gains + long_term_losses
        
        # Estimate tax liability
        tax_liability = (max(0, net_short_term) * self.tax_rate_short + 
                        max(0, net_long_term) * self.tax_rate_long)
        
        # Find harvesting opportunities
        opportunities = self._find_harvesting_opportunities(enriched_lots)
        
        # Calculate total tax savings potential
        total_savings = sum(o.tax_savings for o in opportunities)
        
        # Generate recommendations
        recommendations = self._generate_tax_recommendations(
            enriched_lots, opportunities, net_short_term, net_long_term
        )
        
        return TaxReport(
            short_term_gains=short_term_gains,
            short_term_losses=short_term_losses,
            long_term_gains=long_term_gains,
            long_term_losses=long_term_losses,
            net_short_term=net_short_term,
            net_long_term=net_long_term,
            estimated_tax_liability=tax_liability,
            harvesting_opportunities=opportunities,
            total_tax_savings_potential=total_savings,
            year_end_recommendations=recommendations
        )
    
    def _find_harvesting_opportunities(self, lots: List[TaxLot]) -> List[TaxLossOpportunity]:
        """Find tax loss harvesting opportunities"""
        opportunities = []
        
        loss_lots = [l for l in lots if l.unrealized_gain < 0]
        
        for lot in loss_lots:
            # Check wash sale risk
            wash_sale_risk = lot.days_held < self.wash_sale_window
            
            # Find replacement candidates
            replacements = self._find_replacements(lot.ticker)
            
            # Calculate tax savings
            tax_rate = self.tax_rate_long if lot.is_long_term else self.tax_rate_short
            tax_savings = abs(lot.unrealized_gain) * tax_rate
            
            if wash_sale_risk:
                recommendation = "WAIT - Wash sale risk. Sell after 30 days."
            else:
                recommendation = f"HARVEST - Sell and consider {replacements[0] if replacements else 'similar ETF'}"
            
            opportunities.append(TaxLossOpportunity(
                ticker=lot.ticker,
                shares=lot.shares,
                unrealized_loss=abs(lot.unrealized_gain),
                loss_percent=abs(lot.gain_percent),
                days_held=lot.days_held,
                replacement_candidates=replacements,
                wash_sale_risk=wash_sale_risk,
                tax_savings=tax_savings,
                recommendation=recommendation
            ))
        
        return sorted(opportunities, key=lambda x: x.tax_savings, reverse=True)
    
    def _find_replacements(self, ticker: str) -> List[str]:
        """Find replacement securities to avoid wash sale"""
        try:
            data = self.data_fetcher.get_comprehensive_data(ticker)
            sector = data.get('sector', '')
            
            # Sector-based replacement suggestions
            replacements = {
                'Technology': ['VGT', 'XLK', 'QQQ'],
                'Healthcare': ['VHT', 'XLV', 'IHI'],
                'Financials': ['VFH', 'XLF', 'KRE'],
                'Consumer Discretionary': ['XLY', 'VCR'],
                'Industrials': ['VIS', 'XLI'],
                'Energy': ['VDE', 'XLE'],
                'Real Estate': ['VNQ', 'XLRE'],
                'Materials': ['VAW', 'XLB'],
                'Utilities': ['VPU', 'XLU'],
                'Communication Services': ['VOX', 'XLC']
            }
            
            return replacements.get(sector, ['VTI', 'VOO', 'SPY'])  # Default to broad market
        except:
            return ['VTI', 'VOO']  # Safe defaults
    
    def _generate_tax_recommendations(self, lots: List[TaxLot], 
                                     opportunities: List[TaxLossOpportunity],
                                     net_st: float, net_lt: float) -> List[str]:
        """Generate tax recommendations"""
        recommendations = []
        
        # Loss harvesting
        if opportunities:
            total_harvestable = sum(o.unrealized_loss for o in opportunities if not o.wash_sale_risk)
            if total_harvestable > 0:
                recommendations.append(
                    f"💰 Harvest ${total_harvestable:,.0f} in losses to offset gains and save taxes"
                )
        
        # Short-term gains
        if net_st > 10000:
            recommendations.append(
                f"⚠️  High short-term gains (${net_st:,.0f}). Consider holding >1 year for lower tax rate."
            )
        
        # Year-end timing
        now = datetime.now()
        if now.month == 12:
            days_left = 31 - now.day
            recommendations.append(
                f"📅 Only {days_left} days left in tax year. Consider harvesting losses before Dec 31."
            )
        
        # Lot selection strategy
        recommendations.append(
            "💡 Use specific lot identification for optimal tax treatment when selling."
        )
        
        return recommendations
    
    def calculate_year_end_strategy(self, lots: List[Dict], 
                                    target_gains: float = 0) -> Dict:
        """Calculate optimal year-end tax strategy"""
        report = self.analyze_tax_position(lots)
        
        # Find lots to harvest
        harvest_candidates = [o for o in report.harvesting_opportunities 
                             if not o.wash_sale_risk]
        
        # Calculate optimal harvest
        current_gains = report.net_short_term + report.net_long_term
        target_loss = current_gains - target_gains
        
        selected_harvests = []
        accumulated_loss = 0
        
        for opportunity in harvest_candidates:
            if accumulated_loss >= target_loss:
                break
            selected_harvests.append(opportunity)
            accumulated_loss += opportunity.unrealized_loss
        
        return {
            "current_gains": current_gains,
            "target_gains": target_gains,
            "losses_needed": max(0, target_loss),
            "recommended_harvests": [
                {
                    "ticker": o.ticker,
                    "shares": o.shares,
                    "loss": o.unrealized_loss,
                    "replacement": o.replacement_candidates[0] if o.replacement_candidates else None
                }
                for o in selected_harvests
            ],
            "total_harvest_loss": accumulated_loss,
            "tax_savings": accumulated_loss * self.tax_rate_short,
            "wash_sale_warnings": [o.ticker for o in report.harvesting_opportunities if o.wash_sale_risk]
        }

def format_tax_report(report: TaxReport) -> str:
    """Format tax report for display"""
    lines = [
        f"\n{'='*80}",
        f"💰 Tax Optimization Report",
        f"{'='*80}",
        "",
        "📊 Current Tax Position:",
        "-" * 50,
        f"  Short-Term Gains:   ${report.short_term_gains:>12,.0f}",
        f"  Short-Term Losses:  ${report.short_term_losses:>12,.0f}",
        f"  Net Short-Term:     ${report.net_short_term:>12,.0f}",
        "",
        f"  Long-Term Gains:    ${report.long_term_gains:>12,.0f}",
        f"  Long-Term Losses:   ${report.long_term_losses:>12,.0f}",
        f"  Net Long-Term:      ${report.net_long_term:>12,.0f}",
        "",
        f"  Estimated Tax:      ${report.estimated_tax_liability:>12,.0f}",
        ""
    ]
    
    # Harvesting opportunities
    if report.harvesting_opportunities:
        lines.extend([
            "🌾 Tax Loss Harvesting Opportunities:",
            "-" * 80,
            f"{'Ticker':<10} {'Loss':<12} {'Loss %':<10} {'Days':<8} {'Tax Savings':<12} {'Action'}",
            "-" * 80
        ])
        
        for opp in report.harvesting_opportunities[:10]:
            wash_sale = "⚠️ WASH" if opp.wash_sale_risk else ""
            lines.append(
                f"{opp.ticker:<10} ${opp.unrealized_loss:>10,.0f} {opp.loss_percent:>8.1%} "
                f"{opp.days_held:>6} ${opp.tax_savings:>10,.0f} {opp.recommendation[:30]} {wash_sale}"
            )
        
        lines.append("")
        lines.append(f"💵 Total Tax Savings Potential: ${report.total_tax_savings_potential:,.0f}")
        lines.append("")
    
    # Recommendations
    if report.year_end_recommendations:
        lines.extend([
            "💡 Recommendations:",
            "-" * 50
        ])
        for rec in report.year_end_recommendations:
            lines.append(f"  {rec}")
        lines.append("")
    
    lines.append(f"{'='*80}\n")
    
    return "\n".join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Hedge Fund - Tax Optimizer")
    parser.add_argument("--lots", "-l", required=True,
                       help="Tax lots as JSON or file path")
    parser.add_argument("--year-end", "-y", action="store_true",
                       help="Generate year-end strategy")
    parser.add_argument("--target-gains", "-t", type=float, default=0,
                       help="Target gains for year-end (default 0)")
    parser.add_argument("--tax-rate-short", type=float, default=0.35,
                       help="Short-term tax rate")
    parser.add_argument("--tax-rate-long", type=float, default=0.20,
                       help="Long-term tax rate")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Parse lots
    if args.lots.endswith('.json'):
        with open(args.lots) as f:
            lots = json.load(f)
    else:
        lots = json.loads(args.lots)
    
    optimizer = TaxOptimizer(
        tax_rate_short=args.tax_rate_short,
        tax_rate_long=args.tax_rate_long
    )
    
    try:
        if args.year_end:
            strategy = optimizer.calculate_year_end_strategy(lots, args.target_gains)
            if args.json:
                print(json.dumps(strategy, indent=2))
            else:
                print("\n📅 Year-End Tax Strategy:\n")
                print(f"Current Gains: ${strategy['current_gains']:,.0f}")
                print(f"Target Gains: ${strategy['target_gains']:,.0f}")
                print(f"\nRecommended Harvests:")
                for h in strategy['recommended_harvests']:
                    print(f"  Sell {h['shares']:.2f} shares of {h['ticker']} (${h['loss']:,.0f} loss)")
                    if h['replacement']:
                        print(f"    → Buy {h['replacement']} to maintain exposure")
                print(f"\nTotal Tax Savings: ${strategy['tax_savings']:,.0f}")
        else:
            report = optimizer.analyze_tax_position(lots)
            
            if args.json:
                result = {
                    "short_term_gains": report.short_term_gains,
                    "short_term_losses": report.short_term_losses,
                    "long_term_gains": report.long_term_gains,
                    "long_term_losses": report.long_term_losses,
                    "estimated_tax": report.estimated_tax_liability,
                    "harvesting_opportunities": [
                        {
                            "ticker": o.ticker,
                            "loss": o.unrealized_loss,
                            "tax_savings": o.tax_savings,
                            "wash_sale_risk": o.wash_sale_risk
                        }
                        for o in report.harvesting_opportunities
                    ],
                    "total_savings_potential": report.total_tax_savings_potential
                }
                print(json.dumps(result, indent=2))
            else:
                print(format_tax_report(report))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()