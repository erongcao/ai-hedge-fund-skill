#!/usr/bin/env python3
"""
Stanley Druckenmiller 思维框架蒸馏 - 女娲版

核心理念：全球宏观交易 + 流动性驱动 + 重仓获利

心智模型：
1. 宏观主题驱动（Macro Theme-Driven）- 找到时代最大的趋势
2. 流动性驱动（Liquidity-Driven）- 流动性是市场的核心驱动力
3. 赢家通吃（Concentrated Winners）- 大钱来自少数重仓
4. 顶部保护（Top-Drotection）- 首先要不亏钱
5. 快速止损（Quick Loss Cutting）- 错误时迅速认输

核心投资原则：
1. "重要的不是你对了还是错了，而是对了赚多少，错了承受多少"
2. 找到有信仰的重仓机会
3. 保持灵活性，不固执于任何仓位
4. 在高置信度机会时下大注
5. 不要在意短期波动，要在意趋势是否还在

决策启发式：
1. 首先问：这是一个什么样的宏观环境？
2. 再问：哪个资产/市场最受益？
3. 最后问：流动性支持这个trade吗？
4. 持有：直到主题破坏或达到目标
5. 止损：市场证明你错时立刻退出

反模式（Druckenmiller 绝对不会做的事）：
- 不会在下跌中摊平成本
- 不会盲目持有亏损头寸
- 不会忽视流动性信号
- 不会为了"抄底"而逆向操作
- 不会分散到没有意义的地步

诚实边界：
- 高杠杆操作可能导致巨额亏损
- 需要强大的心理承受能力
- 需要全球宏观洞察力
- 不适合保守型投资者
"""

from typing import Dict, List

class StanleyDruckenmillerDistilled:
    """
    蒸馏后的 Stanley Druckenmiller 思维框架
    """
    
    def __init__(self):
        self.name = "Stanley Druckenmiller"
        self.philosophy = "Global Macro + Concentrated Bets + Capital Preservation"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "macro_theme": "unknown",
            "reasoning": [],
            "position_recommendation": "neutral",
            "risk_reward": "neutral",
            "key_insights": []
        }
        
        # 评估宏观环境
        macro_env = self._assess_macro_environment(data)
        result["macro_theme"] = macro_env
        
        # 评估流动性
        liquidity_score = self._assess_liquidity(data)
        
        # 评估趋势强度
        trend_score = self._assess_trend(data)
        
        # 综合评估
        total_score = (
            liquidity_score * 0.35 +
            trend_score * 0.35 +
            self._assess_fundamentals(data) * 0.30
        )
        
        # 生成信号
        if total_score >= 70:
            result["signal"] = "bullish"
            result["confidence"] = min(90, total_score)
            result["position_recommendation"] = "overweight"
        elif total_score <= 40:
            result["signal"] = "bearish"
            result["confidence"] = max(20, total_score)
            result["position_recommendation"] = "underweight"
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
            result["position_recommendation"] = "neutral"
        
        # 风险回报
        result["risk_reward"] = self._assess_risk_reward(data, total_score)
        result["key_insights"] = self._generate_insights(data, macro_env)
        
        return result
    
    def _assess_macro_environment(self, data: Dict) -> str:
        """评估当前宏观环境"""
        inflation = data.get("inflation_trend", "neutral")
        growth = data.get("growth_trend", "neutral")
        monetary = data.get("monetary_policy", "neutral")  # expansion/contraction
        fiscal = data.get("fiscal_policy", "neutral")  # expansion/contraction
        
        if growth == "rising" and inflation == "falling":
            return "Goldilocks (Low rates, High growth)"
        elif growth == "rising" and inflation == "rising":
            return "Reflation (Rising rates, High growth)"
        elif growth == "falling" and inflation == "rising":
            return "Stagflation (High rates, Low growth)"
        elif growth == "falling" and inflation == "falling":
            return "Disinflation (Falling rates, Low growth)"
        elif monetary == "expansion":
            return "Liquidity-driven rally"
        else:
            return "Unclear environment"
    
    def _assess_liquidity(self, data: Dict) -> float:
        """
        评估流动性环境
        Druckenmiller 认为流动性是市场的核心驱动
        """
        score = 50
        
        # 央行政策
        if data.get("central_bank_expanding", False):
            score += 25
        elif data.get("central_bank_contracting", False):
            score -= 25
        
        # 货币供应增长
        m2_growth = data.get("m2_growth_yoy", 0.05)
        if m2_growth > 0.10:
            score += 20
        elif m2_growth > 0.05:
            score += 10
        elif m2_growth < 0:
            score -= 20
        
        # 信用利差（收紧=风险）
        credit_spread = data.get("credit_spread_bps", 100)
        if credit_spread > 300:
            score -= 20  # 紧张
        elif credit_spread < 150:
            score += 10
        
        # 美元走势（弱势=流动性宽松）
        dollar_trend = data.get("dollar_trend", "neutral")
        if dollar_trend == "weakening":
            score += 15
        elif dollar_trend == "strengthening":
            score -= 15
        
        return max(10, min(95, score))
    
    def _assess_trend(self, data: Dict) -> float:
        """评估技术面/趋势强度"""
        score = 50
        
        # 200日均线
        price = data.get("current_price", 0)
        ma200 = data.get("ma_200", 0)
        if price > ma200 * 1.05:
            score += 20
        elif price < ma200 * 0.95:
            score -= 20
        
        # 相对强度
        rs_rating = data.get("relative_strength", 50)
        if rs_rating > 70:
            score += 15
        elif rs_rating < 30:
            score -= 15
        
        # 趋势一致性
        if data.get("price_above_ma50", False) and data.get("ma50_above_ma200", False):
            score += 10
        
        # 成交量确认
        if data.get("volume_increasing", False):
            score += 5
        
        return max(10, min(95, score))
    
    def _assess_fundamentals(self, data: Dict) -> float:
        """评估基本面"""
        score = 50
        
        # 估值
        pe = data.get("pe_ratio", 20)
        if pe < 15:
            score += 15
        elif pe > 30:
            score -= 15
        
        # 盈利增长
        earnings_growth = data.get("earnings_growth", 0.05)
        if earnings_growth > 0.15:
            score += 15
        elif earnings_growth > 0.05:
            score += 5
        elif earnings_growth < 0:
            score -= 15
        
        # 宏观敏感度（某些股票对宏观敏感）
        macro_sensitivity = data.get("macro_sensitivity", "medium")
        if macro_sensitivity == "high":
            # 高敏感度在宏观好时加分
            if self._assess_liquidity(data) > 60:
                score += 10
        
        return max(10, min(95, score))
    
    def _assess_risk_reward(self, data: Dict, score: float) -> str:
        """评估风险回报比"""
        upside = data.get("upside_to_target", 0.20)
        downside = data.get("downside_risk", 0.10)
        
        ratio = upside / downside if downside > 0 else 1
        
        if ratio > 3:
            return f"Excellent ({ratio:.1f}:1)"
        elif ratio > 2:
            return f"Good ({ratio:.1f}:1)"
        elif ratio > 1:
            return f"Neutral ({ratio:.1f}:1)"
        else:
            return f"Poor ({ratio:.1f}:1)"
    
    def _generate_insights(self, data: Dict, macro: str) -> List[str]:
        """生成 Druckenmiller 风格的洞察"""
        insights = []
        
        insights.append(f"Current environment: {macro}")
        
        if data.get("central_bank_expanding", False):
            insights.append("Central bank liquidity supports risk assets")
        
        if data.get("dollar_trend", "neutral") == "weakening":
            insights.append("Dollar weakness amplifies global liquidity")
        
        if data.get("credit_spread_bps", 100) > 300:
            insights.append("Credit stress signal - be cautious")
        
        # 仓位建议
        if data.get("has_thematic_trade", False):
            insights.append("Strong thematic setup - consider concentrated position")
        
        return insights
    
    def get_position_sizing_rules(self, conviction: float, risk: float) -> Dict:
        """
        Druckenmiller 的仓位管理原则
        高置信度 + 低风险 = 重仓
        """
        max_position = min(20, max(2, conviction * 0.3))
        
        adjusted_size = max_position * (1 - risk * 0.5)
        
        return {
            "recommended_position_pct": f"{adjusted_size:.1f}%",
            "conviction_level": conviction,
            "risk_level": risk,
            "rationale": "Druckenmiller: Size positions based on conviction and liquidity risk"
        }


def create_druckenmiller_agent() -> StanleyDruckenmillerDistilled:
    return StanleyDruckenmillerDistilled()
