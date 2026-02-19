"""
📊 Financial Health Visualization
Generate charts for financial analysis
"""

import os
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class ChartConfig:
    """Configuration for chart generation"""
    width: int = 800
    height: int = 600
    output_dir: str = "."


class FinancialVisualizer:
    """Generate visualization charts for financial analysis"""
    
    def __init__(self, config: Optional[ChartConfig] = None):
        self.config = config or ChartConfig()
        self.charts_generated = []
    
    def generate_ascii_health_dashboard(self, ticker: str, financials: Dict) -> str:
        """Generate ASCII art financial health dashboard"""
        lines = []
        lines.append(f"\n{'='*70}")
        lines.append(f"📊 FINANCIAL HEALTH DASHBOARD: {ticker}")
        lines.append(f"{'='*70}\n")
        
        # Health Score Gauge
        health_score = financials.get('financial_health_score', 50)
        lines.append(self._create_gauge("Financial Health", health_score, 100))
        
        # Innovation Score Gauge
        innovation_score = financials.get('innovation_score', 50)
        lines.append(self._create_gauge("Innovation Score", innovation_score, 100))
        
        lines.append(f"\n{'─'*70}\n")
        
        # Profitability Section
        lines.append("💰 PROFITABILITY:")
        op_margin = financials.get('operating_margin')
        if op_margin is not None:
            lines.append(self._create_bar("Operating Margin", op_margin, 50, "%"))
        
        gross_margin = financials.get('gross_margin')
        if gross_margin is not None:
            lines.append(self._create_bar("Gross Margin", gross_margin, 80, "%"))
        
        roe = financials.get('return_on_equity')
        if roe is not None:
            lines.append(self._create_bar("ROE", roe, 50, "%"))
        
        lines.append(f"\n{'─'*70}\n")
        
        # Debt Section
        lines.append("⚖️  DEBT & LEVERAGE:")
        debt_to_equity = financials.get('debt_to_equity')
        if debt_to_equity is not None:
            lines.append(self._create_bar("Debt/Equity", debt_to_equity, 3, "x", reverse=True))
        
        current_ratio = financials.get('current_ratio')
        if current_ratio is not None:
            lines.append(self._create_bar("Current Ratio", current_ratio, 3, "x"))
        
        lines.append(f"\n{'─'*70}\n")
        
        # Cash Flow Section
        lines.append("💵 CASH FLOW:")
        fcf = financials.get('free_cash_flow')
        if fcf is not None:
            lines.append(f"  Free Cash Flow: ${fcf:,.0f}M {'✅' if fcf > 0 else '❌'}")
        
        cash = financials.get('cash')
        if cash is not None:
            lines.append(f"  Cash Position: ${cash:,.0f}M")
        
        lines.append(f"\n{'─'*70}\n")
        
        # Innovation Section
        lines.append("🔬 INNOVATION INVESTMENT:")
        rd_ratio = financials.get('rd_to_revenue')
        if rd_ratio is not None:
            lines.append(self._create_bar("R&D / Revenue", rd_ratio, 25, "%"))
        
        capex_ratio = financials.get('capex_to_revenue')
        if capex_ratio is not None:
            lines.append(self._create_bar("CapEx / Revenue", capex_ratio, 20, "%"))
        
        rd_expense = financials.get('rd_expense')
        if rd_expense is not None:
            lines.append(f"  R&D Expense: ${rd_expense:,.0f}M")
        
        lines.append(f"\n{'='*70}\n")
        
        return "\n".join(lines)
    
    def _create_gauge(self, label: str, value: float, max_val: float) -> str:
        """Create ASCII gauge"""
        percentage = min(100, max(0, (value / max_val) * 100))
        filled = int(percentage / 5)  # 20 segments
        empty = 20 - filled
        
        # Color coding
        if percentage >= 70:
            emoji = "🟢"
        elif percentage >= 50:
            emoji = "🟡"
        else:
            emoji = "🔴"
        
        bar = "█" * filled + "░" * empty
        return f"  {emoji} {label:20s} [{bar}] {value:.0f}/{max_val:.0f}"
    
    def _create_bar(self, label: str, value: float, max_val: float, unit: str = "", reverse: bool = False) -> str:
        """Create ASCII horizontal bar"""
        if reverse:
            # For metrics where lower is better (like debt)
            percentage = min(100, max(0, 100 - (value / max_val) * 100))
        else:
            percentage = min(100, max(0, (value / max_val) * 100))
        
        filled = int(percentage / 4)  # 25 segments
        empty = 25 - filled
        
        # Color coding
        if reverse:
            # For reverse metrics (debt), green is low
            if percentage >= 70:
                emoji = "🟢"
            elif percentage >= 40:
                emoji = "🟡"
            else:
                emoji = "🔴"
        else:
            # Normal metrics
            if percentage >= 70:
                emoji = "🟢"
            elif percentage >= 40:
                emoji = "🟡"
            else:
                emoji = "🔴"
        
        bar = "█" * filled + "░" * empty
        return f"  {emoji} {label:20s} [{bar}] {value:.1f}{unit}"
    
    def generate_comparison_table(self, tickers: Dict[str, Dict]) -> str:
        """Generate side-by-side comparison table"""
        lines = []
        lines.append(f"\n{'='*100}")
        lines.append(f"📊 MULTI-STOCK FINANCIAL COMPARISON")
        lines.append(f"{'='*100}\n")
        
        # Header
        header = f"{'Metric':<25}"
        for ticker in tickers.keys():
            header += f"{ticker:>15}"
        lines.append(header)
        lines.append("─" * 100)
        
        # Metrics to compare
        metrics = [
            ("Health Score", "financial_health_score", "", 0),
            ("Innovation Score", "innovation_score", "", 0),
            ("Operating Margin", "operating_margin", "%", 1),
            ("ROE", "return_on_equity", "%", 1),
            ("Debt/Equity", "debt_to_equity", "x", 2),
            ("Current Ratio", "current_ratio", "x", 2),
            ("FCF ($M)", "free_cash_flow", "", 0),
            ("R&D/Revenue", "rd_to_revenue", "%", 1),
            ("CapEx/Revenue", "capex_to_revenue", "%", 1),
        ]
        
        for label, key, unit, decimals in metrics:
            row = f"{label:<25}"
            for ticker, data in tickers.items():
                value = data.get(key)
                if value is not None:
                    if decimals == 0:
                        row += f"{value:>14.0f}{unit}"
                    elif decimals == 1:
                        row += f"{value:>14.1f}{unit}"
                    else:
                        row += f"{value:>14.2f}{unit}"
                else:
                    row += f"{'N/A':>15}"
            lines.append(row)
        
        lines.append(f"\n{'='*100}\n")
        return "\n".join(lines)
    
    def generate_radar_summary(self, ticker: str, financials: Dict) -> str:
        """Generate text-based radar chart summary"""
        lines = []
        lines.append(f"\n{'='*70}")
        lines.append(f"🎯 FINANCIAL PROFILE RADAR: {ticker}")
        lines.append(f"{'='*70}\n")
        
        dimensions = [
            ("💰 Profitability", "operating_margin", 30, False),
            ("📊 Efficiency", "return_on_equity", 40, False),
            ("⚖️  Low Leverage", "debt_to_equity", 2, True),
            ("💵 Cash Generation", "free_cash_flow", 10000, False),
            ("🔬 Innovation", "rd_to_revenue", 20, False),
            ("📈 Growth", "revenue_growth_yoy", 30, False),
        ]
        
        for label, key, benchmark, reverse in dimensions:
            value = financials.get(key, 0) or 0
            if reverse:
                # Lower is better
                score = min(100, max(0, 100 - (value / benchmark) * 100))
            else:
                score = min(100, (value / benchmark) * 100)
            
            filled = int(score / 10)
            empty = 10 - filled
            
            if score >= 70:
                emoji = "🟢"
            elif score >= 40:
                emoji = "🟡"
            else:
                emoji = "🔴"
            
            stars = "★" * filled + "☆" * empty
            lines.append(f"  {emoji} {label:18s} {stars} {score:.0f}/100")
        
        lines.append(f"\n{'='*70}\n")
        return "\n".join(lines)


def format_financial_summary(ticker: str, financials: Dict) -> str:
    """Quick formatted summary of key financial metrics"""
    lines = []
    lines.append(f"\n  📈 Key Financial Metrics for {ticker}:")
    lines.append(f"  {'─'*50}")
    
    # Health indicators
    health = financials.get('financial_health_score', 50)
    innovation = financials.get('innovation_score', 50)
    
    health_emoji = "🟢" if health >= 70 else "🟡" if health >= 50 else "🔴"
    innov_emoji = "🟢" if innovation >= 70 else "🟡" if innovation >= 50 else "🔴"
    
    lines.append(f"  {health_emoji} Financial Health: {health}/100")
    lines.append(f"  {innov_emoji} Innovation Score: {innovation}/100")
    lines.append("")
    
    # Key metrics
    op_margin = financials.get('operating_margin')
    if op_margin:
        lines.append(f"  💵 Operating Margin: {op_margin:.1f}%")
    
    debt = financials.get('debt_to_equity')
    if debt:
        debt_emoji = "✅" if debt < 0.5 else "⚠️" if debt < 1.5 else "❌"
        lines.append(f"  {debt_emoji} Debt/Equity: {debt:.2f}x")
    
    roe = financials.get('return_on_equity')
    if roe:
        lines.append(f"  📊 ROE: {roe:.1f}%")
    
    fcf = financials.get('free_cash_flow')
    if fcf:
        fcf_emoji = "✅" if fcf > 0 else "❌"
        lines.append(f"  {fcf_emoji} Free Cash Flow: ${fcf:,.0f}M")
    
    rd = financials.get('rd_to_revenue')
    if rd:
        lines.append(f"  🔬 R&D: {rd:.1f}% of revenue")
    
    lines.append(f"  {'─'*50}\n")
    
    return "\n".join(lines)
