#!/usr/bin/env python3
"""
Bill Ackman 思维框架蒸馏 - 女娲版

核心理念：高置信度集中投资 + 催化剂驱动维权

心智模型：
1. 高置信度集中持仓（High Conviction Concentration）- 找到最好的机会，重仓下注
2. 催化剂驱动（Catalyst-Driven）- 投资要有具体的事件催化剂
3. 权益思维（Ownership Mentality）- 像企业家一样思考
4. 错误定价发现（Mispricing Discovery）- 找到市场错误定价的机会
5. 长期价值创造（Long-Term Value Creation）- 不仅仅是被动持有

决策启发式：
1. 只投你敢重仓的标的（否则仓位太小没意义）
2. 要有具体的"这会在X时间因为Y原因上涨"thesis
3. 失败的教训比成功更重要（尤其是 Valeant）
4. 等待是一种美德（可以在机会不明显时空仓）
5. 运营改善比行业β更重要

反模式（Bill Ackman 绝对不会做的事）：
- 不会撒胡椒面式分散投资
- 不会投资没有清晰thesis的标的
- 不会在下跌时盲目加仓（要基于新信息）
- 不会忽视公司治理问题
- 不会投资自己无法影响的标的

诚实边界：
- 高集中度意味着高波动性
- 需要深入研究和高参与度（不是被动持有）
- 需要有能力影响公司决策（规模门槛）
- 维权投资需要大资金（普通人难以复制）
- 单一持仓可能亏损50%以上

历史教训：
- Herbalife：做空失败，展示了高置信度也可能错
- Valeant：从巨大成功到失败，展示了不考虑商业模式的危险
- Chipotle：展示了运营改善可以创造巨大价值
"""

from typing import Dict, List
from dataclasses import dataclass

class BillAckmanDistilled:
    """
    蒸馏后的 Bill Ackman 思维框架
    """
    
    def __init__(self):
        self.name = "Bill Ackman"
        self.philosophy = "High Conviction + Catalyst-Driven + Ownership Mentality"
    
    def analyze(self, data: Dict) -> Dict:
        """
        使用 Ackman 的思维框架分析股票
        """
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "reasoning": [],
            "thesis_strength": "weak",
            "catalysts": [],
            "red_flags": [],
            "key_metrics": {}
        }
        
        # 评估 thesis 强度
        thesis_score = self._assess_thesis(data)
        result["thesis_strength"] = thesis_score
        
        # 催化剂评估
        catalysts = self._identify_catalysts(data)
        result["catalysts"] = catalysts
        
        # 护城河检查（Ackman 非常看重）
        moat_score = self._assess_moat(data)
        
        # 估值
        valuation_score = self._assess_valuation(data)
        
        # 管理层和治理
        governance_score = self._assess_governance(data)
        
        # 综合评分
        total_score = (
            thesis_score * 0.35 +
            moat_score * 0.25 +
            valuation_score * 0.20 +
            governance_score * 0.20
        )
        
        # 生成信号
        if total_score >= 75 and len(catalysts) > 0:
            result["signal"] = "bullish"
            result["confidence"] = min(90, total_score + 5)
        elif total_score <= 40:
            result["signal"] = "bearish"
            result["confidence"] = max(20, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        # 风险识别
        result["red_flags"] = self._identify_red_flags(data)
        result["key_metrics"] = {
            "thesis_score": thesis_score,
            "moat_score": moat_score,
            "valuation_score": valuation_score,
            "governance_score": governance_score,
            "catalyst_count": len(catalysts)
        }
        
        return result
    
    def _assess_thesis(self, data: Dict) -> float:
        """
        评估投资 thesis 的清晰度和强度
        
        Ackman 的 thesis 要素：
        1. 为什么这个公司被低估
        2. 催化剂是什么
        3. 时间线是什么
        4. 风险是什么
        """
        score = 50
        
        # 是否有清晰的value thesis
        has_value_thesis = data.get("has_value_thesis", False)
        has_catalyst = len(data.get("catalysts", [])) > 0
        has_timeline = data.get("has_estimated_timeline", False)
        
        if has_value_thesis:
            score += 15
        
        if has_catalyst:
            score += 15
        
        if has_timeline:
            score += 10
        
        # 自由现金流生成能力
        fcf_yield = data.get("free_cash_flow_yield", 0)
        if fcf_yield > 0.10:  # > 10% FCF yield
            score += 10
        elif fcf_yield > 0.05:
            score += 5
        
        # 业务可预测性
        business_predictability = data.get("business_predictability", 0.5)
        score += int(business_predictability * 10)
        
        return max(20, min(95, score))
    
    def _identify_catalysts(self, data: Dict) -> List[str]:
        """识别可能的催化剂"""
        catalysts = []
        
        # 潜在的催化剂类型
        potential_catalysts = [
            ("has_activist_investor", "Activist investor involvement"),
            ("has_share_repurchase", "Ongoing share buybacks"),
            ("has_dividend_increase", "Dividend growth"),
            ("has_management_change", "New management team"),
            ("has_operational_improvement", "Operational improvement opportunity"),
            ("has_asset_light_strategy", "Asset light / restructuring potential"),
            ("has_merger_speculation", "M&A speculation / spin-off potential"),
            ("has_regulatory_resolution", "Regulatory uncertainty resolution"),
        ]
        
        for key, description in potential_catalysts:
            if data.get(key, False):
                catalysts.append(description)
        
        return catalysts
    
    def _assess_moat(self, data: Dict) -> float:
        """
        评估护城河 - Ackman 非常看重长期竞争壁垒
        """
        score = 50
        
        # 市场份额和稳定性
        market_share = data.get("market_share", 0)
        if market_share > 0.30:
            score += 20
        elif market_share > 0.15:
            score += 10
        
        # 品牌实力
        brand_strength = data.get("brand_strength", 0)
        if brand_strength > 0.7:
            score += 15
        elif brand_strength > 0.5:
            score += 8
        
        # 转换成本
        switching_cost = data.get("switching_cost", 0)
        if switching_cost > 0.5:
            score += 10
        elif switching_cost > 0.3:
            score += 5
        
        # 自由现金流利润率
        fcf_margin = data.get("free_cash_flow_margin", 0)
        if fcf_margin > 0.15:
            score += 10
        elif fcf_margin > 0.10:
            score += 5
        
        return max(20, min(95, score))
    
    def _assess_valuation(self, data: Dict) -> float:
        """
        评估估值 - Ackman 倾向用 DCF 和 EV/EBITDA
        """
        score = 50
        
        # EV/EBITDA
        ev_ebitda = data.get("ev_ebitda", 0)
        if ev_ebitda > 0:
            if ev_ebitda < 8:
                score += 20
            elif ev_ebitda < 12:
                score += 10
            elif ev_ebitda > 20:
                score -= 15
        
        # 市销率（用于成长型）
        ps_ratio = data.get("price_to_sales", 0)
        if ps_ratio > 0:
            if ps_ratio < 3:
                score += 10
            elif ps_ratio > 10:
                score -= 10
        
        # FCF Yield
        fcf_yield = data.get("free_cash_flow_yield", 0)
        if fcf_yield > 0.10:
            score += 10
        elif fcf_yield < 0.03:
            score -= 10
        
        return max(15, min(85, score))
    
    def _assess_governance(self, data: Dict) -> float:
        """
        评估公司治理 - Ackman 作为维权投资者非常看重这点
        """
        score = 50
        
        # 管理层持股
        insider_ownership = data.get("insider_ownership", 0)
        if insider_ownership > 0.10:
            score += 20
        elif insider_ownership > 0.03:
            score += 10
        
        # 独立董事比例
        independent_board_pct = data.get("independent_board_pct", 0.5)
        if independent_board_pct > 0.70:
            score += 10
        
        # 过去不当行为
        has_governance_issues = data.get("has_governance_issues", False)
        if has_governance_issues:
            score = max(10, score - 25)
        
        # 资本配置历史
        has_good_capital_allocation = data.get("has_good_capital_allocation", True)
        if not has_good_capital_allocation:
            score -= 15
        
        return max(15, min(95, score))
    
    def _identify_red_flags(self, data: Dict) -> List[str]:
        """识别风险信号"""
        flags = []
        
        # 业务风险
        if data.get("has_turnaround_risk", False):
            flags.append("Business turnaround required - higher risk")
        
        if data.get("has_regulatory_risk", False):
            flags.append("Significant regulatory risk")
        
        if data.get("has_technology_disruption", False):
            flags.append("Technology disruption threat")
        
        # 财务风险
        if data.get("debt_to_ebitda", 0) > 4:
            flags.append("High leverage (D/EBITDA > 4x)")
        
        if data.get("negative_fcf", False):
            flags.append("Negative free cash flow")
        
        # 治理风险
        if data.get("has_governance_issues", False):
            flags.append("Corporate governance concerns")
        
        if data.get("insider_ownership", 0) < 0.01:
            flags.append("Minimal insider ownership - misalignment")
        
        return flags
    
    def assess_position_size(self, thesis_strength: float, risk: float) -> Dict:
        """
        Ackman 的仓位管理：thesis越强，仓位越大
        """
        recommended_pct = min(10, max(1, thesis_strength * risk))
        
        return {
            "recommended_allocation": f"{recommended_pct:.1f}%",
            "rationale": f"Thesis strength {thesis_strength:.0f}/100, Risk factor {risk:.1f}",
            "max_concentration_typical": "5-10% for high conviction bets"
        }


# 导出
def create_ackman_agent() -> BillAckmanDistilled:
    return BillAckmanDistilled()
