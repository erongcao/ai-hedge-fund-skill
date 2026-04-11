#!/usr/bin/env python3
"""
Ed Seykota 思维框架蒸馏 - 女娲版

核心理念：趋势追踪 + 电脑化交易 + 心理控制

心智模型：
1. 趋势是朋友（Trend is Your Friend）- 追随主要趋势
2. 电脑化系统（Computerized Systems）- 用技术发现模式
3. 心理管理（Psychology Management）- 控制情绪
4. 风险控制（Risk Control）- 保护资本
5. 简单系统（Simple Systems）- 复杂不等于有效

核心原则：
1. "趋势是你的朋友"
2. "截断亏损，让利润奔跑"
3. "了解自己"
4. "市场是有节奏的"
5. "管理风险比赚钱更重要"

决策启发式：
1. 识别主要趋势方向
2. 只在趋势方向交易
3. 用技术指标确认趋势
4. 设定止损点
5. 监控心理状态

反模式（Seykota 绝对不会做的事）：
- 不会逆趋势交易
- 不会忽视系统信号
- 不会让情绪影响决策
- 不会重仓过夜不设止损
"""

from typing import Dict, List

class EdSeykotaDistilled:
    """
    蒸馏后的 Ed Seykota 思维框架
    """
    
    def __init__(self):
        self.name = "Ed Seykota"
        self.philosophy = "Trend Following + Computerized Systems + Psychology"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "trend_direction": "neutral",
            "trend_strength": 0,
            "system_signals": [],
            "psychology_factors": [],
            "reasoning": []
        }
        
        # 评估趋势
        trend = self._assess_trend(data)
        result["trend_direction"] = trend["direction"]
        result["trend_strength"] = trend["strength"]
        
        # 系统信号
        signals = self._get_system_signals(data, trend)
        result["system_signals"] = signals
        
        # 心理因素
        psych = self._assess_psychology(data)
        result["psychology_factors"] = psych
        
        # 综合评分
        total_score = (
            trend["strength"] * 0.40 +
            signals["score"] * 0.35 +
            (100 - psych["fear_score"]) * 0.25
        )
        
        if total_score >= 70:
            result["signal"] = "bullish" if trend["direction"] == "up" else "bearish"
            result["confidence"] = min(90, total_score)
        elif total_score <= 40:
            result["signal"] = "neutral"
            result["confidence"] = max(30, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        result["reasoning"] = self._generate_reasoning(result, trend, signals)
        
        return result
    
    def _assess_trend(self, data: Dict) -> Dict:
        """评估趋势"""
        trend = {"direction": "neutral", "strength": 50}
        
        # 价格vs均线
        price = data.get("current_price", 0)
        ma20 = data.get("ma_20", 0)
        ma50 = data.get("ma_50", 0)
        ma200 = data.get("ma_200", 0)
        
        if ma20 > 0 and price > 0:
            if price > ma20 > ma50 > ma200:
                trend["direction"] = "up"
                trend["strength"] = 85
            elif price < ma20 < ma50 < ma200:
                trend["direction"] = "down"
                trend["strength"] = 85
            elif price > ma20 and ma20 > ma50:
                trend["direction"] = "up"
                trend["strength"] = 65
            elif price < ma20 and ma20 < ma50:
                trend["direction"] = "down"
                trend["strength"] = 65
        
        # 趋势强度指标
        if data.get("adx", 0) > 25:
            trend["strength"] += 10
        elif data.get("adx", 0) < 15:
            trend["strength"] -= 15
        
        return trend
    
    def _get_system_signals(self, data: Dict, trend: Dict) -> Dict:
        """获取系统信号"""
        sig = {"score": 50, "signals": []}
        
        # 均线交叉
        if data.get("ma_cross_gold", False):
            sig["signals"].append("金叉 - 买入信号")
            sig["score"] += 25
        elif data.get("ma_cross_death", False):
            sig["signals"].append("死叉 - 卖出信号")
            sig["score"] -= 20
        
        # MACD
        if data.get("macd_histogram", 0) > 0:
            sig["score"] += 15
            sig["signals"].append("MACD柱状图正值")
        
        # 趋势确认
        if trend["strength"] > 70:
            sig["score"] += 15
            sig["signals"].append("趋势强度确认")
        
        # RSI超买超卖
        rsi = data.get("rsi", 50)
        if rsi > 70:
            sig["score"] -= 15
            sig["signals"].append("RSI超买")
        elif rsi < 30:
            sig["score"] += 10
            sig["signals"].append("RSI超卖")
        
        return sig
    
    def _assess_psychology(self, data: Dict) -> Dict:
        """评估心理因素"""
        psych = {"fear_score": 50, "factors": []}
        
        # VIX作为恐惧指标
        vix = data.get("vix", 20)
        if vix > 30:
            psych["fear_score"] = 80
            psych["factors"].append("市场极度恐惧")
        elif vix > 25:
            psych["fear_score"] = 65
            psych["factors"].append("市场担忧")
        elif vix < 15:
            psych["fear_score"] = 25
            psych["factors"].append("市场贪婪")
        
        # 持仓情绪
        if data.get("sentiment_extreme_greed", False):
            psych["fear_score"] = 20
            psych["factors"].append("极端贪婪信号")
        elif data.get("sentiment_extreme_fear", False):
            psych["fear_score"] = 85
            psych["factors"].append("极端恐惧信号")
        
        return psych
    
    def _generate_reasoning(self, result: Dict, trend: Dict, signals: Dict) -> List[str]:
        """生成推理"""
        reasoning = []
        
        direction = "上升" if result["trend_direction"] == "up" else "下降" if result["trend_direction"] == "down" else "震荡"
        reasoning.append(f"趋势: {direction} (强度{result['trend_strength']:.0f}%)")
        
        if signals["signals"]:
            reasoning.append(f"信号: {'; '.join(signals['signals'][:3])}")
        
        if result["psychology_factors"]:
            reasoning.append(f"心理: {'; '.join(list(result['psychology_factors'])[:2])}")
        
        return reasoning


def create_seykota_agent() -> EdSeykotaDistilled:
    return EdSeykotaDistilled()
