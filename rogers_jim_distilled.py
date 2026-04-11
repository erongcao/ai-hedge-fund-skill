#!/usr/bin/env python3
"""
Jim Rogers 思维框架蒸馏 - 女娲版

核心理念：全球宏观 + 商品投资 + 新兴市场 + 逆向思维

心智模型：
1. 全球视野（Global Perspective）- 不局限于单一市场
2. 商品为王（Commodities King）- 实物资产重要性
3. 新兴市场（Emerging Markets）- 成长潜力
4. 逆向投资（Contrarian）- 人弃我取
5. 流动性管理（Liquidity）- 保持现金流动性

核心原则：
1. "商品会涨，法定货币会跌"
2. "投资于你了解的领域"
3. "不要听华尔街的"
4. "保持耐心，等待完美机会"
5. "熊市是赚钱的好时机"

决策启发式：
1. 首先判断大趋势（通胀/通缩、美元强弱）
2. 关注商品和实物资产
3. 寻找被低估的新兴市场
4. 保持足够的流动性
5. 不要频繁交易

反模式（Rogers 绝对不会做的事）：
- 不会投资自己不了解的市场
- 不会持有法定货币过多
- 不会在泡沫中追涨
- 不会忽视地缘政治风险
"""

from typing import Dict, List

class JimRogersDistilled:
    """
    蒸馏后的 Jim Rogers 思维框架
    """
    
    def __init__(self):
        self.name = "Jim Rogers"
        self.philosophy = "Global Macro + Commodities + Emerging Markets"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "macro_regime": "unknown",
            "commodity_signal": "neutral",
            "emerging_market_signal": "neutral",
            "contrarian_opportunities": [],
            "reasoning": []
        }
        
        # 评估宏观 regime
        regime = self._assess_macro_regime(data)
        result["macro_regime"] = regime
        
        # 商品信号
        commodity = self._assess_commodities(data, regime)
        result["commodity_signal"] = commodity
        
        # 新兴市场信号
        emerging = self._assess_emerging_markets(data, regime)
        result["emerging_market_signal"] = emerging
        
        # 逆向机会
        contrarian = self._check_contrarian_opportunities(data)
        result["contrarian_opportunities"] = contrarian
        
        # 综合评分
        total_score = regime["score"] * 0.40 + commodity["score"] * 0.35 + emerging["score"] * 0.25
        
        if total_score >= 70:
            result["signal"] = "bullish"
            result["confidence"] = min(90, total_score)
        elif total_score <= 40:
            result["signal"] = "neutral"
            result["confidence"] = max(30, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        result["reasoning"] = self._generate_reasoning(result, regime, commodity, emerging)
        
        return result
    
    def _assess_macro_regime(self, data: Dict) -> Dict:
        """评估宏观 regime"""
        regime = {"score": 50, "type": "unknown", "implications": []}
        
        inflation = data.get("inflation_trend", "neutral")
        growth = data.get("growth_trend", "neutral")
        dollar = data.get("dollar_trend", "neutral")
        
        # 判断 regime 类型
        if inflation == "rising" and growth == "rising":
            regime["type"] = "再通胀"
            regime["score"] = 70
            regime["implications"].append("商品和贵金属受益")
        elif inflation == "rising" and growth == "falling":
            regime["type"] = "滞胀"
            regime["score"] = 60
            regime["implications"].append("现金和短债相对安全")
        elif inflation == "falling" and growth == "falling":
            regime["type"] = "通缩"
            regime["score"] = 40
            regime["implications"].append("避免长期债券")
        elif inflation == "falling" and growth == "rising":
            regime["type"] = "金发女孩"
            regime["score"] = 65
            regime["implications"].append("股票和商品平衡")
        
        # 美元影响
        if dollar == "strengthening":
            regime["score"] -= 15
            regime["implications"].append("新兴市场和商品承压")
        elif dollar == "weakening":
            regime["score"] += 15
            regime["implications"].append("新兴市场和商品受益")
        
        return regime
    
    def _assess_commodities(self, data: Dict, regime: Dict) -> Dict:
        """评估商品信号"""
        commodity = {"score": 50, "direction": "neutral", "opportunities": []}
        
        # 商品价格趋势
        if data.get("commodity_bull_cycle", False):
            commodity["score"] += 30
            commodity["direction"] = "bullish"
            commodity["opportunities"].append("商品牛市周期")
        
        if data.get(" commodity_undervalued", False):
            commodity["score"] += 20
            commodity["opportunities"].append("商品被低估")
        
        # 实物资产偏好
        if regime["type"] in ["再通胀", "滞胀"]:
            commodity["score"] += 20
            commodity["opportunities"].append("抗通胀配置")
        
        return commodity
    
    def _assess_emerging_markets(self, data: Dict, regime: Dict) -> Dict:
        """评估新兴市场"""
        emerging = {"score": 50, "direction": "neutral", "attractive_markets": []}
        
        # 美元强弱
        if data.get("dollar_trend", "neutral") == "weakening":
            emerging["score"] += 25
            emerging["attractive_markets"].append("新兴市场普遍受益")
        
        # 估值
        if data.get("emerging_undervalued", False):
            emerging["score"] += 20
            emerging["attractive_markets"].append("估值吸引")
        
        # 增长潜力
        if regime["type"] == "再通胀":
            emerging["score"] += 15
        
        if emerging["score"] > 65:
            emerging["direction"] = "bullish"
        
        return emerging
    
    def _check_contrarian_opportunities(self, data: Dict) -> List[str]:
        """检查逆向机会"""
        opportunities = []
        
        # 被过度抛售
        if data.get("oversold_contrarian", False):
            opportunities.append("被过度抛售的资产")
        
        # 被冷落的资产类别
        if data.get("commodity_unpopular", False):
            opportunities.append("不受欢迎的商品")
        
        if data.get("emerging_market_unloved", False):
            opportunities.append("被遗忘的新兴市场")
        
        return opportunities
    
    def _generate_reasoning(self, result: Dict, regime: Dict, commodity: Dict, emerging: Dict) -> List[str]:
        """生成推理"""
        reasoning = []
        
        reasoning.append(f"宏观 Regime: {regime['type']} ({regime['score']:.0f}%)")
        
        if regime["implications"]:
            reasoning.append(f"含义: {'; '.join(regime['implications'][:2])}")
        
        if commodity["opportunities"]:
            reasoning.append(f"商品: {'; '.join(commodity['opportunities'][:2])}")
        
        if result["contrarian_opportunities"]:
            reasoning.append(f"逆向机会: {result['contrarian_opportunities'][0]}")
        
        return reasoning


def create_rogers_agent() -> JimRogersDistilled:
    return JimRogersDistilled()
