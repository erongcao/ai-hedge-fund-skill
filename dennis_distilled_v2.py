#!/usr/bin/env python3
"""
Richard Dennis 思维框架蒸馏 - 女娲版 v2

核心理念：海龟交易法则 + 趋势追踪 + 系统化机械执行

身份卡:
- 芝加哥期货交易员，被称为"期货交易王子"
- 400美元起家，20年间做到2亿美元
- 海龟交易实验创始人（1983-1984）
- 证明交易技能可以被系统化教授

心智模型（6个核心镜片）：
1. 趋势追踪（Trend Following）- "让利润奔跑，截断亏损"
2. 系统化交易（Systematic Trading）- 用规则代替直觉
3. N倍波动率风险管理（N-Risk Management）- 基于ATR的动态仓位
4. 金字塔加仓（Pyramiding）- 趋势确认后逐步加仓
5. 机械执行（Mechanical Execution）- 消除情绪干扰
6. 分散化（Diversification）- 多市场降低单一风险

决策启发式（8条核心规则）：
1. "突破20日高低点 = 入场信号"
2. "2N止损 = 绝对纪律，不问原因"
3. "单笔风险 ≤ 账户的2%"
4. "最多4个单位加仓，每个单位间隔1/2 N"
5. "10日低点出场（短线）/ 20日低点出场（长线）"
6. "不要预测顶部和底部，跟随趋势"
7. "如果止损被触发，趋势可能已反转"
8. "市场噪音中，坚持系统信号"

表达DNA:
- 简洁直接，不绕弯子
- 用数据和规则说话，不用形容词
- 经典句式："如果...那么..." 的条件逻辑
- 承认不确定性："我不知道...但我知道..."
- 实用主义："关键是执行，不是预测"

价值观排序:
1. 纪律 > 判断力
2. 风险控制 > 收益最大化
3. 一致性 > 灵活性
4. 长期期望 > 单笔结果

反模式（Dennis 绝对不会做的事）：
- 不会逆势交易
- 不会在止损点犹豫或修改
- 不会因为连续亏损而改变系统
- 不会重仓单一头寸
- 不会预测市场"应该"去哪里
- 不会让情绪影响交易决策

诚实边界:
- 趋势追踪在震荡市场会连续亏损
- 需要承受30-50%的回撤才能换取长期收益
- 系统需要足够资金承受多次连续止损
- 严格执行需要极强的心理承受力
- 1987年股灾和后续年份Dennis自己也遭遇了重大回撤
- 不同市场环境可能需要调整参数

时间线关键节点:
- 1970s: 400美元起步，在芝加哥期货交易所做跑腿员
- 1974: 成立C&D Commodities
- 1983-1984: 海龟交易实验，招募23名学员
- 1986: 海龟实验结束，许多学员成为成功交易员
- 1987: 股灾中遭受重大损失
- 1990s: 管理资金规模下降，逐渐淡出
- 2000s: 退休，专注于其他投资

智识谱系:
- 受影响：Richard Donchian（唐奇安通道之父）
- 合作者：William Eckhardt（海龟实验共同发起人）
- 影响者：海龟学员（Curtis Faith, Jerry Parker等）
- 流派：与Ed Seykota、Bill Dunn同属趋势追踪派

调研来源:
- 《海龟交易法则》(Way of the Turtle) - Curtis Faith
- 《趋势跟踪》(Trend Following) - Michael Covel
- 《新市场巫师》(The New Market Wizards) - Jack Schwager访谈
- Original Turtle Trading Rules (公开文档)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class TrendDirection(Enum):
    """趋势方向"""
    UP = "up"
    DOWN = "down"
    NEUTRAL = "neutral"


class Timeframe(Enum):
    """交易时间框架"""
    SHORT_TERM = "short"    # 20日突破系统
    LONG_TERM = "long"      # 55日突破系统


@dataclass
class TurtlePosition:
    """海龟仓位单位"""
    entry_price: float = 0.0
    stop_loss: float = 0.0
    units: int = 0
    max_units: int = 4
    n_value: float = 0.0  # ATR(20)
    
    def can_add_unit(self) -> bool:
        """是否可以加仓"""
        return self.units < self.max_units
    
    def next_entry_price(self) -> float:
        """下一个加仓点位（间隔1/2 N）"""
        if self.units == 0:
            return 0.0
        return self.entry_price + (self.units * 0.5 * self.n_value)


@dataclass
class RiskParameters:
    """风险管理参数（Dennis标准）"""
    account_risk_per_trade: float = 0.02  # 单笔2%风险
    max_correlated_positions: int = 6     # 最多6个相关头寸
    max_total_units: int = 12             # 总仓位上限
    stop_loss_multiple: float = 2.0       # 2N止损
    
    def calculate_position_size(self, account_value: float, n_value: float) -> float:
        """
        计算仓位大小
        公式: 账户价值的1% / N值 = 每N单位的合约数量
        """
        if n_value <= 0:
            return 0.0
        dollar_risk = account_value * self.account_risk_per_trade
        risk_per_unit = n_value * self.stop_loss_multiple
        return dollar_risk / risk_per_unit if risk_per_unit > 0 else 0.0


class RichardDennisDistilled:
    """
    蒸馏后的 Richard Dennis (海龟交易法) 思维框架 - 女娲版 v2
    
    HOW Dennis thinks, not WHAT he said.
    
    核心洞察：Dennis相信交易不是艺术而是科学，
    成功的关键在于严格的系统执行和风险管理，
    而不是预测市场的能力。
    """
    
    def __init__(self):
        self.name = "Richard Dennis"
        self.philosophy = "Trend Following + Systematic Rules + Mechanical Execution"
        self.nickname = "Prince of the Pit"
        self.timeframe = Timeframe.SHORT_TERM
        
        # 标准风险管理参数
        self.risk_params = RiskParameters()
        
        # 心智模型列表
        self.mental_models = [
            "trend_following",      # 趋势追踪
            "systematic_trading",   # 系统化交易
            "n_risk_management",    # N倍波动率风险管理
            "pyramiding",           # 金字塔加仓
            "mechanical_execution", # 机械执行
            "diversification"       # 分散化
        ]
    
    def analyze(self, data: Dict, account_value: float = 100000.0) -> Dict:
        """
        使用 Dennis 的心智模型分析市场数据
        
        Args:
            data: 市场数据字典
            account_value: 账户总价值（用于仓位计算）
            
        Returns:
            包含信号、信心度、推理和建议的字典
        """
        result = {
            "agent": self.name,
            "philosophy": self.philosophy,
            "signal": "neutral",
            "confidence": 50,
            "trend_score": 0,
            "trend_direction": "neutral",
            "entry_signals": [],
            "exit_signals": [],
            "position_guidance": {},
            "risk_assessment": {},
            "reasoning": [],
            "key_insights": [],
            "red_flags": [],
            "mental_models_applied": [],
            "execution_rules": []
        }
        
        # 1. 应用心智模型：趋势追踪
        trend_analysis = self._apply_trend_following(data)
        result["trend_score"] = trend_analysis["score"]
        result["trend_direction"] = trend_analysis["direction"]
        result["mental_models_applied"].append("trend_following")
        
        # 2. 应用心智模型：系统化交易 - 识别入场信号
        entry_signals = self._apply_systematic_entry(data, trend_analysis)
        result["entry_signals"] = entry_signals
        result["mental_models_applied"].append("systematic_trading")
        
        # 3. 应用心智模型：N倍风险管理
        risk_analysis = self._apply_n_risk_management(data, account_value)
        result["risk_assessment"] = risk_analysis
        result["mental_models_applied"].append("n_risk_management")
        
        # 4. 应用心智模型：金字塔加仓
        pyramiding = self._apply_pyramiding(data, entry_signals, risk_analysis)
        result["position_guidance"] = pyramiding
        result["mental_models_applied"].append("pyramiding")
        
        # 5. 识别出场信号
        exit_signals = self._identify_exit_signals(data, risk_analysis)
        result["exit_signals"] = exit_signals
        
        # 6. 综合评分与信号生成
        signal_result = self._generate_signal(
            trend_analysis, 
            entry_signals, 
            risk_analysis,
            exit_signals
        )
        result["signal"] = signal_result["signal"]
        result["confidence"] = signal_result["confidence"]
        
        # 7. 生成推理和洞察
        result["reasoning"] = self._generate_reasoning(result, data)
        result["key_insights"] = self._generate_key_insights(result, data)
        result["red_flags"] = self._identify_red_flags(result, data)
        result["execution_rules"] = self._generate_execution_rules(result)
        
        return result
    
    def _apply_trend_following(self, data: Dict) -> Dict:
        """
        心智模型1：趋势追踪
        
        Dennis的核心信念：
        - 不要预测趋势，跟随趋势
        - 趋势一旦形成，倾向于继续
        - 让利润奔跑，截断亏损
        """
        trend = {
            "score": 50,
            "direction": "neutral",
            "strength": 0,
            "breakout_20d": False,
            "breakout_55d": False,
            "breakdown_20d": False,
            "breakdown_55d": False
        }
        
        price = data.get("current_price", 0)
        
        # 20日突破系统（短线）
        high_20d = data.get("high_20d", 0)
        low_20d = data.get("low_20d", 0)
        
        if price > 0 and high_20d > 0 and price > high_20d:
            trend["breakout_20d"] = True
            trend["direction"] = "up"
            trend["score"] += 30
        elif price > 0 and low_20d > 0 and price < low_20d:
            trend["breakdown_20d"] = True
            trend["direction"] = "down"
            trend["score"] -= 30
        
        # 55日突破系统（长线）
        high_55d = data.get("high_55d", 0)
        low_55d = data.get("low_55d", 0)
        
        if price > 0 and high_55d > 0 and price > high_55d:
            trend["breakout_55d"] = True
            trend["direction"] = "up"
            trend["score"] += 20  # 额外加分
        elif price > 0 and low_55d > 0 and price < low_55d:
            trend["breakdown_55d"] = True
            trend["direction"] = "down"
            trend["score"] -= 20
        
        # 均线排列确认趋势强度
        ma_20 = data.get("ma_20", 0)
        ma_55 = data.get("ma_55", 0)
        
        if ma_20 > 0 and ma_55 > 0:
            if price > ma_20 > ma_55:
                trend["strength"] = 80 if trend["breakout_20d"] else 60
            elif price < ma_20 < ma_55:
                trend["strength"] = 80 if trend["breakdown_20d"] else 60
            else:
                trend["strength"] = 40
        
        # ATR确认波动足够
        atr_percent = data.get("atr_percent", 10)
        if atr_percent > 5:
            trend["score"] += 5
        elif atr_percent < 2:
            trend["score"] -= 10  # 波动太低，趋势可能不明显
        
        trend["score"] = max(10, min(95, trend["score"]))
        
        return trend
    
    def _apply_systematic_entry(self, data: Dict, trend: Dict) -> List[Dict]:
        """
        心智模型2：系统化交易
        
        Dennis的方法：
        - 用明确的规则代替主观判断
        - 突破 = 入场，不问原因
        - 系统信号优先于直觉
        """
        signals = []
        
        # 入场信号1：20日突破
        if trend["breakout_20d"]:
            signals.append({
                "type": "entry",
                "signal": "breakout_20d_high",
                "priority": "high",
                "description": "突破20日高点 - 短线入场信号",
                "rule": "IF price > 20d_high THEN enter_long"
            })
        elif trend["breakdown_20d"]:
            signals.append({
                "type": "entry",
                "signal": "breakdown_20d_low",
                "priority": "high",
                "description": "跌破20日低点 - 短线做空信号",
                "rule": "IF price < 20d_low THEN enter_short"
            })
        
        # 入场信号2：55日突破（更强信号）
        if trend["breakout_55d"]:
            signals.append({
                "type": "entry",
                "signal": "breakout_55d_high",
                "priority": "very_high",
                "description": "突破55日高点 - 长线入场信号",
                "rule": "IF price > 55d_high THEN enter_long (stronger)"
            })
        elif trend["breakdown_55d"]:
            signals.append({
                "type": "entry",
                "signal": "breakdown_55d_low",
                "priority": "very_high",
                "description": "跌破55日低点 - 长线做空信号",
                "rule": "IF price < 55d_low THEN enter_short (stronger)"
            })
        
        # 入场信号3：趋势确认 + 成交量
        if trend["strength"] > 70 and data.get("volume_confirmation", False):
            signals.append({
                "type": "confirmation",
                "signal": "trend_volume_confirm",
                "priority": "medium",
                "description": "趋势确认 + 成交量放大",
                "rule": "IF trend_strength > 70 AND volume > avg THEN confirm"
            })
        
        return signals
    
    def _apply_n_risk_management(self, data: Dict, account_value: float) -> Dict:
        """
        心智模型3：N倍波动率风险管理
        
        Dennis的风险公式：
        - N = ATR(20)，代表每日平均波动
        - 止损 = 2N
        - 仓位 = 账户1% / N值
        - 单笔最大风险 = 账户2%
        """
        risk = {
            "n_value": 0.0,
            "atr_percent": 0.0,
            "stop_loss_2n": 0.0,
            "position_size_units": 0.0,
            "dollar_risk": 0.0,
            "risk_rating": "medium",
            "recommended_stop_pct": 2.0
        }
        
        price = data.get("current_price", 0)
        atr = data.get("atr_20", 0)
        
        if price > 0 and atr > 0:
            risk["n_value"] = atr
            risk["atr_percent"] = (atr / price) * 100
            risk["stop_loss_2n"] = price - (2 * atr)  # 假设多头
            
            # 计算仓位大小
            dollar_risk = account_value * self.risk_params.account_risk_per_trade
            risk["dollar_risk"] = dollar_risk
            
            # N单位数量
            risk_per_n = atr * self.risk_params.stop_loss_multiple
            if risk_per_n > 0:
                risk["position_size_units"] = dollar_risk / risk_per_n
        
        # 风险评级
        if risk["atr_percent"] > 8:
            risk["risk_rating"] = "very_high"
            risk["recommended_stop_pct"] = 1.5
        elif risk["atr_percent"] > 5:
            risk["risk_rating"] = "high"
            risk["recommended_stop_pct"] = 2.0
        elif risk["atr_percent"] > 3:
            risk["risk_rating"] = "medium"
            risk["recommended_stop_pct"] = 2.0
        else:
            risk["risk_rating"] = "low"
            risk["recommended_stop_pct"] = 2.5
        
        return risk
    
    def _apply_pyramiding(self, data: Dict, entry_signals: List[Dict], 
                         risk: Dict) -> Dict:
        """
        心智模型4：金字塔加仓
        
        Dennis的加仓规则：
        - 最多4个单位
        - 每个单位间隔1/2 N
        - 每个单位的风险相同（2%）
        - 第一个单位盈利后才加第二个
        """
        position = {
            "max_units": 4,
            "current_units": 0,
            "entry_prices": [],
            "stop_losses": [],
            "add_unit_interval": 0.0,
            "total_exposure_pct": 0.0,
            "next_add_price": 0.0,
            "can_pyramid": False
        }
        
        if not entry_signals or risk["n_value"] <= 0:
            return position
        
        price = data.get("current_price", 0)
        n_value = risk["n_value"]
        
        # 加仓间隔 = 1/2 N
        position["add_unit_interval"] = 0.5 * n_value
        
        # 第一单位入场价
        if entry_signals[0]["type"] == "entry":
            entry_price = price
            position["entry_prices"].append(entry_price)
            position["current_units"] = 1
            position["stop_losses"].append(entry_price - 2 * n_value)
            position["can_pyramid"] = True
            
            # 计算后续加仓点位
            for i in range(1, 4):
                add_price = entry_price + (i * 0.5 * n_value)
                position["entry_prices"].append(add_price)
                position["stop_losses"].append(add_price - 2 * n_value)
            
            position["next_add_price"] = position["entry_prices"][1]
            
            # 总风险暴露（假设全部加仓）
            position["total_exposure_pct"] = 4 * self.risk_params.account_risk_per_trade * 100
        
        return position
    
    def _identify_exit_signals(self, data: Dict, risk: Dict) -> List[Dict]:
        """
        出场信号识别
        
        Dennis的出场规则：
        - 2N止损（硬性止损）
        - 10日低点出场（短线系统）
        - 20日低点出场（长线系统）
        - 趋势破坏信号
        """
        signals = []
        price = data.get("current_price", 0)
        
        # 出场信号1：2N止损
        if risk["n_value"] > 0 and price > 0:
            stop_2n = price - (2 * risk["n_value"])
            signals.append({
                "type": "stop_loss",
                "signal": "2n_stop",
                "priority": "critical",
                "price": stop_2n,
                "description": f"2N止损位: {stop_2n:.2f}",
                "rule": "IF price <= entry - 2N THEN exit_immediately"
            })
        
        # 出场信号2：10日低点（短线）
        low_10d = data.get("low_10d", 0)
        if low_10d > 0:
            signals.append({
                "type": "exit",
                "signal": "10d_low_exit",
                "priority": "high",
                "price": low_10d,
                "description": f"跌破10日低点出场: {low_10d:.2f}",
                "rule": "IF price < 10d_low AND short_term_system THEN exit"
            })
        
        # 出场信号3：20日低点（长线）
        low_20d = data.get("low_20d", 0)
        if low_20d > 0:
            signals.append({
                "type": "exit",
                "signal": "20d_low_exit",
                "priority": "medium",
                "price": low_20d,
                "description": f"跌破20日低点出场: {low_20d:.2f}",
                "rule": "IF price < 20d_low AND long_term_system THEN exit"
            })
        
        # 出场信号4：趋势破坏
        if data.get("ma_cross_down", False):
            signals.append({
                "type": "exit",
                "signal": "trend_break",
                "priority": "high",
                "description": "均线死叉 - 趋势破坏",
                "rule": "IF MA_cross_down THEN exit"
            })
        
        # 出场信号5：反向突破
        if data.get("breakout_20d_high", False):  # 如果是空头，向上突破是出场信号
            signals.append({
                "type": "exit",
                "signal": "opposite_breakout",
                "priority": "high",
                "description": "反向突破 - 可能的趋势反转",
                "rule": "IF opposite_direction_breakout THEN exit"
            })
        
        return signals
    
    def _generate_signal(self, trend: Dict, entry_signals: List[Dict],
                        risk: Dict, exit_signals: List[Dict]) -> Dict:
        """生成最终交易信号"""
        result = {
            "signal": "neutral",
            "confidence": 50
        }
        
        # 基础分数
        base_score = trend["score"]
        
        # 入场信号加分
        entry_bonus = 0
        for sig in entry_signals:
            if sig["priority"] == "very_high":
                entry_bonus += 15
            elif sig["priority"] == "high":
                entry_bonus += 10
            elif sig["priority"] == "medium":
                entry_bonus += 5
        
        # 风险调整
        risk_adjustment = 0
        if risk["risk_rating"] == "very_high":
            risk_adjustment = -15
        elif risk["risk_rating"] == "high":
            risk_adjustment = -5
        elif risk["risk_rating"] == "low":
            risk_adjustment = 5
        
        # 出场信号扣分（如果有强出场信号，降低入场意愿）
        exit_penalty = 0
        for sig in exit_signals:
            if sig["priority"] == "critical":
                exit_penalty = -30
                break
            elif sig["priority"] == "high":
                exit_penalty = -10
        
        total_score = base_score + entry_bonus + risk_adjustment + exit_penalty
        total_score = max(10, min(95, total_score))
        
        # 确定信号
        if total_score >= 70 and len([s for s in entry_signals if s["type"] == "entry"]) > 0:
            result["signal"] = "bullish" if trend["direction"] == "up" else "bearish"
            result["confidence"] = min(90, total_score)
        elif total_score <= 40:
            result["signal"] = "neutral"
            result["confidence"] = max(30, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        return result
    
    def _generate_reasoning(self, result: Dict, data: Dict) -> List[str]:
        """生成Dennis风格的推理"""
        reasoning = []
        
        # 趋势分析
        direction = result["trend_direction"]
        trend_desc = "上升" if direction == "up" else "下降" if direction == "down" else "震荡"
        reasoning.append(f"[趋势] {trend_desc} (评分: {result['trend_score']:.0f}/100)")
        
        # 入场信号
        entry_count = len([s for s in result["entry_signals"] if s["type"] == "entry"])
        if entry_count > 0:
            reasoning.append(f"[入场] {entry_count}个系统信号触发")
        
        # 风险管理
        risk = result["risk_assessment"]
        reasoning.append(f"[风险] ATR: {risk.get('atr_percent', 0):.1f}% | 评级: {risk.get('risk_rating', 'unknown')}")
        
        # 仓位建议
        position = result["position_guidance"]
        if position.get("can_pyramid"):
            reasoning.append(f"[仓位] 可金字塔加仓，最多{position['max_units']}个单位")
        
        # 止损
        if risk.get("stop_loss_2n"):
            reasoning.append(f"[止损] 2N = {risk['stop_loss_2n']:.2f}")
        
        return reasoning
    
    def _generate_key_insights(self, result: Dict, data: Dict) -> List[str]:
        """生成核心洞察"""
        insights = []
        
        # 趋势洞察
        trend = result["trend_direction"]
        score = result["trend_score"]
        if score > 75:
            insights.append(f"强{trend}趋势确认，适合跟随")
        elif score < 40:
            insights.append("趋势不明朗，保持观望")
        
        # 突破洞察
        for sig in result["entry_signals"]:
            if sig["priority"] == "very_high":
                insights.append(f"55日突破 - 高置信度信号")
            elif sig["priority"] == "high":
                insights.append(f"20日突破 - 标准入场信号")
        
        # 风险洞察
        risk = result["risk_assessment"]
        if risk.get("risk_rating") == "very_high":
            insights.append("高波动率环境，需减小仓位")
        
        # 执行洞察
        if result["signal"] != "neutral":
            insights.append("信号触发，执行比判断更重要")
        
        return insights
    
    def _identify_red_flags(self, result: Dict, data: Dict) -> List[str]:
        """识别危险信号（反模式检查）"""
        flags = []
        
        # 震荡市场警告
        if result["trend_score"] < 45 and result["trend_score"] > 35:
            flags.append("震荡市场 - 趋势追踪可能连续止损")
        
        # 高波动警告
        risk = result["risk_assessment"]
        if risk.get("atr_percent", 0) > 10:
            flags.append("极高波动 - 单次止损可能过大")
        
        # 流动性警告
        if data.get("avg_volume", 0) < 100000:
            flags.append("流动性不足 - 可能影响执行")
        
        # 出场信号检查
        exit_critical = [s for s in result["exit_signals"] if s.get("priority") == "critical"]
        if exit_critical:
            flags.append("出场信号触发 - 已有头寸应考虑平仓")
        
        # 相关性警告（假设有多头寸）
        correlated_exposure = data.get("correlated_positions", 0)
        if correlated_exposure >= self.risk_params.max_correlated_positions:
            flags.append(f"相关头寸已达上限({self.risk_params.max_correlated_positions}) - 暂缓新开仓")
        
        return flags
    
    def _generate_execution_rules(self, result: Dict) -> List[str]:
        """生成执行规则（Dennis风格）"""
        rules = []
        
        if result["signal"] == "bullish":
            rules.append("1. 突破即入场，不等待回调")
            rules.append("2. 设2N止损，绝不移动止损位")
            rules.append("3. 盈利后每1/2N加一单位，最多4单位")
            rules.append("4. 跌破10日低点全部出场")
        elif result["signal"] == "bearish":
            rules.append("1. 跌破即入场做空")
            rules.append("2. 设2N止损（上方）")
            rules.append("3. 盈利后逐步加仓")
            rules.append("4. 突破10日高点全部出场")
        else:
            rules.append("1. 无系统信号，保持空仓观望")
            rules.append("2. 不要预测，等待突破")
        
        rules.append("5. 单笔风险不超过账户2%")
        rules.append("6. 机械执行，不问原因")
        
        return rules
    
    # ============ 公开API方法 ============
    
    def get_turtle_rules(self) -> Dict:
        """获取完整海龟交易规则"""
        return {
            "entry_rules": {
                "system_1_short_term": "突破20日高低点入场",
                "system_2_long_term": "突破55日高低点入场",
                "filter": "用55日系统过滤20日系统（同向才做）"
            },
            "exit_rules": {
                "system_1": "跌破10日低点出场",
                "system_2": "跌破20日低点出场",
                "stop_loss": "2N硬性止损"
            },
            "position_sizing": {
                "unit_calculation": "账户1% / N值",
                "max_units_per_market": 4,
                "max_correlated_positions": 6,
                "max_total_units": 12,
                "pyramiding_interval": "1/2 N"
            },
            "risk_management": {
                "risk_per_trade": "2% of account",
                "stop_loss_distance": "2N",
                "position_adjustment": "根据N值动态调整"
            },
            "markets": {
                "principle": "分散化交易多个市场",
                "include": "外汇、商品、债券、股指",
                "avoid": "流动性差的市场"
            }
        }
    
    def calculate_position_size(self, account_value: float, atr: float, 
                                price: float) -> Dict:
        """
        计算标准海龟仓位
        
        Returns:
            包含仓位信息的字典
        """
        return self.risk_params.calculate_position_size(account_value, atr)
    
    def get_max_loss_tolerance(self, num_positions: int = 1) -> str:
        """
        Dennis的最大损失容忍度
        
        Args:
            num_positions: 当前持仓数量
        """
        max_total_risk = num_positions * self.risk_params.account_risk_per_trade * 100
        return f"总风险暴露: {max_total_risk:.1f}% (单笔2% × {num_positions}个头寸)"
    
    def express_like_dennis(self, analysis: Dict) -> str:
        """
        用Dennis的风格表达分析结果（表达DNA模拟）
        """
        signal = analysis.get("signal", "neutral")
        confidence = analysis.get("confidence", 50)
        
        if signal == "bullish":
            if confidence > 80:
                return f"突破确认。N={analysis.get('risk_assessment', {}).get('n_value', 0):.2f}，仓位{self.risk_params.account_risk_per_trade*100:.0f}%，2N止损。执行。"
            else:
                return f"有突破迹象，但强度一般。等待确认或减小仓位。"
        elif signal == "bearish":
            return f"跌破支撑。做空，2N止损。不要问为什么。"
        else:
            return f"没有信号。等待。不要预测。"
    
    def get_mental_model_description(self, model_name: str) -> Dict:
        """获取心智模型详细描述"""
        models = {
            "trend_following": {
                "name": "趋势追踪",
                "description": "不预测顶部和底部，只跟随已形成的趋势",
                "evidence": ["海龟交易实验", "20年2亿美元业绩"],
                "application": "突破入场，趋势破坏出场",
                "limitation": "震荡市场会连续亏损"
            },
            "systematic_trading": {
                "name": "系统化交易",
                "description": "用明确的规则代替主观判断",
                "evidence": ["海龟实验证明了规则可复制"],
                "application": "机械执行系统信号",
                "limitation": "需要极强的纪律性"
            },
            "n_risk_management": {
                "name": "N倍波动率风险管理",
                "description": "基于ATR的动态仓位和止损",
                "evidence": ["海龟规则文档", "不同市场的统一标准"],
                "application": "2N止损，1%单位计算",
                "limitation": "极端波动时止损可能过大"
            },
            "pyramiding": {
                "name": "金字塔加仓",
                "description": "趋势确认后逐步增加仓位",
                "evidence": ["海龟4单位规则"],
                "application": "每1/2N加一单位",
                "limitation": "趋势快速反转时全部单位受损"
            },
            "mechanical_execution": {
                "name": "机械执行",
                "description": "消除情绪干扰，严格按规则执行",
                "evidence": ["Dennis强调执行比判断重要"],
                "application": "信号触发立即执行",
                "limitation": "难以做到完全无情绪"
            },
            "diversification": {
                "name": "分散化",
                "description": "多市场降低单一风险",
                "evidence": ["海龟交易20+个市场"],
                "application": "同时跟踪多个不相关市场",
                "limitation": "需要更多资金和精力"
            }
        }
        return models.get(model_name, {})


# 导出函数
def create_dennis_agent() -> RichardDennisDistilled:
    """创建Dennis思维框架实例"""
    return RichardDennisDistilled()


# 测试代码
if __name__ == "__main__":
    # 测试数据
    test_data = {
        "current_price": 150.0,
        "high_20d": 148.0,
        "low_20d": 142.0,
        "high_55d": 155.0,
        "low_55d": 135.0,
        "ma_20": 145.0,
        "ma_55": 140.0,
        "atr_20": 3.5,
        "atr_percent": 2.33,
        "volume_confirmation": True,
        "breakout_20d_high": True,
        "breakout_55d_high": False,
        "avg_volume": 500000
    }
    
    agent = RichardDennisDistilled()
    result = agent.analyze(test_data, account_value=100000)
    
    print("=" * 60)
    print(f"Richard Dennis 分析结果")
    print("=" * 60)
    print(f"信号: {result['signal']}")
    print(f"信心度: {result['confidence']:.1f}")
    print(f"\n推理:")
    for r in result['reasoning']:
        print(f"  • {r}")
    print(f"\n核心洞察:")
    for i in result['key_insights']:
        print(f"  → {i}")
    print(f"\n危险信号:")
    for f in result['red_flags']:
        print(f"  ⚠ {f}")
    print(f"\n执行规则:")
    for rule in result['execution_rules']:
        print(f"  {rule}")
    print(f"\nDennis风格表达:")
    print(f"  \"{agent.express_like_dennis(result)}\"")
