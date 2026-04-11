#!/usr/bin/env python3
"""
Bruce Kovner 思维框架蒸馏 - 女娲版

核心理念：宏观+技术+风险管理三位一体

心智模型：
1. 宏观趋势（Macro Trends）- 理解大方向
2. 技术分析（Technical Analysis）- 找到精确入场点
3. 风险管理（Risk Management）- 保护资本
4. 灵活应变（Flexibility）- 承认错误并改正
5. 耐心等待（Patience）- 等待完美机会

核心原则：
1. "好的交易需要三个要素：方向、时机、价格"
2. "在关键支撑位买入，在关键阻力位卖出"
3. "知道什么时候退出比知道什么时候入场更重要"
4. "管理风险是生存的关键"
5. "错误时立刻承认，不要固执"

决策启发式：
1. 首先判断宏观趋势
2. 找到技术上的关键点位
3. 计算风险回报比
4. 等待最佳入场时机
5. 设定止损和目标

反模式（Kovner 绝对不会做的事）：
- 不会在支撑位以下买入
- 不会忽视技术信号
- 不会让亏损头寸发展成灾难
- 不会重仓单一判断
"""

from typing import Dict, List

class BruceKovnerDistilled:
    """
    蒸馏后的 Bruce Kovner (Caxton Associates) 思维框架
    """
    
    def __init__(self):
        self.name = "Bruce Kovner"
        self.philosophy = "Macro + Technical + Risk Management Trinity"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "macro_alignment": "neutral",
            "technical_score": 0,
            "key_levels": {},
            "entry_quality": "poor",
            "reasoning": []
        }
        
        # 宏观对齐
        macro = self._check_macro_alignment(data)
        result["macro_alignment"] = macro
        
        # 技术评分
        tech = self._assess_technical(data)
        result["technical_score"] = tech["score"]
        result["key_levels"] = tech["levels"]
        
        # 入场质量
        entry = self._assess_entry_quality(data, macro, tech)
        result["entry_quality"] = entry
        
        # 综合评分
        total_score = (
            macro["score"] * 0.35 +
            tech["score"] * 0.35 +
            entry["score"] * 0.30
        )
        
        if total_score >= 70 and entry["quality"] != "poor":
            result["signal"] = "bullish" if macro["direction"] == "bullish" else "bearish"
            result["confidence"] = min(90, total_score)
        elif total_score <= 40 or entry["quality"] == "poor":
            result["signal"] = "neutral"
            result["confidence"] = max(30, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        result["reasoning"] = self._generate_reasoning(result, macro, tech, entry)
        
        return result
    
    def _check_macro_alignment(self, data: Dict) -> Dict:
        """检查宏观趋势对齐"""
        macro = {"score": 50, "direction": "neutral", "theme": ""}
        
        # 通胀和增长
        inflation = data.get("inflation_trend", "neutral")
        growth = data.get("growth_trend", "neutral")
        
        if inflation == "rising" and growth == "rising":
            macro["score"] += 20
            macro["theme"] = "再通胀交易"
        elif inflation == "rising" and growth == "falling":
            macro["score"] -= 15
            macro["theme"] = "滞胀风险"
        elif inflation == "falling" and growth == "rising":
            macro["score"] += 15
            macro["theme"] = "金发女孩"
        elif inflation == "falling" and growth == "falling":
            macro["score"] -= 10
            macro["theme"] = "通缩风险"
        
        # 央行政策
        if data.get("central_bank_expanding", False):
            macro["score"] += 15
            macro["theme"] = "宽松货币"
        
        if macro["score"] > 60:
            macro["direction"] = "bullish"
        elif macro["score"] < 40:
            macro["direction"] = "bearish"
        
        return macro
    
    def _assess_technical(self, data: Dict) -> Dict:
        """技术分析"""
        tech = {"score": 50, "levels": {}}
        
        # 支撑阻力
        price = data.get("current_price", 0)
        support = data.get("support_level", price * 0.95)
        resistance = data.get("resistance_level", price * 1.05)
        
        tech["levels"]["support"] = support
        tech["levels"]["resistance"] = resistance
        
        # 价格vs关键位置
        if price > resistance:
            tech["score"] += 25
            tech["levels"]["status"] = "突破阻力"
        elif price < support:
            tech["score"] -= 25
            tech["levels"]["status"] = "跌破支撑"
        else:
            # 在区间内
            distance_to_support = (price - support) / support
            distance_to_resistance = (resistance - price) / price
            
            if distance_to_support < 0.02:
                tech["score"] -= 15  # 接近支撑，可能跌破
            elif distance_to_resistance < 0.02:
                tech["score"] += 15  # 接近阻力，可能突破
        
        # 趋势指标
        if data.get("trend_intact", False):
            tech["score"] += 15
        
        # 成交量
        if data.get("volume_confirmation", False):
            tech["score"] += 10
        
        return tech
    
    def _assess_entry_quality(self, data: Dict, macro: Dict, tech: Dict) -> Dict:
        """评估入场质量"""
        entry = {"score": 50, "quality": "average", "notes": []}
        
        # 检查是否在好的位置
        if tech["levels"].get("status") == "突破阻力":
            entry["quality"] = "excellent"
            entry["score"] = 85
            entry["notes"].append("在突破点入场")
        elif tech["levels"].get("status") == "跌破支撑":
            entry["quality"] = "avoid"
            entry["score"] = 20
            entry["notes"].append("避免在支撑以下入场")
        elif tech["score"] > 60:
            entry["quality"] = "good"
            entry["score"] = 70
            entry["notes"].append("技术面支持")
        elif tech["score"] < 40:
            entry["quality"] = "poor"
            entry["score"] = 35
            entry["notes"].append("技术面不利")
        
        # 宏观对齐
        if macro["score"] > 60 and entry["quality"] == "good":
            entry["score"] += 15
            entry["notes"].append("宏观对齐")
        
        return entry
    
    def _generate_reasoning(self, result: Dict, macro: Dict, tech: Dict, entry: Dict) -> List[str]:
        """生成推理"""
        reasoning = []
        
        reasoning.append(f"宏观: {macro['theme']} ({macro['score']:.0f}%)")
        reasoning.append(f"技术: {tech['score']:.0f}%, 状态: {tech['levels'].get('status', '区间内')}")
        reasoning.append(f"入场质量: {entry['quality']}")
        
        if entry["notes"]:
            reasoning.append(f"要点: {'; '.join(entry['notes'])}")
        
        return reasoning


def create_kovner_agent() -> BruceKovnerDistilled:
    return BruceKovnerDistilled()
