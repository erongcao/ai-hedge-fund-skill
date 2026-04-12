#!/usr/bin/env python3
"""
Circle of Competence 检测框架

核心理念：每位投资大师都有自己的能力圈边界。
当分析超出能力圈的问题时，应该诚实拒绝，而不是强行回答。
"""

from typing import Dict, List, Tuple
from enum import Enum

class CompetenceLevel(Enum):
    """能力圈等级"""
    EXPERT = "expert"           # 核心能力圈，高置信度
    COMPETENT = "competent"     # 能理解，但不是专家
    OUTSIDE = "outside"         # 能力圈外，应该拒绝

class CircleOfCompetence:
    """
    能力圈检测器
    
    每位大师的 ability_circle 定义：
    - expert_sectors: 核心能力圈行业
    - expert_asset_types: 擅长的资产类型
    - expert_geographies: 熟悉的地域
    - avoid_sectors: 明确回避的行业
    - avoid_patterns: 回避的投资模式
    """
    
    def __init__(self, master_name: str, config: Dict):
        self.master_name = master_name
        self.config = config
        
    def check(self, data: Dict) -> Tuple[CompetenceLevel, str, float]:
        """
        检查是否在能力圈内
        
        Returns:
            (level, reason, confidence_adjustment)
            confidence_adjustment: 能力圈外时的置信度调整（通常大幅降低）
        """
        sector = data.get("sector", "")
        industry = data.get("industry", "")
        asset_type = data.get("asset_type", "stock")  # stock, crypto, bond, etc.
        geography = data.get("geography", "US")
        
        # 1. 检查是否在 expert_sectors 中
        expert_sectors = self.config.get("expert_sectors", [])
        if sector in expert_sectors or industry in expert_sectors:
            return CompetenceLevel.EXPERT, f"Within {self.master_name}'s core circle of competence", 1.0
        
        # 2. 检查是否在 avoid_sectors 中
        avoid_sectors = self.config.get("avoid_sectors", [])
        if sector in avoid_sectors or industry in avoid_sectors:
            return CompetenceLevel.OUTSIDE, \
                   f"{self.master_name} explicitly avoids {sector} - outside circle of competence", \
                   0.3
        
        # 3. 检查资产类型
        expert_assets = self.config.get("expert_asset_types", ["stock"])
        if asset_type not in expert_assets:
            return CompetenceLevel.OUTSIDE, \
                   f"{self.master_name} does not invest in {asset_type} - outside circle of competence", \
                   0.3
        
        # 4. 检查地域
        expert_geos = self.config.get("expert_geographies", ["US", "Global"])
        if geography not in expert_geos and "Global" not in expert_geos:
            return CompetenceLevel.COMPETENT, \
                   f"{geography} may be outside {self.master_name}'s primary focus", \
                   0.7
        
        # 5. 默认可理解，但不是核心能力圈
        return CompetenceLevel.COMPETENT, \
               f"{sector} is within {self.master_name}'s circle of competence but not core expertise", \
               0.85


# ==================== 22位大师的能力圈配置 ====================

MASTER_CIRCLES = {
    # ===== 经典价值投资大师 =====
    "Warren Buffett": {
        "expert_sectors": [
            "Consumer Defensive", "Consumer Cyclical", "Financial Services",
            "Insurance", "Banking", "Beverages", "Retail"
        ],
        "expert_asset_types": ["stock"],
        "expert_geographies": ["US"],
        "avoid_sectors": [
            "Technology",  # 直到晚年才投资苹果
            "Biotechnology",
            "Cryptocurrency"
        ],
        "avoid_patterns": ["IPOs", "high_growth_no_profit"],
        "notes": "Circle expanded late in career to include Apple, but still avoids most tech"
    },
    
    "Ben Graham": {
        "expert_sectors": [
            "Industrial", "Manufacturing", "Railroads", "Utilities", "Financial Services"
        ],
        "expert_asset_types": ["stock", "bond"],
        "expert_geographies": ["US"],
        "avoid_sectors": [
            "Technology",  # Graham died before tech became mainstream
            "Speculative Growth"
        ],
        "avoid_patterns": ["growth_at_any_price", "story_stocks"],
        "notes": "Classic net-net investor, prefers tangible assets"
    },
    
    "Cathie Wood": {
        "expert_sectors": [
            "Technology", "Healthcare", "Biotechnology", "Fintech", "AI"
        ],
        "expert_asset_types": ["stock"],
        "expert_geographies": ["US", "Global"],
        "avoid_sectors": [
            "Traditional Banking", "Legacy Retail"
        ],
        "avoid_patterns": ["value_traps", "low_growth_dividend_stocks"],
        "notes": "Focused on disruptive innovation, comfortable with unprofitable growth"
    },
    
    # ===== 宏观/对冲大师 =====
    "Ray Dalio": {
        "expert_sectors": [
            "Macro", "Multi-Asset", "Fixed Income", "Commodities", "Currencies"
        ],
        "expert_asset_types": ["stock", "bond", "commodity", "currency"],
        "expert_geographies": ["Global", "US", "China"],
        "avoid_sectors": [],
        "avoid_patterns": ["concentrated_single_stock", "unhedged_positions"],
        "notes": "All-weather approach, diversifies across economic environments"
    },
    
    "George Soros": {
        "expert_sectors": [
            "Macro", "Currencies", "Fixed Income", "Emerging Markets"
        ],
        "expert_asset_types": ["currency", "bond", "stock", "commodity"],
        "expert_geographies": ["Global", "UK", "Asia", "Emerging Markets"],
        "avoid_sectors": [],
        "avoid_patterns": ["buy_and_hold_forever", "ignoring_macro_regime"],
        "notes": "Reflexivity theory, comfortable with any asset class"
    },
    
    "Stanley Druckenmiller": {
        "expert_sectors": [
            "Macro", "Technology", "Currencies", "Commodities"
        ],
        "expert_asset_types": ["stock", "currency", "commodity", "bond"],
        "expert_geographies": ["Global", "US"],
        "avoid_sectors": [],
        "avoid_patterns": ["holding_losers", "ignoring_liquidity"],
        "notes": "Flexible macro trader, can invest anywhere"
    },
    
    # ===== 维权/事件驱动大师 =====
    "Bill Ackman": {
        "expert_sectors": [
            "Consumer", "Restaurant", "Retail", "Real Estate", "Healthcare"
        ],
        "expert_asset_types": ["stock"],
        "expert_geographies": ["US"],
        "avoid_sectors": [
            "Technology",  # Limited tech investments
            "Cryptocurrency"
        ],
        "avoid_patterns": ["passive_indexing", "small_caps"],
        "notes": "Activist investor, needs to influence management"
    },
    
    "Carl Icahn": {
        "expert_sectors": [
            "Industrial", "Energy", "Technology", "Pharmaceuticals", "Real Estate"
        ],
        "expert_asset_types": ["stock"],
        "expert_geographies": ["US"],
        "avoid_sectors": [],
        "avoid_patterns": ["management_friendly_boards", "illiquid_positions"],
        "notes": "Aggressive activist, targets companies with poor governance"
    },
    
    "Daniel Loeb": {
        "expert_sectors": [
            "Technology", "Consumer", "Financials", "Healthcare"
        ],
        "expert_asset_types": ["stock"],
        "expert_geographies": ["US", "Japan"],
        "avoid_sectors": [],
        "avoid_patterns": ["entrenched_management", "poor_capital_allocation"],
        "notes": "Activist with strong operational focus"
    },
    
    # ===== 量化大师 =====
    "Jim Simons": {
        "expert_sectors": [
            "Quantitative", "Multi-Asset", "Market Neutral"
        ],
        "expert_asset_types": ["stock", "bond", "commodity", "currency", "derivative"],
        "expert_geographies": ["Global"],
        "avoid_sectors": [],
        "avoid_patterns": ["discretionary_trading", "fundamental_analysis"],
        "notes": "Pure quant, not limited by traditional sector definitions"
    },
    
    "Jeff Yass": {
        "expert_sectors": [
            "Options", "Volatility", "Derivatives", "Quantitative"
        ],
        "expert_asset_types": ["option", "stock"],
        "expert_geographies": ["US"],
        "avoid_sectors": [],
        "avoid_patterns": ["directional_bets_without_hedge", "unstructured_risk"],
        "notes": "Options market making and volatility arbitrage"
    },
    
    # ===== 成长股/科技股专家 =====
    "Ken Griffin": {
        "expert_sectors": [
            "Technology", "Financials", "Consumer", "Healthcare"
        ],
        "expert_asset_types": ["stock", "bond", "commodity", "currency"],
        "expert_geographies": ["Global", "US"],
        "avoid_sectors": [],
        "avoid_patterns": ["concentrated_illiquid_positions"],
        "notes": "Multi-strategy, can trade anything"
    },
    
    "Steve Cohen": {
        "expert_sectors": [
            "Technology", "Healthcare", "Consumer", "Financials"
        ],
        "expert_asset_types": ["stock", "option", "derivative"],
        "expert_geographies": ["US"],
        "avoid_sectors": [],
        "avoid_patterns": ["slow_moving_positions"],
        "notes": "Fast trader, information edge focused"
    },
    
    # ===== 价值投资/深度价值 =====
    "Mohnish Pabrai": {
        "expert_sectors": [
            "Financial Services", "Consumer", "Industrial", "Automotive"
        ],
        "expert_asset_types": ["stock"],
        "expert_geographies": ["US", "India", "Global"],
        "avoid_sectors": [
            "Technology",  # Limited tech investments
            "Biotechnology"
        ],
        "avoid_patterns": ["complex_businesses", "high_debt"],
        "notes": "Cloning strategy, follows Buffett but with smaller cap focus"
    },
    
    "David Einhorn": {
        "expert_sectors": [
            "Financials", "Technology", "Consumer", "Energy"
        ],
        "expert_asset_types": ["stock", "bond"],
        "expert_geographies": ["US"],
        "avoid_sectors": [],
        "avoid_patterns": ["momentum_trading", "unclear_accounting"],
        "notes": "Value + short seller, looks for accounting issues"
    },
    
    # ===== 期货/宏观交易员 =====
    "Richard Dennis": {
        "expert_sectors": [
            "Futures", "Commodities", "Currencies", "Indices"
        ],
        "expert_asset_types": ["future", "commodity", "currency"],
        "expert_geographies": ["Global"],
        "avoid_sectors": [
            "Individual Stocks",  # Turtle trading was on futures/commodities
            "Private Companies"
        ],
        "avoid_patterns": ["fundamental_analysis", "discretionary_override"],
        "notes": "Systematic trend following on liquid futures markets"
    },
    
    "Paul Tudor Jones": {
        "expert_sectors": [
            "Macro", "Currencies", "Commodities", "Indices"
        ],
        "expert_asset_types": ["future", "currency", "bond", "stock"],
        "expert_geographies": ["Global"],
        "avoid_sectors": [],
        "avoid_patterns": ["ignoring_risk_management", "no_stop_losses"],
        "notes": "Macro trader with strong risk management focus"
    },
    
    "Ed Seykota": {
        "expert_sectors": [
            "Futures", "Commodities", "Indices", "Currencies"
        ],
        "expert_asset_types": ["future"],
        "expert_geographies": ["Global"],
        "avoid_sectors": [
            "Individual Stocks"
        ],
        "avoid_patterns": ["override_system", "ignore_trend"],
        "notes": "Pure trend following, psychological discipline"
    },
    
    "Bruce Kovner": {
        "expert_sectors": [
            "Macro", "Currencies", "Commodities", "Bonds"
        ],
        "expert_asset_types": ["currency", "bond", "commodity", "future"],
        "expert_geographies": ["Global"],
        "avoid_sectors": [],
        "avoid_patterns": ["poor_risk_management", "emotional_trading"],
        "notes": "Macro trader combining fundamental and technical analysis"
    },
    
    "Larry Williams": {
        "expert_sectors": [
            "Futures", "Commodities", "Short-term Trading"
        ],
        "expert_asset_types": ["future"],
        "expert_geographies": ["US"],
        "avoid_sectors": [
            "Long-term Investing"
        ],
        "avoid_patterns": ["buy_and_hold", "ignoring_seasonality"],
        "notes": "Short-term futures trading, overbought/oversold focus"
    },
    
    "Jesse Livermore": {
        "expert_sectors": [
            "Stock Trading", "Market Timing", "Speculation"
        ],
        "expert_asset_types": ["stock"],
        "expert_geographies": ["US"],
        "avoid_sectors": [
            "Long-term Investing",
            "Dividend Stocks"
        ],
        "avoid_patterns": ["averaging_down", "ignoring_market_trend"],
        "notes": "Speculative trader, market timing focused"
    },
    
    "Jim Rogers": {
        "expert_sectors": [
            "Commodities", "Currencies", "Emerging Markets", "Macro"
        ],
        "expert_asset_types": ["commodity", "currency", "stock", "bond"],
        "expert_geographies": ["Global", "Asia", "China", "Commodities"],
        "avoid_sectors": [
            "US Technology"  # Generally bearish on US tech
        ],
        "avoid_patterns": ["short_term_trading", "ignoring_macro_cycles"],
        "notes": "Long-term macro investor, commodity supercycle believer"
    },
}


def get_circle_of_competence(master_name: str) -> CircleOfCompetence:
    """获取指定大师的能力圈检测器"""
    config = MASTER_CIRCLES.get(master_name, {
        "expert_sectors": [],
        "expert_asset_types": ["stock"],
        "expert_geographies": ["Global"],
        "avoid_sectors": [],
        "avoid_patterns": [],
        "notes": "No specific circle defined"
    })
    return CircleOfCompetence(master_name, config)


def check_all_masters(data: Dict) -> Dict[str, Tuple[CompetenceLevel, str, float]]:
    """
    检查所有大师对某个投资标的的能力圈等级
    
    Returns:
        {master_name: (level, reason, confidence_adjustment)}
    """
    results = {}
    for master_name in MASTER_CIRCLES.keys():
        coc = get_circle_of_competence(master_name)
        level, reason, adj = coc.check(data)
        results[master_name] = (level, reason, adj)
    return results


def get_experts_for_sector(sector: str, asset_type: str = "stock") -> List[str]:
    """获取某个行业/资产类型的专家大师"""
    experts = []
    for master_name, config in MASTER_CIRCLES.items():
        if sector in config.get("expert_sectors", []):
            if asset_type in config.get("expert_asset_types", ["stock"]):
                experts.append(master_name)
    return experts


def get_avoiders_for_sector(sector: str) -> List[str]:
    """获取明确回避某个行业的大师"""
    avoiders = []
    for master_name, config in MASTER_CIRCLES.items():
        if sector in config.get("avoid_sectors", []):
            avoiders.append(master_name)
    return avoiders


if __name__ == "__main__":
    # 测试
    test_cases = [
        {"sector": "Technology", "industry": "Software", "asset_type": "stock"},
        {"sector": "Consumer Defensive", "industry": "Beverages", "asset_type": "stock"},
        {"sector": "Cryptocurrency", "industry": "Bitcoin", "asset_type": "crypto"},
        {"sector": "Financial Services", "industry": "Insurance", "asset_type": "stock"},
    ]
    
    for test in test_cases:
        print(f"\n=== Testing: {test['sector']} / {test['asset_type']} ===")
        results = check_all_masters(test)
        
        # 显示专家
        experts = [name for name, (level, _, _) in results.items() if level == CompetenceLevel.EXPERT]
        competent = [name for name, (level, _, _) in results.items() if level == CompetenceLevel.COMPETENT]
        outside = [name for name, (level, _, _) in results.items() if level == CompetenceLevel.OUTSIDE]
        
        print(f"Experts: {experts[:5]}...")
        print(f"Competent: {competent[:5]}...")
        print(f"Outside: {outside[:5]}...")
