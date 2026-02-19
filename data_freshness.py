"""
Data Freshness and Period Tracker
Ensures consistent data periods and transparency
"""

from dataclasses import dataclass, field
from typing import Optional, Dict
from datetime import datetime


@dataclass
class DataFreshness:
    """Track data freshness and time periods for all metrics"""
    
    # Report timestamp
    report_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    
    # Price data
    price_date: Optional[str] = None
    price_as_of: str = "实时"
    
    # Financial metrics periods
    roe_period: str = "TTM (过去12个月)"  # Yahoo only provides TTM
    roe_calculation_date: Optional[str] = None
    
    fcf_period: str = "TTM (过去12个月)"
    fcf_calculation_date: Optional[str] = None
    
    margin_period: str = "TTM (过去12个月)"
    
    earnings_period: str = "最近4个季度"
    latest_earnings_date: Optional[str] = None
    
    debt_period: str = "最新财报"
    
    # Analyst data
    analyst_consensus_date: Optional[str] = None
    
    # News data
    news_period: str = "近1年"
    news_last_updated: Optional[str] = None
    
    # Warnings
    data_warnings: list = field(default_factory=list)
    
    def add_warning(self, warning: str):
        """Add data consistency warning"""
        if warning not in self.data_warnings:
            self.data_warnings.append(warning)
    
    def format_freshness_report(self) -> str:
        """Format data freshness report"""
        lines = []
        lines.append("\n📅 数据时效性报告:")
        lines.append("-" * 50)
        
        lines.append(f"  报告生成时间: {self.report_date}")
        lines.append("")
        
        lines.append("  📊 财务指标周期:")
        lines.append(f"    • ROE: {self.roe_period}")
        lines.append(f"    • 自由现金流: {self.fcf_period}")
        lines.append(f"    • 利润率: {self.margin_period}")
        lines.append(f"    • 债务数据: {self.debt_period}")
        lines.append("")
        
        lines.append("  📈 财报数据:")
        lines.append(f"    • 分析周期: {self.earnings_period}")
        if self.latest_earnings_date:
            lines.append(f"    • 最新财报: {self.latest_earnings_date}")
        lines.append("")
        
        if self.data_warnings:
            lines.append("  ⚠️ 数据一致性警告:")
            for warning in self.data_warnings:
                lines.append(f"    • {warning}")
            lines.append("")
        
        lines.append("  ℹ️ 说明:")
        lines.append("    TTM = Trailing Twelve Months (过去12个月)")
        lines.append("    不同指标的TTM计算基准日可能略有差异")
        lines.append("-" * 50)
        
        return "\n".join(lines)


def validate_data_consistency(data_dict: Dict) -> DataFreshness:
    """Validate data consistency and create freshness report"""
    freshness = DataFreshness()
    
    # Check for common data inconsistency issues
    warnings = []
    
    # Check if using mixed TTM data
    if 'returnOnEquity' in data_dict and 'freeCashflow' in data_dict:
        warnings.append("ROE和FCF均为TTM数据，但计算时间点可能不同")
    
    # Check if margins are TTM
    if 'operatingMargins' in data_dict:
        warnings.append("利润率数据为TTM，反映过去12个月平均水平")
    
    # Check earnings dates if available
    if 'earningsDates' in data_dict:
        earnings_dates = data_dict['earningsDates']
        if earnings_dates and len(earnings_dates) > 0:
            latest = earnings_dates[0]
            freshness.latest_earnings_date = str(latest)[:10]
    
    for warning in warnings:
        freshness.add_warning(warning)
    
    return freshness


# Format helper for displaying metrics with perioddef format_metric_with_period(value, metric_name: str, period: str = "TTM") -> str:
    """Format metric value with its calculation period"""
    if value is None:
        return "N/A"
    
    if isinstance(value, float):
        return f"{value:.2f} ({period})"
    elif isinstance(value, int):
        return f"{value:,} ({period})"
    else:
        return f"{value} ({period})"


def get_yahoo_data_period_description(field_name: str) -> str:
    """Get description of Yahoo Finance data period for a field"""
    period_map = {
        'returnOnEquity': 'TTM (过去12个月)',
        'returnOnAssets': 'TTM (过去12个月)',
        'freeCashflow': 'TTM (过去12个月)',
        'operatingCashflow': 'TTM (过去12个月)',
        'operatingMargins': 'TTM (过去12个月)',
        'grossMargins': 'TTM (过去12个月)',
        'profitMargins': 'TTM (过去12个月)',
        'ebitdaMargins': 'TTM (过去12个月)',
        'revenueGrowth': '同比增长',
        'earningsGrowth': '同比增长',
        'trailingPE': '基于过去12个月盈利',
        'forwardPE': '基于未来12个月预测盈利',
        'currentPrice': '实时',
        'marketCap': '实时',
    }
    
    return period_map.get(field_name, '未知周期')
