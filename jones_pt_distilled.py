#!/usr/bin/env python3
"""
Paul Tudor Jones 思维框架蒸馏 - 女娲版

核心理念：宏观分析 + 风险管理 + 纪律执行 + 预测崩溃

心智模型：
1. 宏观驱动（Macro-Driven）- 理解大的经济趋势
2. 风险管理至上（Risk Management Supreme）- 保护本金
3. 纪律执行（Disciplined Execution）- 严格遵守规则
4. 崩溃意识（Crash Awareness）- 学会预测和应对极端事件
5. 快速止损（Quick Stops）- 错误时立刻认输

核心投资原则：
1. "我只在能赚钱的时候交易"
2. "最重要的交易规则是保护本金"
3. "如果你对了，赚足够多；如果你错了，立刻出局"
4. "不要让任何一笔交易让你出局"
5. "关注宏观主题，理解资金流向"

决策启发式：
1. 首先判断宏观环境（通胀/通缩、增长/衰退）
2. 找到受益的资产类别
3. 计算风险回报比
4. 设置严格的止损点
5. 如果市场证明你错了，承认并退出

反模式（Jones 绝对不会做的事）：
- 不会让亏损头寸持有过夜
- 不会忽视技术面突破
- 不会逆大趋势交易
- 不会重仓赌单一判断

诚实边界：
- 高杠杆操作风险极大
- 需要强大的心理承受能力
- 宏观预测准确率有限
"""

from typing import Dict, List

class PaulTudorJonesDistilled:
    """
    蒸馏后的 Paul Tudor Jones 思维框架
    """
    
    def __init__(self):
        self.name = "Paul Tudor Jones"
        self.philosophy = "Macro Analysis + Risk Management + Crash Prediction"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "macro_signal": "neutral",
            "reasoning": [],
            "risk_reward": {},
            "crash_indicators": [],
            "position_guidance": {}
        }
        
        # 评估宏观信号
        macro = self._assess_macro(data)
        result["macro_signal"] = macro
        
        # 评估风险回报
        risk_reward = self._assess_risk_reward(data)
        result["risk_reward"] = risk_reward
        
        # 崩溃指标检查
        crash_indicators = self._check_crash_indicators(data)
        result["crash_indicators"] = crash_indicators
        
        # 仓位指导
        position = self._calculate_position(data, macro, risk_reward)
        result["position_guidance"] = position
        
        # 综合评分
        total_score = (
            macro["score"] * 0.35 +
            risk_reward["score"] * 0.30 +
            (100 - position["risk_score"]) * 0.35
        )
        
        # 崩溃风险调整
        if len(crash_indicators) >= 3:
            total_score *= 0.7  # 降低仓位建议
        
        if total_score >= 70:
            result["signal"] = "bullish" if macro["direction"] == "bullish" else "bearish"
            result["confidence"] = min(90, total_score)
        elif total_score <= 40:
            result["signal"] = "neutral"
            result["confidence"] = max(30, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        result["reasoning"] = self._generate_reasoning(result, macro, risk_reward)
        
        return result
    
    def _assess_macro(self, data: Dict) -> Dict:
        """评估宏观环境"""
        macro = {
            "score": 50,
            "direction": "neutral",
            "theme": "unknown",
            "key_factors": []
        }
        
        # 通胀环境
        inflation = data.get("inflation_trend", "neutral")
        if inflation == "rising":
            macro["score"] += 15
            macro["key_factors"].append("通胀上升")
        elif inflation == "falling":
            macro["score"] -= 10
            macro["key_factors"].append("通胀下降")
        
        # 增长环境
        growth = data.get("growth_trend", "neutral")
        if growth == "rising":
            macro["score"] += 10
            macro["key_factors"].append("增长上升")
        elif growth == "falling":
            macro["score"] -= 10
            macro["key_factors"].append("增长下降")
        
        # 央行政策
        if data.get("fed_pivot", False):
            macro["score"] += 20
            macro["key_factors"].append("央行转向")
        
        # 判断方向
        if macro["score"] > 60:
            macro["direction"] = "bullish"
            macro["theme"] = "风险资产友好"
        elif macro["score"] < 40:
            macro["direction"] = "bearish"
            macro["theme"] = "避险环境"
        else:
            macro["direction"] = "neutral"
            macro["theme"] = "不明朗"
        
        return macro
    
    def _assess_risk_reward(self, data: Dict) -> Dict:
        """评估风险回报"""
        rr = {
            "score": 50,
            "upside_pct": 0,
            "downside_pct": 0,
            "ratio": 0
        }
        
        upside = data.get("upside_to_target", 0.15)
        downside = data.get("downside_risk", 0.10)
        
        rr["upside_pct"] = upside * 100
        rr["downside_pct"] = downside * 100
        
        if downside > 0:
            rr["ratio"] = upside / downside
        
        # 评分
        if rr["ratio"] > 3:
            rr["score"] = 85
        elif rr["ratio"] > 2:
            rr["score"] = 70
        elif rr["ratio"] > 1.5:
            rr["score"] = 60
        elif rr["ratio"] > 1:
            rr["score"] = 50
        else:
            rr["score"] = 35
        
        return rr
    
    def _check_crash_indicators(self, data: Dict) -> List[str]:
        """检查崩溃预警指标"""
        indicators = []
        
        # VIX极端值
        vix = data.get("vix", 20)
        if vix > 30:
            indicators.append("VIX极高 (>30) - 市场恐慌")
        elif vix > 25:
            indicators.append("VIX偏高 (>25) - 注意风险")
        
        # 信用利差扩大
        if data.get("credit_spread_widening", False):
            indicators.append("信用利差扩大 - 风险偏好下降")
        
        # 债市倒挂
        if data.get("yield_curve_inverted", False):
            indicators.append("收益率曲线倒挂 - 衰退预警")
        
        # 过度杠杆
        if data.get("margin_debt_high", False):
            indicators.append("融资余额过高 - 市场脆弱")
        
        # 技术面破位
        if data.get("support_breakdown", False):
            indicators.append("关键技术支撑破位")
        
        return indicators
    
    def _calculate_position(self, data: Dict, macro: Dict, risk_reward: Dict) -> Dict:
        """计算仓位指导"""
        pos = {
            "recommended_pct": 5,
            "stop_loss_pct": 2.0,
            "risk_score": 50,
            "time_horizon": "medium"
        }
        
        # 基于宏观调整
        if macro["direction"] == "bullish":
            pos["recommended_pct"] += 5
        elif macro["direction"] == "bearish":
            pos["recommended_pct"] -= 5
        
        # 基于风险回报调整
        if risk_reward["ratio"] > 2:
            pos["recommended_pct"] += 3
        
        # 基于崩溃指标调整
        crash_count = len(data.get("crash_indicators", []))
        if crash_count >= 3:
            pos["recommended_pct"] *= 0.5
            pos["risk_score"] = 80
        elif crash_count >= 1:
            pos["recommended_pct"] *= 0.75
            pos["risk_score"] = 60
        
        # 止损设置
        pos["stop_loss_pct"] = data.get("atr_percent", 5.0) * 2
        
        return pos
    
    def _generate_reasoning(self, result: Dict, macro: Dict, risk_reward: Dict) -> List[str]:
        """生成推理"""
        reasoning = []
        
        reasoning.append(f"宏观: {macro['theme']} ({macro['score']:.0f}/100)")
        reasoning.append(f"风险回报: {risk_reward['ratio']:.1f}:1 ({risk_reward['score']:.0f}/100)")
        
        if result["crash_indicators"]:
            reasoning.append(f"崩溃预警: {len(result['crash_indicators'])}个指标触发")
        
        pos = result["position_guidance"]
        reasoning.append(f"建议仓位: {pos['recommended_pct']:.0f}%")
        reasoning.append(f"止损: {pos['stop_loss_pct']:.1f}%")
        
        return reasoning


def create_jones_agent() -> PaulTudorJonesDistilled:
    return PaulTudorJonesDistilled()
