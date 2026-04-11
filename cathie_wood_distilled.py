#!/usr/bin/env python3
"""
Cathie Wood 思维框架蒸馏 - 女娲版

核心理念：颠覆性创新 + 长期成长 + 成长股投资

心智模型：
1. 颠覆性创新（Disruptive Innovation）- 寻找改变世界的公司
2. 长期视野（Long-Term Vision）- 不在乎短期波动
3. 结构性增长（Structural Growth）- 行业趋势而非周期
4. 主动错误（Active Mistakes）- 错误是学习机会
5. 专注少数主题（Thematic Focus）- 不分散于无关领域

核心投资原则：
1. "我们投资于能够改变世界的公司"
2. "创新是唯一真正的护城河"
3. "不在乎季度盈利，在乎5年后的潜力"
4. "高风险高回报，但我们管理风险"
5. "如果你的论文没变，下跌是买入机会"

决策启发式：
1. 这家公司有10倍的潜力吗？
2. 创新是在加速还是减速？
3. 市场是否低估了长期潜力？
4. 管理层有执行力吗？
5. 价格合理吗（相对于5年后的潜力）？

反模式（Cathie Wood 绝对不会做的事）：
- 不会买没有真正创新的公司
- 不会买依赖宏观经济周期的公司
- 不会在论文变坏后坚持
- 不会买估值已经充分反映未来的股票
- 不会分散到不相关的领域

诚实边界：
- 成长股波动性极高
- 高估值容易被利率上升打击
- 需要承受短期大幅亏损
- 不是每笔投资都会成功
- 2022-2023年的教训：不是所有创新都抗通胀
"""

from typing import Dict, List

class CathieWoodDistilled:
    """
    蒸馏后的 Cathie Wood (ARK Invest) 思维框架
    """
    
    def __init__(self):
        self.name = "Cathie Wood"
        self.philosophy = "Disruptive Innovation + Long-Term Growth + Thematic Investing"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "innovation_score": 0,
            "growth_potential": "unknown",
            "reasoning": [],
            "key_metrics": {}
        }
        
        # 评估创新度
        innovation = self._assess_innovation(data)
        result["innovation_score"] = innovation
        
        # 评估成长潜力
        growth = self._assess_growth_potential(data)
        result["growth_potential"] = growth
        
        # 评估估值（相对于5年潜力）
        valuation_score = self._assess_future_valuation(data)
        
        # 综合评分
        total_score = (
            innovation * 0.40 +
            growth["score"] * 0.35 +
            valuation_score * 0.25
        )
        
        if total_score >= 70:
            result["signal"] = "bullish"
        elif total_score <= 40:
            result["signal"] = "bearish"
        else:
            result["signal"] = "neutral"
        
        result["confidence"] = total_score
        result["key_metrics"] = {
            "innovation_score": innovation,
            "5yr_cagr_target": growth.get("cagr_target", "unknown"),
            "market_opportunity": growth.get("tam_expansion", "unknown"),
            "current_valuation_vs_5yr": valuation_score
        }
        
        return result
    
    def _assess_innovation(self, data: Dict) -> float:
        """
        评估创新程度
        Wood 寻找的是能改变世界的创新
        """
        score = 50
        
        # 创新类型
        innovation_types = data.get("innovation_types", [])
        
        # 优先的创新领域
        high_priority = ["ai", "robotics", "genomics", "blockchain", "energy_storage"]
        medium_priority = ["cloud", "saas", "ecommerce", "fintech"]
        
        for inn in innovation_types:
            if inn.lower() in high_priority:
                score += 20
            elif inn.lower() in medium_priority:
                score += 10
        
        # 研发占比
        rd_intensity = data.get("rd_to_revenue", 0.10)
        if rd_intensity > 0.20:
            score += 15
        elif rd_intensity > 0.10:
            score += 10
        
        # 技术领先程度
        tech_lead = data.get("technological_lead", 0.5)
        score += int(tech_lead * 15)
        
        # 专利组合
        if data.get("strong_patent_portfolio", False):
            score += 10
        
        return max(15, min(95, score))
    
    def _assess_growth_potential(self, data: Dict) -> Dict:
        """
        评估5年成长潜力
        """
        growth = {
            "score": 50,
            "cagr_target": "unknown",
            "tam_expansion": "unknown"
        }
        
        # 目标市场规模和增长
        tam = data.get("total_addressable_market", 0)
        tam_growth = data.get("tam_growth_rate", 0.10)
        
        if tam > 100e9 and tam_growth > 0.20:
            growth["score"] += 25
        elif tam > 10e9 and tam_growth > 0.15:
            growth["score"] += 15
        
        # 5年CAGR估算
        cagr_5y = data.get("estimated_5y_revenue_cagr", 0.20)
        growth["cagr_target"] = f"{cagr_5y:.0%}"
        
        if cagr_5y > 0.40:
            growth["score"] += 25
        elif cagr_5y > 0.25:
            growth["score"] += 15
        elif cagr_5y < 0.10:
            growth["score"] -= 15
        
        # 市场渗透率
        penetration = data.get("current_market_penetration", 0.05)
        if 0.01 < penetration < 0.30:
            growth["score"] += 15  # 有大量增长空间
        elif penetration > 0.50:
            growth["score"] -= 10  # 增长空间有限
        
        growth["tam_expansion"] = f"${tam/1e9:.0f}B TAM growing at {tam_growth:.0%}"
        
        return {
            "score": max(15, min(95, growth["score"])),
            "cagr_target": growth["cagr_target"],
            "tam_expansion": growth["tam_expansion"]
        }
    
    def _assess_future_valuation(self, data: Dict) -> float:
        """
        评估相对于5年潜力的当前估值
        Wood 用 5-year discounted cash flow
        """
        score = 50
        
        # 当前P/S
        ps = data.get("price_to_sales", 10)
        # 高增长股票用P/S更合适
        
        if ps < 5:
            score += 20  # 相对便宜
        elif ps < 10:
            score += 10
        elif ps > 20:
            score -= 20  # 昂贵
        
        # 相对于成长的P/S
        cagr = data.get("estimated_5y_revenue_cagr", 0.20)
        expected_ps_5y = data.get("price_to_sales_5y_estimate", 5)
        
        # 如果5年后P/S还能维持高价，需要超高增长
        if ps > 15 and cagr < 0.30:
            score -= 20
        
        # 市值/目标市场
        market_cap = data.get("market_cap", 0)
        tam = data.get("total_addressable_market", 1e9)
        if market_cap < tam * 0.3:
            score += 15  # 潜在空间大
        elif market_cap > tam:
            score -= 25  # 已经超过TAM
        
        return max(15, min(95, score))
    
    def get_innovation_themes(self) -> List[str]:
        """
        ARK 专注的创新主题
        """
        return [
            "Artificial Intelligence",
            "Robotics & Automation", 
            "Genomics & Biotechnology",
            "Blockchain & Financial Tech",
            "Energy Storage & Renewable Energy"
        ]


def create_cathie_wood_agent() -> CathieWoodDistilled:
    return CathieWoodDistilled()
