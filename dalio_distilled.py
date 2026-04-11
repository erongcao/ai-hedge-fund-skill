#!/usr/bin/env python3
"""
Ray Dalio 思维框架蒸馏 - 女娲版

核心理念：风险平价 + 全天候 + 去杠杆化思考

心智模型：
1. 风险平价（Risk Parity）- 分散的不是资产，而是风险
2. 全天候（All Weather）- 在任何经济环境下都能表现良好
3. 去杠杆化思考（Deleveraging）- 理解债务周期
4. 理解经济机器（Economic Machine）- 理解信贷、债务、通胀的关系
5. 相信分散化（Diversification）- 真正的分散是风险因子的分散

决策启发式：
1. 不要集中于股票，要分散于经济环境（上升/下降 × 通胀/通缩）
2. 债券和股票负相关时，债券是好的对冲
3. 黄金和商品是对冲通胀的工具
4. 用杠杆放大低波动资产（但普通人不要学）
5. 理解相关性，不是资产本身

反模式（Dalio 绝对不会做的事）：
- 不会单押一种资产或策略
- 不会忽视债务周期的影响
- 不会在高度泡沫化时追涨
- 不会忽视央行政策对市场的影响

诚实边界：
- 需要杠杆才能达到目标收益（普通人难以复制）
- 需要专业衍生品知识
- 在低利率环境下策略表现会变化
"""

from typing import Dict, List
from dataclasses import dataclass

class RayDalioDistilled:
    """
    蒸馏后的 Ray Dalio 思维框架
    """
    
    def __init__(self):
        self.name = "Ray Dalio"
        self.philosophy = "All Weather + Risk Parity + Understanding the Economic Machine"
    
    def analyze_portfolio_risk(self, data: Dict) -> Dict:
        """
        分析投资组合的风险特征
        """
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "reasoning": [],
            "risk_assessment": {},
            "environmental_sensitivity": {},
            "recommendations": []
        }
        
        # 评估组合在不同经济环境下的表现
        risk_assessment = self._assess_environmental_risk(data)
        result["risk_assessment"] = risk_assessment
        
        # 环境敏感性
        result["environmental_sensitivity"] = self._assess_sensitivity(data)
        
        # 生成信号
        if risk_assessment["is_diversified"] and risk_assessment["has_tail_hedge"]:
            result["signal"] = "bullish"
            result["confidence"] = 75
        elif not risk_assessment["is_diversified"]:
            result["signal"] = "bearish"
            result["confidence"] = 70
        
        # 建议
        result["recommendations"] = self._generate_recommendations(data, risk_assessment)
        
        return result
    
    def analyze_macro_environment(self, data: Dict) -> Dict:
        """
        分析当前宏观环境（通胀/增长）
        """
        result = {
            "agent": self.name,
            "environment": "unknown",  # growth/rising, growth/falling, contraction/rising, contraction/falling
            "best_assets": [],
            "worst_assets": [],
            "reasoning": []
        }
        
        # 判断经济环境
        inflation = data.get("inflation_trend", "neutral")  # rising/neutral/falling
        growth = data.get("growth_trend", "neutral")  # rising/neutral/falling
        
        if growth == "rising" and inflation == "falling":
            result["environment"] = "Goldilocks (Best)"
            result["best_assets"] = ["Stocks", "Corporate Bonds"]
            result["worst_assets"] = ["Long-term Bonds", "Gold"]
        elif growth == "rising" and inflation == "rising":
            result["environment"] = "Expansion + Inflation"
            result["best_assets"] = ["Commodities", "Stocks", "TIPS"]
            result["worst_assets"] = ["Long-term Bonds"]
        elif growth == "falling" and inflation == "falling":
            result["environment"] = "Disinflation (Good for Bonds)"
            result["best_assets"] = ["Long Bonds", "Stocks (defensive)"]
            result["worst_assets"] = ["Commodities"]
        elif growth == "falling" and inflation == "rising":
            result["environment"] = "Stagflation (Worst)"
            result["best_assets"] = ["Gold", "Commodities", "TIPS"]
            result["worst_assets"] = ["Stocks", "Long Bonds"]
        
        return result
    
    def _assess_environmental_risk(self, data: Dict) -> Dict:
        """评估组合在四种经济环境下的表现"""
        assessment = {
            "is_diversified": False,
            "has_tail_hedge": False,
            "risk_concentration": "high",
            "environments_covered": []
        }
        
        # 检查是否覆盖不同环境
        has_stock = data.get("stock_allocation", 0) > 0.1
        has_bond = data.get("bond_allocation", 0) > 0.1
        has_gold = data.get("gold_allocation", 0) > 0.05
        has_commodity = data.get("commodity_allocation", 0) > 0.05
        
        if has_stock:
            assessment["environments_covered"].append("growth")
        if has_bond:
            assessment["environments_covered"].append("disinflation")
        if has_gold:
            assessment["environments_covered"].append("deflation")
        if has_commodity:
            assessment["environments_covered"].append("inflation")
        
        # 分散化检查
        if len(assessment["environments_covered"]) >= 3:
            assessment["is_diversified"] = True
        
        # 尾部对冲
        if has_gold or has_bond:
            assessment["has_tail_hedge"] = True
        
        # 风险集中度
        largest_position = data.get("largest_position_pct", 1.0)
        if largest_position > 0.3:
            assessment["risk_concentration"] = "very_high"
        elif largest_position > 0.2:
            assessment["risk_concentration"] = "high"
        elif largest_position > 0.1:
            assessment["risk_concentration"] = "medium"
        else:
            assessment["risk_concentration"] = "low"
        
        return assessment
    
    def _assess_sensitivity(self, data: Dict) -> Dict:
        """评估组合对不同环境因子的敏感性"""
        return {
            "inflation_sensitivity": data.get("inflation_beta", 0),
            "growth_sensitivity": data.get("market_beta", 1.0),
            "interest_rate_sensitivity": data.get("duration", 0)
        }
    
    def _generate_recommendations(self, data: Dict, assessment: Dict) -> List[str]:
        """生成 Dalio 风格的建议"""
        recs = []
        
        if not assessment["is_diversified"]:
            recs.append("Consider diversifying across economic environments, not just asset classes")
        
        if not assessment["has_tail_hedge"]:
            recs.append("Add tail hedges (gold or long-term bonds) to protect against adverse scenarios")
        
        if assessment["risk_concentration"] in ["very_high", "high"]:
            recs.append("Reduce concentration in largest position to manage single-stock risk")
        
        # 全天候建议
        recs.append("For All Weather: ~30% stocks, ~40% long bonds, ~15% intermediate bonds, ~7.5% gold, ~7.5% commodities")
        
        return recs


# 导出
def create_dalio_agent() -> RayDalioDistilled:
    return RayDalioDistilled()
