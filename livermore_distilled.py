#!/usr/bin/env python3
"""
Jesse Livermore 思维框架蒸馏 - 女娲版

核心理念：时机把握 + 趋势确认 + 操盘手心理学

心智模型：
1. 时机把握（Timing）- 在正确的时间买入和卖出
2. 趋势确认（Trend Confirmation）- 等待趋势确认
3. 支撑阻力（Support/Resistance）- 在关键点交易
4. 操盘手心理学（Bucket Shop Psychology）- 理解庄家行为
5. 操守（Integrity）- 遵守自己的规则

核心原则：
1. "市场永远是对的"
2. "在趋势确认后才入场"
3. "支撑位买入，阻力位卖出"
4. "让利润奔跑，截断亏损"
5. "知道什么时候该出局"

关键价位：
1. 最小阻力线 - 趋势会朝最小阻力的方向发展
2. 关键点 - 突破或跌破时入场
3. 连续反弹/回落 - 趋势中的规律

决策启发式：
1. 首先判断最小阻力线方向
2. 等待关键点突破或跌破
3. 在支撑位买入，在阻力位卖出
4. 不要在中间价位交易
5. 知道什么时候该持仓观望

反模式（Livermore 绝对不会做的事）：
- 不会在趋势不明时重仓
- 不会逆势交易
- 不会忽视关键价位
- 不会让亏损头寸发展成灾难
"""

from typing import Dict, List

class JesseLivermoreDistilled:
    """
    蒸馏后的 Jesse Livermore 思维框架
    """
    
    def __init__(self):
        self.name = "Jesse Livermore"
        self.philosophy = "Market Timing + Trend Confirmation + Key Levels"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "path_of_least_resistance": "neutral",
            "key_levels": {},
            "market_position": "观望",
            "reasoning": []
        }
        
        # 评估最小阻力线
        path = self._assess_path_of_least_resistance(data)
        result["path_of_least_resistance"] = path
        
        # 识别关键价位
        levels = self._identify_key_levels(data, path)
        result["key_levels"] = levels
        
        # 市场位置判断
        position = self._assess_market_position(data, path, levels)
        result["market_position"] = position
        
        # 综合评分
        total_score = path["score"]
        
        if path["direction"] != "neutral" and position != "观望":
            total_score += 20
        
        if total_score >= 75:
            result["signal"] = "bullish" if path["direction"] == "up" else "bearish"
            result["confidence"] = min(90, total_score)
        elif total_score <= 40:
            result["signal"] = "neutral"
            result["confidence"] = max(25, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        result["reasoning"] = self._generate_reasoning(result, path, levels, position)
        
        return result
    
    def _assess_path_of_least_resistance(self, data: Dict) -> Dict:
        """评估最小阻力线"""
        path = {"score": 50, "direction": "neutral", "evidence": []}
        
        price = data.get("current_price", 0)
        ma20 = data.get("ma_20", 0)
        ma50 = data.get("ma_50", 0)
        
        # 趋势判断
        if ma20 > 0 and ma50 > 0:
            if price > ma20 > ma50:
                path["direction"] = "up"
                path["score"] = 75
                path["evidence"].append("价格>MA20>MA50 上升排列")
            elif price < ma20 < ma50:
                path["direction"] = "down"
                path["score"] = 75
                path["evidence"].append("价格<MA20<MA50 下降排列")
            elif price > ma20:
                path["direction"] = "up"
                path["score"] = 60
                path["evidence"].append("价格>MA20")
            elif price < ma20:
                path["direction"] = "down"
                path["score"] = 60
                path["evidence"].append("价格<MA20")
        
        # 突破确认
        if data.get("breakout_20d_high", False) and path["direction"] == "up":
            path["score"] += 15
            path["evidence"].append("突破20日高点")
        elif data.get("breakout_20d_low", False) and path["direction"] == "down":
            path["score"] += 15
            path["evidence"].append("跌破20日低点")
        
        # 成交量确认
        if data.get("volume_confirmation", False):
            path["score"] += 10
            path["evidence"].append("成交量放大确认")
        
        return path
    
    def _identify_key_levels(self, data: Dict, path: Dict) -> Dict:
        """识别关键价位"""
        levels = {}
        price = data.get("current_price", 0)
        
        # 支撑位
        levels["support"] = data.get("support_level", price * 0.95)
        levels["resistance"] = data.get("resistance_level", price * 1.05)
        
        # 关键点（历史高低点）
        levels["pivot_high"] = data.get("pivot_high_20d", price * 1.02)
        levels["pivot_low"] = data.get("pivot_low_20d", price * 0.98)
        
        # 当前价格位置
        if price > levels["resistance"]:
            levels["price_position"] = "突破阻力"
        elif price < levels["support"]:
            levels["price_position"] = "跌破支撑"
        else:
            levels["price_position"] = "区间内"
        
        return levels
    
    def _assess_market_position(self, data: Dict, path: Dict, levels: Dict) -> str:
        """评估市场位置"""
        position = "观望"
        
        # 突破阻力
        if levels["price_position"] == "突破阻力" and path["direction"] == "up":
            position = "买入时机"
        
        # 跌破支撑
        elif levels["price_position"] == "跌破支撑" and path["direction"] == "down":
            position = "卖出时机"
        
        # 在区间内且趋势不明
        elif levels["price_position"] == "区间内" and path["direction"] == "neutral":
            position = "观望"
        
        # 趋势明确但未突破
        elif path["direction"] == "up" and levels["price_position"] == "区间内":
            position = "等待突破买入"
        elif path["direction"] == "down" and levels["price_position"] == "区间内":
            position = "等待跌破卖出"
        
        return position
    
    def _generate_reasoning(self, result: Dict, path: Dict, levels: Dict, position: str) -> List[str]:
        """生成推理"""
        reasoning = []
        
        direction_desc = "上升" if path["direction"] == "up" else "下降" if path["direction"] == "down" else "不明"
        reasoning.append(f"最小阻力线: {direction_desc} ({path['score']:.0f}%)")
        
        if path["evidence"]:
            reasoning.append(f"证据: {'; '.join(path['evidence'][:2])}")
        
        reasoning.append(f"当前价位: {levels.get('price_position', '区间内')}")
        reasoning.append(f"建议: {position}")
        
        return reasoning


def create_livermore_agent() -> JesseLivermoreDistilled:
    return JesseLivermoreDistilled()
