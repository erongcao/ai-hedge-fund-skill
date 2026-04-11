#!/usr/bin/env python3
"""
Larry Williams 思维框架蒸馏 - 女娲版

核心理念：超卖超买 + 季节性 + 短线交易

心智模型：
1. 超卖超买（Overbought/Oversold）- 极端区域的反转机会
2. 季节性（Seasonality）- 某些时期有规律
3. 短线交易（Short-Term Trading）- 快速进出
4. 百分比目标（Percentage Targets）- 用固定目标
5. 资金管理（Money Management）- 保护本金

核心指标：
1. Williams %R - 超卖超买指标
2. 季节性效应 - 年度规律
3. 动量震荡指标 - 短线信号

决策启发式：
1. 在超卖区买入，在超买区卖出
2. 关注季节性窗口
3. 设置固定的百分比止损
4. 短线交易不持仓过夜

反模式（Williams 绝对不会做的事）：
- 不会在极端超买时追高
- 不会忽视超卖反弹机会
- 不会让利润变成亏损
"""

from typing import Dict, List

class LarryWilliamsDistilled:
    """
    蒸馏后的 Larry Williams 思维框架
    """
    
    def __init__(self):
        self.name = "Larry Williams"
        self.philosophy = "Overbought/Oversold + Seasonality + Short-Term"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "williams_r": 0,
            "overbought_oversold": "neutral",
            "seasonal_signal": "neutral",
            "short_term_bias": "neutral",
            "reasoning": []
        }
        
        # Williams %R
        williams_r = self._calculate_williams_r(data)
        result["williams_r"] = williams_r
        result["overbought_oversold"] = self._interpret_williams_r(williams_r)
        
        # 季节性
        seasonal = self._check_seasonality(data)
        result["seasonal_signal"] = seasonal
        
        # 短线偏向
        short_term = self._assess_short_term(data, williams_r, seasonal)
        result["short_term_bias"] = short_term["bias"]
        
        # 综合评分
        total_score = (
            short_term["momentum_score"] * 0.40 +
            seasonal["score"] * 0.30 +
            short_term["timing_score"] * 0.30
        )
        
        if total_score >= 70:
            result["signal"] = "bullish" if short_term["bias"] == "bullish" else "bearish"
            result["confidence"] = min(90, total_score)
        elif total_score <= 40:
            result["signal"] = "neutral"
            result["confidence"] = max(30, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        result["reasoning"] = self._generate_reasoning(result, short_term, seasonal)
        
        return result
    
    def _calculate_williams_r(self, data: Dict) -> float:
        """计算Williams %R"""
        # Williams %R = (最高价 - 收盘价) / (最高价 - 最低价) * -100
        price = data.get("current_price", 0)
        high_14 = data.get("high_14d", price)
        low_14 = data.get("low_14d", price)
        
        if high_14 > low_14 and high_14 > price:
            williams_r = ((high_14 - price) / (high_14 - low_14)) * -100
        else:
            williams_r = -50  # 中性
        
        return williams_r
    
    def _interpret_williams_r(self, williams_r: float) -> str:
        """解读Williams %R"""
        if williams_r > -20:
            return "overbought"
        elif williams_r < -80:
            return "oversold"
        else:
            return "neutral"
    
    def _check_seasonality(self, data: Dict) -> Dict:
        """检查季节性信号"""
        seasonal = {"score": 50, "pattern": "none", "direction": "neutral"}
        
        import datetime
        month = datetime.datetime.now().month
        
        # 简单的季节性规律
        # 这是示例，实际需要更复杂的历史数据分析
        bullish_months = [11, 12, 1, 3]  # 年末年初通常表现好
        bearish_months = [6, 7, 8, 9]  # 夏季通常较差
        
        if month in bullish_months:
            seasonal["score"] = 70
            seasonal["pattern"] = "年末/年初效应"
            seasonal["direction"] = "bullish"
        elif month in bearish_months:
            seasonal["score"] = 35
            seasonal["pattern"] = "夏季疲软"
            seasonal["direction"] = "bearish"
        
        return seasonal
    
    def _assess_short_term(self, data: Dict, williams_r: float, seasonal: Dict) -> Dict:
        """评估短线机会"""
        st = {"bias": "neutral", "momentum_score": 50, "timing_score": 50}
        
        # 动量评分
        if data.get("momentum_5d", 0) > 0:
            st["momentum_score"] += 15
        elif data.get("momentum_5d", 0) < 0:
            st["momentum_score"] -= 15
        
        if data.get("momentum_10d", 0) > 0:
            st["momentum_score"] += 10
        else:
            st["momentum_score"] -= 10
        
        # Williams %R 信号
        if williams_r < -80:
            st["momentum_score"] += 20
            st["timing_score"] = 75
        elif williams_r > -20:
            st["momentum_score"] -= 20
            st["timing_score"] = 75
        
        # 季节性加成
        if seasonal["direction"] == "bullish":
            st["momentum_score"] += 15
        elif seasonal["direction"] == "bearish":
            st["momentum_score"] -= 15
        
        # 整体偏向
        if st["momentum_score"] > 60:
            st["bias"] = "bullish"
        elif st["momentum_score"] < 40:
            st["bias"] = "bearish"
        
        return st
    
    def _generate_reasoning(self, result: Dict, short_term: Dict, seasonal: Dict) -> List[str]:
        """生成推理"""
        reasoning = []
        
        reasoning.append(f"Williams %R: {result['williams_r']:.1f} ({result['overbought_oversold']})")
        
        if seasonal["pattern"] != "none":
            reasoning.append(f"季节性: {seasonal['pattern']} ({seasonal['direction']})")
        
        reasoning.append(f"短线偏向: {short_term['bias']} (动量: {short_term['momentum_score']:.0f}%)")
        
        return reasoning


def create_williams_agent() -> LarryWilliamsDistilled:
    return LarryWilliamsDistilled()
