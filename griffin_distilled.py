#!/usr/bin/env python3
"""
Ken Griffin 思维框架蒸馏 - 女娲版

核心理念：做市商思维 + 全球市场中性 + 科技驱动

心智模型：
1. 市场中性（Market Neutral）- 同时做多和做空消除市场风险
2. 做市商优势（Market Making Edge）- 理解订单流和信息不对称
3. 技术基础设施（Tech Infrastructure）- 速度就是优势
4. 风险分散（Diversified Risk）- 不依赖单一策略
5. 全球视野（Global Reach）- 跨资产、跨市场机会

决策启发式：
1. 做市商要理解每一笔交易的对家是谁
2. 量化策略要不断迭代，旧的模型会衰减
3. 杠杆是工具，不是目的
4. 流动性好时可以做市，紧张时要撤退
5. 技术投入是竞争力的核心

反模式（Griffin 绝对不会做的事）：
- 不会忽视技术基础设施
- 不会只依赖单一策略
- 不会在流动性差时硬扛
- 不会忽视尾部风险
- 不会把 Citadel 做成单策略基金

诚实边界：
- 需要大量技术人才
- 需要极低延迟的交易系统
- 需要充足的资本缓冲
- 普通投资者难以复制
"""

from typing import Dict, List

class KenGriffinDistilled:
    """
    蒸馏后的 Ken Griffin (Citadel) 思维框架
    """
    
    def __init__(self):
        self.name = "Ken Griffin"
        self.philosophy = "Market Neutral + Tech-Driven + Global Market Making"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "market_neutral_score": 0,
            "reasoning": [],
            "strategy_recommendation": "none",
            "key_metrics": {}
        }
        
        # 评估市场中性潜力
        neutral_score = self._assess_market_neutral(data)
        result["market_neutral_score"] = neutral_score
        
        # 评估做市机会
        making_score = self._assess_market_making(data)
        
        # 综合评分
        total_score = (neutral_score + making_score) / 2
        
        # 生成信号
        if total_score >= 70:
            result["signal"] = "bullish"
            result["strategy_recommendation"] = "market_neutral"
        elif total_score <= 35:
            result["signal"] = "bearish"
            result["strategy_recommendation"] = "reduce_exposure"
        else:
            result["signal"] = "neutral"
        
        result["confidence"] = total_score
        result["key_metrics"] = {
            "market_neutral_score": neutral_score,
            "market_making_score": making_score
        }
        
        return result
    
    def _assess_market_neutral(self, data: Dict) -> float:
        """评估市场中性策略的可行性"""
        score = 50
        
        # 相关性（低相关性才能对冲）
        avg_correlation = data.get("avg_stock_correlation", 0.4)
        if avg_correlation < 0.3:
            score += 25
        elif avg_correlation > 0.6:
            score -= 20
        
        # 波动率
        volatility = data.get("realized_volatility", 0.15)
        if volatility > 0.20:
            score += 15  # 高波动=更多机会
        elif volatility < 0.10:
            score -= 10
        
        # 融资金融券成本
        borrow_cost = data.get("short_borrow_cost_bps", 50)
        if borrow_cost < 30:
            score += 15  # 便宜
        elif borrow_cost > 100:
            score -= 15  # 昂贵
        
        return max(15, min(90, score))
    
    def _assess_market_making(self, data: Dict) -> float:
        """评估做市机会"""
        score = 50
        
        # 交易量
        volume = data.get("avg_daily_volume", 1e6)
        if volume > 10e6:
            score += 20
        elif volume > 1e6:
            score += 10
        
        # 买卖价差
        spread = data.get("avg_bid_ask_spread_bps", 10)
        if spread > 20:
            score += 15
        elif spread < 5:
            score -= 10
        
        # 市场深度
        depth = data.get("order_book_depth", "medium")
        if depth == "high":
            score += 10
        elif depth == "low":
            score -= 10
        
        return max(15, min(90, score))


def create_griffin_agent() -> KenGriffinDistilled:
    return KenGriffinDistilled()
