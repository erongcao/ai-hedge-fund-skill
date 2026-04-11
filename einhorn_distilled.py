#!/usr/bin/env python3
"""
David Einhorn 思维框架蒸馏 - 女娲版

核心理念：价值导向 + 做空能力 + 催化信任

心智模型：
1. 价值投资（Value-Oriented）- 价格低于价值是核心
2. 做空机会（Short Opportunities）- 也能从下跌中获利
3. 催化剂信任（Catalyst Trust）- 等待是有价值的
4. 错误定价发现（Mispricing Discovery）- 市场经常犯错
5. 耐心资本（Patient Capital）- 等待正确时机

决策启发式：
1. 买之前先问：这家公司为什么会涨？
2. 做空之前问：催化剂是什么？时间线呢？
3. 能用一句话解释投资逻辑吗？
4. 等待的过程是投资的一部分
5. 高置信度 + 好价格 = 买入

反模式（Einhorn 绝对不会做的事）：
- 不会买没有清晰催化剂的股票
- 不会在下跌中摊平成本
- 不会忽视治理问题
- 不会做没有安全边际的投机
- 不会忽视宏观风险

诚实边界：
- 做空有无限损失风险
- 需要耐心等待催化剂
- 集中持仓意味着波动性高
"""

from typing import Dict, List

class DavidEinhornDistilled:
    """
    蒸馏后的 David Einhorn (Greenlight Capital) 思维框架
    """
    
    def __init__(self):
        self.name = "David Einhorn"
        self.philosophy = "Value-Oriented + Catalyst-Driven + Long/Short"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "catalyst_clarity": "unclear",
            "reasoning": [],
            "long_short_recommendation": "neutral",
            "key_metrics": {}
        }
        
        # 做多分析
        long_score = self._analyze_long(data)
        
        # 做空分析（如果有）
        short_score = self._analyze_short(data) if data.get("has_short_candidate", False) else 50
        
        # 综合评分
        total_score = long_score * 0.6 + short_score * 0.4
        
        # 生成信号
        if total_score >= 70:
            result["signal"] = "bullish"
        elif total_score <= 40:
            result["signal"] = "bearish"
        else:
            result["signal"] = "neutral"
        
        result["confidence"] = total_score
        result["catalyst_clarity"] = self._assess_catalyst_clarity(data)
        result["key_metrics"] = {
            "long_score": long_score,
            "short_score": short_score,
            "value_score": self._assess_value_score(data)
        }
        
        return result
    
    def _analyze_long(self, data: Dict) -> float:
        score = 50
        
        # 估值
        intrinsic = data.get("intrinsic_value_estimate", 0)
        current = data.get("current_price", 0)
        if intrinsic > current:
            margin = (intrinsic - current) / intrinsic
            score += int(margin * 40)
        
        # 催化剂
        if data.get("has_clear_catalyst", False):
            score += 15
        
        # 管理层
        if data.get("management_quality", "average") == "excellent":
            score += 10
        
        return max(15, min(95, score))
    
    def _analyze_short(self, data: Dict) -> float:
        score = 50
        
        # 做空需要更严格的条件
        if not data.get("has_short_candidate", False):
            return 50
        
        # 催化剂明确
        if data.get("short_catalyst", "none") != "none":
            score += 25
        
        # 高估值
        peg = data.get("peg_ratio", 1.0)
        if peg > 3:
            score += 20
        
        # 商业模式问题
        if data.get("has_business_model_problems", False):
            score += 15
        
        return max(15, min(90, score))
    
    def _assess_catalyst_clarity(self, data: Dict) -> str:
        if data.get("has_clear_catalyst", False):
            return "clear - specific event expected"
        elif data.get("has_vague_catalyst", False):
            return "vague - general thesis"
        else:
            return "unclear - patience required"
    
    def _assess_value_score(self, data: Dict) -> float:
        score = 50
        pe = data.get("pe_ratio", 20)
        if 0 < pe < 15:
            score += 20
        elif pe > 30:
            score -= 15
        return max(15, min(90, score))


def create_einhorn_agent() -> DavidEinhornDistilled:
    return DavidEinhornDistilled()
