#!/usr/bin/env python3
"""
Mohnish Pabrai 思维框架蒸馏 - 女娲版

核心理念：价值投资 + 模仿策略 + 低摩擦

心智模型：
1. 模仿优于创新（Imitation Over Innovation）- 复制成功投资者的策略
2. 低摩擦投资（Low Friction）- 减少决策数量，提高质量
3. 安全边际至上（Margin of Safety First）- 永远要安全边际
4. 集中投资（Concentrated Bets）- 20-30个最好想法
5. 长期持有（Long-Term Holding）- 不要频繁交易

核心投资原则：
1. "最好的投资理念来自模仿"
2. "每笔投资要有50%的安全边际"
3. "不换股太频繁（年换手率<20%）"
4. "投资组合集中但有耐心"
5. "错误时要承认并卖出"

决策启发式：
1. 这笔投资有足够的安全边际吗？（价格<价值的50%）
2. 我能在5分钟内解释为什么买吗？
3. 这是我能持有10年的公司吗？
4. 如果股市关闭5年，我还愿意持有吗？
5. 下跌50%我能接受吗？

反模式（Pabrai 绝对不会做的事）：
- 不会买没有安全边际的股票
- 不会频繁交易
- 不会投资自己看不懂的业务
- 不会分散到没有意义的程度
- 不会在错误时固执

诚实边界：
- 安全边际要求限制了很多机会
- 集中持仓意味着高波动性
- 长期持有意味着流动性差
- 模仿策略可能不适合所有人
"""

from typing import Dict, List

class MohnishPabraiDistilled:
    """
    蒸馏后的 Mohnish Pabrai 思维框架
    """
    
    def __init__(self):
        self.name = "Mohnish Pabrai"
        self.philosophy = "Deep Value + Margin of Safety + Imitation Strategy"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "margin_of_safety": "insufficient",
            "reasoning": [],
            "holding_period_recommendation": "5+ years",
            "key_metrics": {}
        }
        
        # 评估安全边际
        mos = self._assess_margin_of_safety(data)
        result["margin_of_safety"] = mos
        
        # 评估是否是"10年持有"机会
        holding_score = self._assess_holding_potential(data)
        
        # 集中投资适合度
        concentration_score = self._assess_concentration_fit(data)
        
        # 综合评分
        total_score = (
            mos["score"] * 0.50 +
            holding_score * 0.30 +
            concentration_score * 0.20
        )
        
        # 生成信号
        if total_score >= 75:
            result["signal"] = "bullish"
        elif total_score <= 40:
            result["signal"] = "bearish"
        else:
            result["signal"] = "neutral"
        
        result["confidence"] = total_score
        result["key_metrics"] = {
            "margin_of_safety_pct": mos["safety_margin"],
            "upside_to_intrinsic": mos["upside_to_fair_value"],
            "downside_risk": mos["downside_risk"]
        }
        
        return result
    
    def _assess_margin_of_safety(self, data: Dict) -> Dict:
        """
        评估安全边际
        Pabrai 要求至少50%的安全边际
        """
        mos = {
            "score": 0,
            "safety_margin": 0,
            "upside_to_fair_value": 0,
            "downside_risk": 0
        }
        
        current_price = data.get("current_price", 0)
        intrinsic_value = data.get("intrinsic_value_estimate", current_price)
        
        if current_price > 0 and intrinsic_value > 0:
            mos["safety_margin"] = (intrinsic_value - current_price) / intrinsic_value
            mos["upside_to_fair_value"] = (intrinsic_value - current_price) / current_price
        
        # 下跌空间
        liquidation_value = data.get("liquidation_value_per_share", 0)
        if liquidation_value > 0 and current_price > 0:
            mos["downside_risk"] = (current_price - liquidation_value) / current_price
        
        # 评分
        safety = mos["safety_margin"]
        if safety >= 0.50:
            mos["score"] = 95
        elif safety >= 0.40:
            mos["score"] = 85
        elif safety >= 0.30:
            mos["score"] = 70
        elif safety >= 0.20:
            mos["score"] = 55
        elif safety >= 0.10:
            mos["score"] = 40
        else:
            mos["score"] = 25
        
        # 额外加分
        if data.get("net_cash_per_share", 0) > current_price * 0.2:
            mos["score"] += 10  # 大量净现金
        
        if data.get("has_absolutely_no_debt", False):
            mos["score"] += 10
        
        return mos
    
    def _assess_holding_potential(self, data: Dict) -> float:
        """评估是否适合持有10年"""
        score = 50
        
        # 业务稳定性
        business_stability = data.get("business_stability_score", 0.5)
        score += int(business_stability * 25)
        
        # 行业是否在结构性下滑
        if data.get("industry_in_decline", False):
            score -= 30
        
        # 竞争壁垒
        moat = data.get("has_economic_moat", False)
        if moat:
            score += 20
        
        # 管理层质量
        if data.get("management_quality", "average") == "excellent":
            score += 10
        
        # 资本配置历史
        if data.get("has_history_of_poor_capital_allocation", False):
            score -= 20
        
        return max(10, min(95, score))
    
    def _assess_concentration_fit(self, data: Dict) -> float:
        """
        评估是否适合集中持仓
        Pabrai 通常持有20-30个高质量标的
        """
        score = 50
        
        # 规模适中
        market_cap = data.get("market_cap", 0)
        if 1e9 < market_cap < 50e9:
            score += 20  # 中小盘最适合
        elif market_cap > 50e9:
            score += 10
        
        # 流动性
        avg_volume = data.get("avg_daily_volume", 0)
        market_cap_float = market_cap * 0.2  # 假设20%流通股
        days_to_sell = market_cap_float / avg_volume if avg_volume > 0 else 999
        
        if days_to_sell < 5:
            score += 15
        elif days_to_sell < 20:
            score += 5
        else:
            score -= 15  # 流动性差
        
        # 透明度
        if data.get("financials_transparency", "high") == "high":
            score += 10
        
        return max(15, min(90, score))
    
    def get_imitation_candidates(self) -> List[str]:
        """
        Pabrai 模仿的大师名单
        可以用来筛选类似的机会
        """
        return [
            "Warren Buffett",
            "Charlie Munger", 
            "Ben Graham",
            "Peter Lynch",
            "Seth Klarman",
            "Joel Greenblatt",
            "Monish Pabrai himself"
        ]


def create_pabrai_agent() -> MohnishPabraiDistilled:
    return MohnishPabraiDistilled()
