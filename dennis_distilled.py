#!/usr/bin/env python3
"""
Richard Dennis 思维框架蒸馏 - 女娲版

核心理念：海龟交易法 + 趋势追踪 + 系统化交易

心智模型：
1. 趋势追踪（Trend Following）- 让利润奔跑，截断亏损
2. 系统化交易（Systematic Trading）- 用规则而非直觉
3. 风险管理优先（Risk Management First）- 保护资本
4. 分散化（Diversification）- 多市场、多策略
5. 机械执行（Mechanical Execution）- 消除情绪干扰

海龟交易规则：
1. 追随趋势，不预测顶部或底部
2. 突破20日高低点时入场
3. 2N止损（基于ATR的风险管理）
4. 金字塔加仓（趋势确认后加仓）
5. 永远不让盈利变成亏损

决策启发式：
1. "追随趋势，让利润奔跑"
2. "截断亏损，让利润奔跑"
3. "当市场朝有利方向移动时，加仓"
4. "如果止损被触发，说明趋势可能反转"
5. "不要预测市场要到哪里，学会跟随"

反模式（Dennis 绝对不会做的事）：
- 不会逆势交易
- 不会在止损点上犹豫
- 不会因为亏损而改变系统
- 不会重仓单一头寸

诚实边界：
- 需要严格纪律执行
- 趋势市场表现好，震荡市场可能连续亏损
- 需要足够的资金承受回撤
- 系统需要不断适应市场变化
"""

from typing import Dict, List

class RichardDennisDistilled:
    """
    蒸馏后的 Richard Dennis (海龟交易法) 思维框架
    """
    
    def __init__(self):
        self.name = "Richard Dennis"
        self.philosophy = "Turtle Trading + Trend Following + Systematic Execution"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "trend_score": 0,
            "reasoning": [],
            "entry_signals": [],
            "exit_signals": [],
            "risk_assessment": {}
        }
        
        # 评估趋势强度
        trend_score = self._assess_trend(data)
        result["trend_score"] = trend_score
        
        # 识别入场信号
        entry_signals = self._identify_entry_signals(data, trend_score)
        result["entry_signals"] = entry_signals
        
        # 识别出场信号
        exit_signals = self._identify_exit_signals(data)
        result["exit_signals"] = exit_signals
        
        # 风险管理评估
        risk = self._assess_risk(data)
        result["risk_assessment"] = risk
        
        # 综合评分
        total_score = trend_score * 0.5 + (100 - risk["atr_percent"]) * 0.3 + risk["volatility_score"] * 0.2
        
        if total_score >= 70 and len(entry_signals) > 0:
            result["signal"] = "bullish" if data.get("trend_direction", "neutral") == "up" else "bearish"
            result["confidence"] = min(90, total_score)
        elif total_score <= 40:
            result["signal"] = "neutral"
            result["confidence"] = max(30, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        result["reasoning"] = self._generate_reasoning(result, data)
        
        return result
    
    def _assess_trend(self, data: Dict) -> float:
        """评估趋势强度 - 海龟用20日/55日突破"""
        score = 50
        
        # 价格vs移动均线
        price = data.get("current_price", 0)
        ma20 = data.get("ma_20", 0)
        ma55 = data.get("ma_55", 0)
        
        if ma20 > 0 and ma55 > 0:
            if price > ma20 and ma20 > ma55:
                score += 30  # 上升趋势
            elif price < ma20 and ma20 < ma55:
                score -= 20  # 下降趋势
            elif price > ma20:
                score += 15
            elif price < ma20:
                score -= 10
        
        # 突破20日高低点
        if data.get("breakout_20d_high", False):
            score += 20
        elif data.get("breakout_20d_low", False):
            score -= 20
        
        # ATR趋势
        atr_percent = data.get("atr_percent", 10)
        if atr_percent > 5:
            score += 10  # 波动足够大
        
        return max(10, min(95, score))
    
    def _identify_entry_signals(self, data: Dict, trend_score: float) -> List[str]:
        """识别海龟入场信号"""
        signals = []
        
        # 突破20日高低点
        if data.get("breakout_20d_high", False):
            signals.append("突破20日高点 - 买入信号")
        elif data.get("breakout_20d_low", False):
            signals.append("突破20日低点 - 卖出信号")
        
        # 突破55日高低点（更强信号）
        if data.get("breakout_55d_high", False):
            signals.append("突破55日高点 - 强买入信号")
        elif data.get("breakout_55d_low", False):
            signals.append("突破55日低点 - 强卖出信号")
        
        # 趋势确认
        if trend_score > 70 and data.get("volume_confirmation", False):
            signals.append("趋势确认 + 成交量放大 - 入场时机")
        
        return signals
    
    def _identify_exit_signals(self, data: Dict) -> List[str]:
        """识别海龟出场信号"""
        signals = []
        
        # ATR止损
        atr = data.get("atr", 0)
        entry = data.get("entry_price", 0)
        if atr > 0 and entry > 0:
            stop_loss = entry - 2 * atr
            signals.append(f"止损位: {stop_loss:.2f} (2N规则)")
        
        # 趋势破坏
        if data.get("trend_broken", False):
            signals.append("趋势破坏 - 应立即出场")
        
        # 反转信号
        if data.get("ma_cross_down", False):
            signals.append("均线死叉 - 出场信号")
        
        return signals
    
    def _assess_risk(self, data: Dict) -> Dict:
        """海龟风格的风险评估"""
        risk = {
            "atr_percent": 10,  # ATR占价格百分比
            "position_size": "medium",
            "volatility_score": 50,
            "recommended_stop_pct": 2.0
        }
        
        atr_percent = data.get("atr_percent", 10)
        risk["atr_percent"] = atr_percent
        
        if atr_percent > 10:
            risk["position_size"] = "small"
            risk["volatility_score"] = 30
            risk["recommended_stop_pct"] = 1.0
        elif atr_percent > 5:
            risk["position_size"] = "medium"
            risk["volatility_score"] = 60
            risk["recommended_stop_pct"] = 2.0
        else:
            risk["position_size"] = "large"
            risk["volatility_score"] = 80
            risk["recommended_stop_pct"] = 2.5
        
        return risk
    
    def _generate_reasoning(self, result: Dict, data: Dict) -> List[str]:
        """生成Dennis风格的推理"""
        reasoning = []
        
        reasoning.append(f"趋势评分: {result['trend_score']:.0f}/100")
        
        if result["entry_signals"]:
            reasoning.append(f"入场信号: {len(result['entry_signals'])}个")
        
        if result["risk_assessment"]:
            rs = result["risk_assessment"]
            reasoning.append(f"仓位建议: {rs['position_size']} (ATR: {rs['atr_percent']:.1f}%)")
            reasoning.append(f"止损: {rs['recommended_stop_pct']}N")
        
        return reasoning
    
    def get_turtle_rules(self) -> Dict:
        """海龟交易核心规则"""
        return {
            "entry_rules": [
                "突破20日高低点时入场",
                "趋势确认后金字塔加仓",
                "最多4个单位加仓"
            ],
            "exit_rules": [
                "2N止损",
                "10日低点出场（短线）",
                "20日低点出场（长线）"
            ],
            "position_sizing": [
                "单笔风险不超过2%",
                "根据ATR调整仓位",
                "波动越大仓位越小"
            ]
        }


def create_dennis_agent() -> RichardDennisDistilled:
    return RichardDennisDistilled()
