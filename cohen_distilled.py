#!/usr/bin/env python3
"""
Steve Cohen 思维框架蒸馏 - 女娲版

核心理念：基本面选股 + 交易敏锐 + 信息网络

心智模型：
1. 基本面驱动（Fundamental-Driven）- 股票要能说清楚上涨逻辑
2. 交易能力（Trading Skill）- 知道何时进场和出场
3. 信息网络（Information Network）- 好的信息是优势
4. 灵活性（Flexibility）- 不固执于任何仓位
5. 快速止损（Rapid Loss Execution）- 亏钱时不能拖

决策启发式：
1. 每笔交易要有thesis，逻辑坏了就走
2. 仓位大小要和对事件的置信度匹配
3. 分散但不要太分散（10-20个核心持仓）
4. 关注现金流和盈利质量
5. 市场在变化，策略也要变

反模式（Cohen 绝对不会做的事）：
- 不会死扛亏损头寸
- 不会重仓单一没有充分研究的机会
- 不会忽视市场信号
- 不会在不确定时不下注（要么全押要么不做）
- 不会把投资决定建立在情绪上

诚实边界：
- 需要稳定的信息来源
- 需要强大的交易执行能力
- 需要心理承受大波动
- Point72 的高波动期说明了这种策略的风险
"""

from typing import Dict, List

class SteveCohenDistilled:
    """
    蒸馏后的 Steve Cohen (Point72) 思维框架
    """
    
    def __init__(self):
        self.name = "Steve Cohen"
        self.philosophy = "Fundamental Stock Picking + Trading Skill + Information Edge"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "thesis_clarity": "unclear",
            "reasoning": [],
            "entry_exit_plan": {},
            "key_insights": []
        }
        
        # 评估 thesis 清晰度
        thesis_score = self._assess_thesis(data)
        result["thesis_clarity"] = thesis_score
        
        # 评估基本面
        fundamental_score = self._assess_fundamentals(data)
        
        # 评估技术面
        technical_score = self._assess_technical(data)
        
        # 综合评分
        total_score = (
            thesis_score * 0.40 +
            fundamental_score * 0.35 +
            technical_score * 0.25
        )
        
        # 生成信号
        if total_score >= 70:
            result["signal"] = "bullish"
        elif total_score <= 40:
            result["signal"] = "bearish"
        else:
            result["signal"] = "neutral"
        
        result["confidence"] = total_score
        
        # 入场出场计划
        result["entry_exit_plan"] = self._create_entry_exit_plan(data, total_score)
        result["key_insights"] = self._generate_insights(data)
        
        return result
    
    def _assess_thesis(self, data: Dict) -> float:
        """评估投资 thesis 的清晰度和质量"""
        score = 50
        
        # 能说清楚上涨逻辑吗
        has_clear_catalyst = data.get("has_clear_catalyst", False)
        has_price_target = data.get("has_price_target", False)
        has_timeline = data.get("has_timeline", False)
        
        if has_clear_catalyst:
            score += 20
        
        if has_price_target:
            score += 15
        
        if has_timeline:
            score += 10
        
        # 风险回报比
        risk_reward = data.get("risk_reward_ratio", 1.0)
        if risk_reward > 2.5:
            score += 15
        elif risk_reward > 1.5:
            score += 8
        
        return max(20, min(95, score))
    
    def _assess_fundamentals(self, data: Dict) -> float:
        """评估基本面质量"""
        score = 50
        
        # 盈利质量
        earnings_quality = data.get("earnings_quality_score", 0.5)
        score += int(earnings_quality * 30)
        
        # 现金流
        fcf_yield = data.get("free_cash_flow_yield", 0.05)
        if fcf_yield > 0.08:
            score += 15
        elif fcf_yield < 0:
            score -= 15
        
        # 估值相对成长
        peg = data.get("peg_ratio", 1.0)
        if 0 < peg < 1.0:
            score += 10
        elif peg > 2.0:
            score -= 10
        
        return max(15, min(95, score))
    
    def _assess_technical(self, data: Dict) -> float:
        """评估技术面"""
        score = 50
        
        # 趋势
        price = data.get("current_price", 0)
        ma50 = data.get("ma_50", 0)
        ma200 = data.get("ma_200", 0)
        
        if price > ma50 > ma200:
            score += 20  # 完美上升趋势
        elif price > ma200:
            score += 10
        
        # 相对强弱
        rs = data.get("relative_strength_12m", 50)
        if rs > 65:
            score += 10
        elif rs < 35:
            score -= 10
        
        return max(15, min(90, score))
    
    def _create_entry_exit_plan(self, data: Dict, score: float) -> Dict:
        """Cohen 风格的入场出场计划"""
        current = data.get("current_price", 0)
        target = data.get("price_target", current * 1.2)
        stop = data.get("stop_loss", current * 0.90)
        
        # 根据置信度调整仓位
        if score >= 75:
            position_size = "7-10%"
            allocation = "high conviction"
        elif score >= 60:
            position_size = "4-6%"
            allocation = "medium conviction"
        else:
            position_size = "1-3%"
            allocation = "low conviction speculative"
        
        return {
            "entry_price": f"${current:.2f}" if current > 0 else "TBD",
            "price_target": f"${target:.2f}" if target > 0 else "TBD based on thesis",
            "stop_loss": f"${stop:.2f}" if stop > 0 else "Strict exit on thesis failure",
            "position_size": position_size,
            "allocation": allocation,
            "thesis_evaluation": "Evaluate weekly, exit if thesis breaks"
        }
    
    def _generate_insights(self, data: Dict) -> List[str]:
        """生成洞察"""
        insights = []
        
        if data.get("has_insider_buying", False):
            insights.append("Recent insider buying signals confidence")
        
        if data.get("short_interest_ratio", 0) > 0.10:
            insights.append("High short interest - potential short squeeze candidate")
        
        if data.get("institutional_ownership", 0.5) < 0.3:
            insights.append("Low institutional ownership - potential for re-rating")
        
        return insights


def create_cohen_agent() -> SteveCohenDistilled:
    return SteveCohenDistilled()
