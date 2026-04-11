#!/usr/bin/env python3
"""
George Soros 思维框架蒸馏 - 女娲版

核心理念：反身性理论 + 宏观押注 +  Reflexivity

心智模型：
1. 反身性（Reflexivity）- 市场参与者的偏见会影响基本面
2. 自我强化趋势（Self-Reinforcing Trends）- 趋势一旦开始会加速
3. 均衡谬误（Equilibrium Fallacy）- 市场经常错误而非正确
4. 顶部和底部识别（Peak/Bottom Identification）- 大机会在于识别极端
5. 哲学投资（Philosophical Investing）- 投资要有宏观视野

核心投资原则：
1. "市场总是错的" - 定价经常偏离基本面
2. "趋势会自我强化" - 确认趋势时要加仓
3. "知道什么时候认输" - 趋势破坏时果断退出
4. "大机会来临时要下重注" - 高置信度 + 大机会 = 重仓
5. "理解反身性" - 价格影响预期，预期影响价格

决策启发式：
1. 首先问：这个市场/资产的错误定价是什么？
2. 趋势是否正在形成？什么会加速/破坏它？
3. 我的假设错了会怎样？最大损失是多少？
4. 这是"不得不"的机会吗？（once-in-a-decade）

反模式（Soros 绝对不会做的事）：
- 不会在趋势破坏后坚持
- 不会忽视基本面和价格的相互作用
- 不会太分散（他的旗舰基金是单一宏观策略）
- 不会在不确定时小仓位试水（不确定就完全不做）
- 不会忽视心理因素

诚实边界：
- 宏观押注需要大资金
- 需要极强的心理承受能力
- 需要全球政治经济洞察
- 失败时损失可能巨大
"""

from typing import Dict, List

class GeorgeSorosDistilled:
    """
    蒸馏后的 George Soros 思维框架
    """
    
    def __init__(self):
        self.name = "George Soros"
        self.philosophy = "Reflexivity + Macro Bets + Trend Recognition"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "reflexivity_score": 0,
            "trend_assessment": "unknown",
            "reasoning": [],
            "key_insights": [],
            "max_loss_tolerance": "10%"
        }
        
        # 评估反身性
        reflexivity = self._assess_reflexivity(data)
        result["reflexivity_score"] = reflexivity
        
        # 评估趋势
        trend = self._assess_trend(data)
        result["trend_assessment"] = trend
        
        # 评估错误定价
        mispricing = self._assess_mispricing(data)
        
        # 综合评分
        total_score = (
            reflexivity * 0.35 +
            trend["strength"] * 0.35 +
            mispricing * 0.30
        )
        
        # 生成信号
        if total_score >= 70:
            result["signal"] = "bullish" if trend["direction"] == "up" else "bearish"
            result["confidence"] = min(95, total_score)
        elif total_score <= 35:
            result["signal"] = "neutral"
            result["confidence"] = max(20, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        result["key_insights"] = self._generate_insights(data, reflexivity, trend)
        
        return result
    
    def _assess_reflexivity(self, data: Dict) -> float:
        """
        评估反身性程度
        反身性 = 价格影响预期，预期影响基本面
        """
        score = 50
        
        # 高负债公司往往有强反身性
        debt_equity = data.get("debt_to_equity", 0.5)
        if debt_equity > 2.0:
            score += 20
        elif debt_equity > 1.0:
            score += 10
        
        # 预期与实际差距大时有反身性
        analyst_expectation = data.get("analyst_consensus", 0)
        actual_earnings = data.get("actual_earnings_surprise", 0)
        if abs(analyst_expectation - actual_earnings) > 0.2:
            score += 15
        
        # 股价与基本面严重背离
        price_fundamental_gap = data.get("price_vs_fair_value_pct", 0)
        if abs(price_fundamental_gap) > 0.30:
            score += 20
        
        # 杠杆收购（LBO）有强反身性
        if data.get("is_levered_buyout", False):
            score += 15
        
        return max(15, min(95, score))
    
    def _assess_trend(self, data: Dict) -> Dict:
        """评估趋势状态"""
        trend = {
            "direction": "neutral",
            "strength": 0,
            "self_reinforcing": False,
            "break_point": None
        }
        
        # 趋势强度
        momentum_3m = data.get("momentum_3m", 0)
        momentum_12m = data.get("momentum_12m", 0)
        
        if momentum_3m > 0.15 and momentum_12m > 0.30:
            trend["direction"] = "up"
            trend["strength"] = 80
            trend["self_reinforcing"] = True
        elif momentum_3m < -0.15 and momentum_12m < -0.30:
            trend["direction"] = "down"
            trend["strength"] = 80
            trend["self_reinforcing"] = True
        elif momentum_3m > 0:
            trend["direction"] = "up"
            trend["strength"] = 50
        elif momentum_3m < 0:
            trend["direction"] = "down"
            trend["strength"] = 50
        
        # 识别可能的转折点
        if data.get("currency_pegged", False) and data.get(" Reserves_depleting", False):
            trend["break_point"] = "Currency devaluation risk"
        elif data.get("debt_cyle", "late") == "late":
            trend["break_point"] = "Debt cycle peak"
        
        return trend
    
    def _assess_mispricing(self, data: Dict) -> float:
        """评估错误定价程度"""
        score = 50
        
        # P/E vs 历史平均
        current_pe = data.get("pe_ratio", 20)
        historical_pe = data.get("historian_pe", 18)
        
        if current_pe > 0 and historical_pe > 0:
            pe_discount = (current_pe - historical_pe) / historical_pe
            if abs(pe_discount) > 0.4:
                score += 25
            elif abs(pe_discount) > 0.25:
                score += 15
        
        # 账面价值 vs 市场价值
        if data.get("price_to_book", 1) < 0.8:
            score += 20  # 严重低于账面价值
        elif data.get("price_to_book", 1) > 3:
            score -= 15  # 严重高于账面价值
        
        # 资产出售 vs 市值
        sum_of_parts_discount = data.get("sum_of_parts_discount", 0)
        if sum_of_parts_discount > 0.4:
            score += 25
        
        return max(15, min(95, score))
    
    def _generate_insights(self, data: Dict, reflexivity: float, trend: Dict) -> List[str]:
        """生成 Soros 风格的洞察"""
        insights = []
        
        if reflexivity > 70:
            insights.append("High reflexivity - price is influencing fundamentals")
        
        if trend["self_reinforcing"]:
            insights.append(f"Trend is self-reinforcing: {trend['direction']}")
        
        if trend["break_point"]:
            insights.append(f"Watch for break point: {trend['break_point']}")
        
        # Soros 会关注的特殊信号
        if data.get("consensus_positioning", "neutral") == "crowded":
            insights.append("Crowded trade - potential for sharp reversal")
        
        if data.get("central_bank_policies_changing", False):
            insights.append("Central bank policy shift - major reflexivity event")
        
        return insights
    
    def get_max_loss_tolerance(self, conviction: float) -> str:
        """Soros 的最大损失容忍度"""
        if conviction >= 80:
            return "Up to 20% on individual macro bet"
        elif conviction >= 60:
            return "Up to 10% on individual macro bet"
        else:
            return "Max 5% - only take if very high conviction"


def create_soros_agent() -> GeorgeSorosDistilled:
    return GeorgeSorosDistilled()
