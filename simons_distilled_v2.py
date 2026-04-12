#!/usr/bin/env python3
"""
Jim Simons 思维框架蒸馏 - 女娲版 v2.0

核心理念：量化交易 + 数学模型 + 统计套利 + 数据驱动决策

心智模型：
1. 市场无效性狩猎（Market Inefficiency Hunting）- 寻找市场微观结构中的定价错误
2. 模式识别优先（Pattern Recognition First）- 数学家的本能：在噪声中寻找信号
3. 统计套利思维（Statistical Arbitrage Mindset）- 不追求单一巨大收益，追求大量微小优势的复利
4. 反直觉杠杆（Counter-Intuitive Leverage）- 只在有确定性优势时使用杠杆放大
5. 持续模型迭代（Continuous Model Evolution）- 市场会适应，模型必须持续进化

决策启发式：
1. 任何策略必须回测验证，但警惕过拟合
2. 交易成本会吞噬微小策略的利润，必须精确建模
3. 信号强度与置信度成正比，与持仓时间成反比
4. 分散化是免费的午餐，跨资产、跨地域、跨时间尺度
5. 当模型与直觉冲突时，相信模型
6. 黑天鹅事件比正态分布预测的更频繁，需要厚尾建模
7. 人才的数学天赋 > 金融经验，雇佣物理学家和数学家
8. 技术基础设施是护城河的一部分，速度和数据质量决定生死

反模式（Simons 绝对不会做的事）：
- 不会基于新闻、情绪或直觉做交易决策
- 不会持有长期投资头寸（他是日内/短期/高频）
- 不会忽视交易成本和滑点的影响
- 不会在没有严格统计验证的情况下部署策略
- 不会公开分享核心模型细节（保密是竞争优势）
- 不会让单一策略承担过大风险敞口
- 不会在模型失效时死守"信仰"

诚实边界：
- Renaissance/Medallion 的成功依赖独特的数据、基础设施和人才，无法完全复制
- 高频/量化策略有严格的市场容量限制，大资金无法简单复制小策略
- 个人投资者缺乏技术基础设施和数据优势
- 历史回测不等于未来表现，市场结构变化可能使模型失效
- 即使是 Simons，也有策略亏损的时期
- 本框架提供的是思维参考，不是可直接套用的交易系统

智识谱系：
- 影响：James Ax（数学家）、Elwyn Berlekamp（信息论）、Leonard Baum（隐马尔可夫模型）
- 被影响：量化交易行业、对冲基金行业、数据科学领域
- 同辈：Ed Thorp（最早量化投资者）、David Shaw（DE Shaw）、Ray Dalio（桥水）
- 区别：Simons 更纯粹的数学驱动，Thorp 偏重博弈论，Dalio 偏重宏观逻辑

内在张力：
- 科学严谨 vs 商业保密：追求学术发表的本能 vs 保护alpha的需要
- 系统化 vs 人工干预：完全自动化 vs 必要时人工覆盖
- 短期收益 vs 长期模型健康：榨取当前alpha vs 保护策略寿命
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class SignalType(Enum):
    """交易信号类型"""
    STATISTICAL_ARBITRAGE = "statistical_arbitrage"
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    VOLATILITY_ARBITRAGE = "volatility_arbitrage"
    CROSS_ASSET_CORRELATION = "cross_asset_correlation"


@dataclass
class QuantStrategyMetrics:
    """量化策略核心指标"""
    # 信号质量
    sharpe_ratio: float = 0.0
    information_ratio: float = 0.0
    win_rate: float = 0.0
    
    # 风险指标
    max_drawdown: float = 0.0
    volatility: float = 0.0
    var_95: float = 0.0  # 95% VaR
    
    # 执行指标
    avg_holding_period_days: float = 0.0
    turnover_annual: float = 0.0  # 年换手率
    transaction_cost_impact: float = 0.0  # 交易成本对收益的影响
    
    # 容量指标
    strategy_capacity_usd: float = 0.0  # 策略容量（美元）
    market_impact_estimate: float = 0.0  # 市场冲击估计
    
    # 统计验证
    backtest_periods: int = 0  # 回测周期数
    out_of_sample_tests: int = 0  # 样本外测试次数
    overfitting_risk: str = "unknown"  # low/medium/high


class JimSimonsDistilled:
    """
    蒸馏后的 Jim Simons (Renaissance Technologies) 思维框架
    
    HOW he thinks, not WHAT he says.
    
    Simons 是数学家出身的量化交易先驱，他的核心贡献是证明了：
    1. 市场存在可以被数学模型捕捉的微观无效性
    2. 大量微弱优势的复利可以产生卓越回报
    3. 数据和基础设施是量化交易的护城河
    """
    
    def __init__(self):
        self.name = "Jim Simons"
        self.philosophy = "Pattern Recognition + Statistical Arbitrage + Data-Driven Models"
        self.fund = "Renaissance Technologies (Medallion Fund)"
        
        # 核心心智模型
        self.mental_models = {
            "market_inefficiency_hunting": {
                "description": "寻找市场微观结构中的定价错误，而非宏观预测",
                "time_horizon": "short_term",
                "confidence_required": "high"
            },
            "pattern_recognition_first": {
                "description": "数学家的本能：在噪声中寻找统计显著的信号",
                "approach": "data_mining_with_statistical_validation"
            },
            "statistical_arbitrage_mindset": {
                "description": "不追求单一巨大收益，追求大量微小优势的复利",
                "trade_count": "high",
                "edge_per_trade": "small_but_consistent"
            },
            "counter_intuitive_leverage": {
                "description": "只在有确定性优势时使用杠杆放大",
                "condition": "when_model_confidence_exceeds_threshold"
            },
            "continuous_model_evolution": {
                "description": "市场会适应，模型必须持续进化和迭代",
                "half_life": "models_degrade_over_time"
            }
        }
        
        # 决策启发式
        self.decision_heuristics = [
            "任何策略必须回测验证，但警惕过拟合",
            "交易成本会吞噬微小策略的利润，必须精确建模",
            "信号强度与置信度成正比，与持仓时间成反比",
            "分散化是免费的午餐，跨资产、跨地域、跨时间尺度",
            "当模型与直觉冲突时，相信模型",
            "黑天鹅事件比正态分布预测的更频繁，需要厚尾建模",
            "人才的数学天赋 > 金融经验，雇佣物理学家和数学家",
            "技术基础设施是护城河的一部分"
        ]
    
    def analyze(self, data: Dict) -> Dict:
        """
        使用 Simons 的心智模型分析市场/策略
        
        Args:
            data: 包含市场数据或策略数据的字典
            
        Returns:
            分析结果字典，包含信号、置信度、推理过程
        """
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "reasoning": [],
            "key_insights": [],
            "red_flags": [],
            "quant_metrics": {},
            "recommended_approach": "quantitative_analysis_required"
        }
        
        # 执行核心检查清单
        checklist = self._simons_checklist(data)
        
        # 1. 市场无效性评估
        inefficiency_score = self._assess_market_inefficiency(data, checklist)
        
        # 2. 数据质量评估
        data_quality_score = self._assess_data_quality(data, checklist)
        
        # 3. 策略统计验证评估
        statistical_validation_score = self._assess_statistical_validation(data, checklist)
        
        # 4. 执行可行性评估
        execution_feasibility_score = self._assess_execution_feasibility(data, checklist)
        
        # 5. 风险评估
        risk_score = self._assess_quant_risks(data, checklist)
        
        # 综合评分（Simons 的权重偏好）
        total_score = (
            inefficiency_score * 0.25 +          # 市场无效性是机会来源
            data_quality_score * 0.20 +           # 数据是模型的基础
            statistical_validation_score * 0.25 + # 统计验证是核心
            execution_feasibility_score * 0.15 +  # 执行决定能否捕获alpha
            risk_score * 0.15                     # 风险控制
        )
        
        # 生成信号
        if total_score >= 70 and checklist["has_statistical_edge"]:
            result["signal"] = "bullish"
            result["confidence"] = min(90, total_score + 5)
            result["recommended_approach"] = "quantitative_strategy_viable"
        elif total_score <= 40 or not checklist["data_sufficient"]:
            result["signal"] = "neutral"
            result["confidence"] = max(20, total_score)
            result["recommended_approach"] = "insufficient_for_quantitative_approach"
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
            result["recommended_approach"] = "requires_further_validation"
        
        result["reasoning"] = self._generate_reasoning(checklist)
        result["key_insights"] = self._generate_key_insights(checklist, inefficiency_score)
        result["red_flags"] = self._identify_red_flags(checklist)
        result["quant_metrics"] = checklist
        
        return result
    
    def evaluate_strategy(self, strategy_data: Dict) -> Dict:
        """
        评估一个量化策略的可行性（Simons 式审查）
        
        Args:
            strategy_data: 策略数据字典
            
        Returns:
            策略评估结果
        """
        result = {
            "agent": self.name,
            "strategy_score": 0,
            "viability": "unknown",
            "warnings": [],
            "recommendations": [],
            "required_tests": [],
            "capacity_estimate": 0
        }
        
        # 基础检查清单
        checks = {
            "has_alpha_source": strategy_data.get("has_calculated_alpha", False),
            "has_risk_management": strategy_data.get("has_risk_rules", False),
            "has_backtest": strategy_data.get("backtest_completed", False),
            "out_of_sample_tested": strategy_data.get("oos_tested", False),
            "transaction_costs_modeled": strategy_data.get("tx_costs_included", False),
            "overfitting_checked": strategy_data.get("overfitting_analysis", False)
        }
        
        score = 50  # 基础分
        
        # Alpha 源检查
        if checks["has_alpha_source"]:
            alpha_persistence = strategy_data.get("alpha_persistence_months", 0)
            if alpha_persistence >= 12:
                score += 15
            elif alpha_persistence >= 6:
                score += 10
            else:
                score += 5
                result["warnings"].append("Alpha persistence insufficient for confidence")
        else:
            score -= 20
            result["warnings"].append("No clear alpha source identified")
        
        # 回测验证
        if checks["has_backtest"]:
            score += 10
            if checks["out_of_sample_tested"]:
                score += 10
            else:
                result["warnings"].append("No out-of-sample testing performed")
                result["required_tests"].append("Out-of-sample backtesting on unseen periods")
        else:
            score -= 15
            result["warnings"].append("Strategy lacks backtesting")
        
        # 过拟合检查
        if checks["overfitting_checked"]:
            score += 10
        else:
            result["warnings"].append("Overfitting analysis not performed")
            result["required_tests"].append("Parameter sensitivity analysis")
            result["required_tests"].append("Walk-forward analysis")
        
        # 风险管理
        if checks["has_risk_management"]:
            score += 10
            max_drawdown = strategy_data.get("max_drawdown", 0.5)
            if max_drawdown < 0.20:
                score += 10
            elif max_drawdown > 0.40:
                score -= 10
                result["warnings"].append("Drawdown exceeds acceptable threshold")
        else:
            score -= 15
            result["warnings"].append("No risk management framework")
        
        # 交易成本
        if checks["transaction_costs_modeled"]:
            score += 10
            cost_impact = strategy_data.get("cost_impact_on_returns", 0)
            if cost_impact > 0.30:  # 成本侵蚀超过30%的收益
                score -= 15
                result["warnings"].append("Transaction costs severely erode alpha")
        else:
            result["warnings"].append("Transaction costs not modeled - critical gap")
        
        # 持仓周期评估
        holding_period = strategy_data.get("avg_holding_period_days", 0)
        if holding_period < 1:
            score += 5  # 高频，需要基础设施
            result["warnings"].append("High-frequency requires significant infrastructure")
        elif holding_period < 5:
            score += 3  # 短期
        elif holding_period > 30:
            score -= 5  # 对Simons来说偏长期
            result["warnings"].append("Holding period longer than typical Simons approach")
        
        result["strategy_score"] = max(10, min(95, score))
        
        # 可行性判断
        if result["strategy_score"] >= 70 and len(result["warnings"]) <= 1:
            result["viability"] = "viable"
        elif result["strategy_score"] >= 50:
            result["viability"] = "requires_improvement"
        else:
            result["viability"] = "not_viable"
        
        # 容量估计
        result["capacity_estimate"] = self._estimate_strategy_capacity(strategy_data)
        
        # 推荐测试
        result["recommendations"] = [
            "Run out-of-sample backtesting on multiple unseen periods",
            "Test for overfitting using parameter randomization",
            "Verify transaction cost assumptions with live paper trading",
            "Assess strategy capacity and market impact",
            "Monitor for regime changes and model decay",
            "Implement real-time risk monitoring and kill switches"
        ]
        
        return result
    
    def generate_factor_checklist(self) -> Dict:
        """
        Simons 会检查的量化因子清单
        
        Returns:
            按类别组织的因子检查清单
        """
        return {
            "momentum_factors": {
                "description": "价格动量和趋势因子",
                "factors": [
                    "short_term_reversal (1-5 days)",
                    "medium_term_momentum (1-6 months)",
                    "earnings_momentum",
                    "analyst_revisions",
                    "price_acceleration"
                ],
                "expected_correlation": "moderate_with_trend"
            },
            "mean_reversion_factors": {
                "description": "价格回归均值的机会",
                "factors": [
                    "short_term_overreaction",
                    "pairs_trading_spreads",
                    "statistical_arbitrage_signals",
                    "volatility_mean_reversion"
                ],
                "time_horizon": "hours_to_days"
            },
            "volatility_factors": {
                "description": "波动率相关策略",
                "factors": [
                    "implied_vs_realized_vol_spread",
                    "volatility_smile_arbitrage",
                    "term_structure_trades",
                    "volatility_skew_exploitation"
                ],
                "risk_level": "high_requires_hedging"
            },
            "cross_asset_factors": {
                "description": "跨资产相关性和套利",
                "factors": [
                    "correlation_breakdown_trades",
                    "index_vs_constituents_arbitrage",
                    "cash_vs_futures_basis",
                    "etfs_vs_nav_premium_discount"
                ],
                "execution_speed": "critical"
            },
            "microstructure_factors": {
                "description": "市场微观结构信号",
                "factors": [
                    "order_flow_imbalance",
                    "bid_ask_dynamics",
                    "volume_profile_analysis",
                    "market_depth_changes"
                ],
                "data_frequency": "tick_or_minute"
            },
            "alternative_data_factors": {
                "description": "非传统数据源信号",
                "factors": [
                    "satellite_imagery_analysis",
                    "credit_card_transaction_trends",
                    "web_scraping_sentiment",
                    "supply_chain_data"
                ],
                "alpha_decay": "faster_as_adoption_increases"
            }
        }
    
    def _simons_checklist(self, data: Dict) -> Dict:
        """
        Simons 的核心检查清单
        
        Returns:
            完整的检查清单字典
        """
        checklist = {
            # 数据质量
            "data_sufficient": False,
            "data_frequency": data.get("data_frequency", "daily"),
            "data_history_years": data.get("data_history_years", 0),
            "data_quality_score": 0,
            
            # 市场特征
            "market_inefficiency_signals": [],
            "liquidity_adequate": False,
            "volatility_regime": data.get("volatility_regime", "normal"),
            
            # 统计验证
            "has_statistical_edge": False,
            "sharpe_ratio": data.get("sharpe_ratio", 0),
            "statistical_significance": data.get("p_value", 1.0),
            
            # 执行相关
            "transaction_costs_estimated": False,
            "avg_bid_ask_spread_bps": data.get("avg_bid_ask_spread_bps", 10),
            "market_impact_model": False,
            
            # 风险相关
            "max_drawdown": data.get("max_drawdown", 0.5),
            "tail_risk_hedged": False,
            "position_limits_set": False
        }
        
        # 数据质量评估
        if checklist["data_history_years"] >= 10:
            checklist["data_quality_score"] += 30
        elif checklist["data_history_years"] >= 5:
            checklist["data_quality_score"] += 20
        elif checklist["data_history_years"] >= 2:
            checklist["data_quality_score"] += 10
        
        if checklist["data_frequency"] in ["tick", "minute", "hourly"]:
            checklist["data_quality_score"] += 20
        elif checklist["data_frequency"] == "daily":
            checklist["data_quality_score"] += 10
        
        checklist["data_sufficient"] = checklist["data_quality_score"] >= 30
        
        # 统计边缘检测
        if checklist["sharpe_ratio"] > 1.5:
            checklist["has_statistical_edge"] = True
        elif checklist["sharpe_ratio"] > 1.0 and checklist["statistical_significance"] < 0.05:
            checklist["has_statistical_edge"] = True
        
        # 流动性评估
        avg_volume = data.get("avg_daily_volume_usd", 0)
        checklist["liquidity_adequate"] = avg_volume > 10e6  # >$10M daily
        
        return checklist
    
    def _assess_market_inefficiency(self, data: Dict, checklist: Dict) -> float:
        """
        评估市场无效性程度
        
        Args:
            data: 市场数据
            checklist: 检查清单
            
        Returns:
            无效性评分 (0-100)
        """
        score = 50  # 中性起点
        
        # 买卖价差（大价差=低效）
        bid_ask_spread = data.get("avg_bid_ask_spread_bps", 10)
        if bid_ask_spread > 20:
            score += 20
            checklist["market_inefficiency_signals"].append("wide_bid_ask_spreads")
        elif bid_ask_spread > 10:
            score += 10
        elif bid_ask_spread < 5:
            score -= 10
        
        # 波动率（高波动=更多机会）
        volatility = data.get("realized_volatility", 0.15)
        if volatility > 0.30:
            score += 15
            checklist["market_inefficiency_signals"].append("high_volatility_opportunity")
        elif volatility > 0.20:
            score += 10
        elif volatility < 0.10:
            score -= 10
        
        # 市场结构
        if data.get("has_limit_order_book", True):
            score += 10
            checklist["market_inefficiency_signals"].append("order_book_opportunities")
        
        if data.get("market_fragmented", False):
            score += 15
            checklist["market_inefficiency_signals"].append("fragmentation_arbitrage")
        
        # 投资者结构（散户多=更多情绪化定价）
        retail_pct = data.get("retail_trading_pct", 0.3)
        if retail_pct > 0.4:
            score += 15
            checklist["market_inefficiency_signals"].append("high_retail_participation")
        elif retail_pct < 0.2:
            score -= 10
        
        # 信息不对称程度
        if data.get("analyst_coverage", 10) < 5:
            score += 10
            checklist["market_inefficiency_signals"].append("low_analyst_coverage")
        
        return max(10, min(95, score))
    
    def _assess_data_quality(self, data: Dict, checklist: Dict) -> float:
        """评估数据质量"""
        score = checklist["data_quality_score"]
        
        # 数据完整性
        if data.get("data_completeness", 1.0) > 0.95:
            score += 10
        elif data.get("data_completeness", 1.0) < 0.80:
            score -= 15
        
        # 数据延迟
        latency_ms = data.get("data_latency_ms", 1000)
        if latency_ms < 10:
            score += 10  # 超低延迟
        elif latency_ms > 1000:
            score -= 10
        
        return max(0, min(100, score))
    
    def _assess_statistical_validation(self, data: Dict, checklist: Dict) -> float:
        """评估统计验证程度"""
        score = 50
        
        # Sharpe ratio
        sharpe = data.get("sharpe_ratio", 0)
        if sharpe > 2.0:
            score += 25
        elif sharpe > 1.5:
            score += 20
        elif sharpe > 1.0:
            score += 10
        elif sharpe < 0.5:
            score -= 20
        
        # 统计显著性
        p_value = data.get("p_value", 1.0)
        if p_value < 0.01:
            score += 15
        elif p_value < 0.05:
            score += 10
        elif p_value > 0.10:
            score -= 15
        
        # 样本量
        observations = data.get("observation_count", 0)
        if observations > 10000:
            score += 10
        elif observations < 1000:
            score -= 10
        
        return max(10, min(95, score))
    
    def _assess_execution_feasibility(self, data: Dict, checklist: Dict) -> float:
        """评估执行可行性"""
        score = 50
        
        # 流动性
        if checklist["liquidity_adequate"]:
            score += 20
        else:
            score -= 15
        
        # 交易成本建模
        if data.get("transaction_costs_modeled", False):
            score += 15
        
        # 市场冲击
        impact_bps = data.get("estimated_market_impact_bps", 10)
        if impact_bps < 5:
            score += 10
        elif impact_bps > 20:
            score -= 15
        
        # 滑点
        slippage_bps = data.get("avg_slippage_bps", 5)
        if slippage_bps < 3:
            score += 10
        elif slippage_bps > 10:
            score -= 10
        
        return max(10, min(90, score))
    
    def _assess_quant_risks(self, data: Dict, checklist: Dict) -> float:
        """评估量化风险"""
        score = 50
        
        # 最大回撤
        max_dd = data.get("max_drawdown", 0.5)
        if max_dd < 0.10:
            score += 20
        elif max_dd < 0.20:
            score += 10
        elif max_dd > 0.40:
            score -= 20
        elif max_dd > 0.30:
            score -= 10
        
        # 尾部风险
        skewness = data.get("return_skewness", 0)
        kurtosis = data.get("return_kurtosis", 3)
        if kurtosis > 4:  # 厚尾
            score -= 5  # 需要额外对冲
        
        # 策略相关性
        correlation_to_existing = data.get("correlation_to_existing", 0.5)
        if correlation_to_existing < 0.3:
            score += 10
        elif correlation_to_existing > 0.7:
            score -= 10
        
        return max(10, min(90, score))
    
    def _generate_reasoning(self, checklist: Dict) -> List[str]:
        """生成推理过程"""
        reasoning = []
        
        # 数据质量
        if checklist["data_sufficient"]:
            reasoning.append(f"Data quality: Sufficient ({checklist['data_history_years']:.1f} years)")
        else:
            reasoning.append("Data quality: Insufficient for reliable modeling")
        
        # 统计边缘
        if checklist["has_statistical_edge"]:
            reasoning.append(f"Statistical edge detected (Sharpe: {checklist['sharpe_ratio']:.2f})")
        else:
            reasoning.append("No clear statistical edge identified")
        
        # 市场无效性信号
        if checklist["market_inefficiency_signals"]:
            signals = ", ".join(checklist["market_inefficiency_signals"][:3])
            reasoning.append(f"Inefficiency signals: {signals}")
        
        # 流动性
        if checklist["liquidity_adequate"]:
            reasoning.append("Liquidity: Adequate for strategy execution")
        else:
            reasoning.append("Liquidity: May constrain strategy capacity")
        
        return reasoning
    
    def _generate_key_insights(self, checklist: Dict, inefficiency_score: float) -> List[str]:
        """生成核心洞察"""
        insights = []
        
        if inefficiency_score > 70:
            insights.append("High market inefficiency suggests quantitative opportunities exist")
        
        if checklist["has_statistical_edge"] and checklist["data_sufficient"]:
            insights.append("Strategy has statistical foundation but requires rigorous validation")
        
        if len(checklist["market_inefficiency_signals"]) >= 3:
            insights.append("Multiple inefficiency signals present - diversification potential")
        
        if not checklist["liquidity_adequate"]:
            insights.append("Limited liquidity will constrain strategy capacity")
        
        return insights
    
    def _identify_red_flags(self, checklist: Dict) -> List[str]:
        """识别危险信号"""
        flags = []
        
        if not checklist["data_sufficient"]:
            flags.append("Insufficient data history for reliable backtesting")
        
        if not checklist["has_statistical_edge"]:
            flags.append("No clear statistical edge - strategy may not be viable")
        
        if checklist["max_drawdown"] > 0.40:
            flags.append("Maximum drawdown exceeds risk tolerance")
        
        if not checklist["liquidity_adequate"]:
            flags.append("Inadequate liquidity for intended position sizes")
        
        flags.append("Model overfitting risk - historical backtest may not predict future")
        flags.append("Market regime change risk - patterns that worked before may stop working")
        flags.append("Transaction costs can erode small statistical edges")
        flags.append("Black swan vulnerability - quants particularly exposed to tail events")
        
        return flags
    
    def _estimate_strategy_capacity(self, strategy_data: Dict) -> float:
        """估计策略容量"""
        avg_volume = strategy_data.get("avg_daily_volume_usd", 0)
        turnover = strategy_data.get("turnover_annual", 1.0)
        
        # 假设最多占日成交量的X%，年换手Y次
        max_participation_rate = 0.01  # 1%
        
        if avg_volume > 0 and turnover > 0:
            daily_capacity = avg_volume * max_participation_rate
            annual_capacity = daily_capacity * 252 / turnover
            return annual_capacity
        
        return 0
    
    def get_trading_philosophy(self) -> Dict:
        """
        获取 Simons 的交易哲学
        
        Returns:
            包含核心原则的字典
        """
        return {
            "core_principles": [
                "We look for patterns in data, not stories in headlines",
                "Small edges, compounded thousands of times, produce exceptional returns",
                "The market is not perfectly efficient at the micro level",
                "Models must evolve as markets adapt",
                "Risk management is as important as signal generation",
                "Technology and data infrastructure are competitive advantages"
            ],
            "research_approach": [
                "Hire mathematicians, physicists, and computer scientists",
                "Encourage collaboration and idea sharing",
                "Focus on short-term predictions where noise is manageable",
                "Test everything rigorously with out-of-sample data",
                "Keep successful strategies confidential"
            ],
            "risk_principles": [
                "Never risk the firm on a single strategy",
                "Diversify across thousands of independent signals",
                "Use leverage only when statistical confidence is high",
                "Prepare for models to stop working",
                "Monitor for regime changes continuously"
            ]
        }
    
    def get_limitations(self) -> List[str]:
        """
        获取诚实边界/局限性
        
        Returns:
            局限性列表
        """
        return [
            "Renaissance/Medallion's success relies on unique data, infrastructure, and talent that cannot be fully replicated",
            "High-frequency/quantitative strategies have strict capacity constraints",
            "Individual investors lack the technological infrastructure and data advantages of institutional quant funds",
            "Historical backtests do not guarantee future performance; market structure changes can invalidate models",
            "Even Simons experienced periods of strategy underperformance",
            "This framework provides mental models, not a directly deployable trading system",
            "Quantitative strategies require continuous monitoring and adaptation",
            "The edge in quantitative trading has been significantly competed away since Renaissance's early days"
        ]


def create_simons_agent() -> JimSimonsDistilled:
    """
    创建 Jim Simons 蒸馏思维代理
    
    Returns:
        JimSimonsDistilled 实例
    """
    return JimSimonsDistilled()


if __name__ == "__main__":
    # 测试示例
    test_market_data = {
        "data_history_years": 15,
        "data_frequency": "minute",
        "avg_bid_ask_spread_bps": 15,
        "realized_volatility": 0.25,
        "retail_trading_pct": 0.45,
        "has_limit_order_book": True,
        "market_fragmented": True,
        "avg_daily_volume_usd": 500e6,
        "sharpe_ratio": 1.8,
        "p_value": 0.001,
        "max_drawdown": 0.15
    }
    
    agent = JimSimonsDistilled()
    
    print("=" * 60)
    print(f"Agent: {agent.name}")
    print(f"Philosophy: {agent.philosophy}")
    print("=" * 60)
    
    # 市场分析测试
    print("\n>>> Market Analysis:")
    result = agent.analyze(test_market_data)
    print(f"Signal: {result['signal']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reasoning: {result['reasoning']}")
    print(f"Key Insights: {result['key_insights']}")
    
    # 策略评估测试
    print("\n>>> Strategy Evaluation:")
    test_strategy = {
        "has_calculated_alpha": True,
        "alpha_persistence_months": 18,
        "has_risk_rules": True,
        "backtest_completed": True,
        "oos_tested": True,
        "overfitting_analysis": True,
        "tx_costs_included": True,
        "max_drawdown": 0.12,
        "sharpe_ratio": 1.6,
        "avg_holding_period_days": 2.5,
        "avg_daily_volume_usd": 1000e6,
        "turnover_annual": 50
    }
    
    strat_result = agent.evaluate_strategy(test_strategy)
    print(f"Strategy Score: {strat_result['strategy_score']}")
    print(f"Viability: {strat_result['viability']}")
    print(f"Capacity Estimate: ${strat_result['capacity_estimate']:,.0f}")
    print(f"Warnings: {strat_result['warnings']}")
    
    # 因子清单
    print("\n>>> Factor Checklist:")
    factors = agent.generate_factor_checklist()
    for category, details in factors.items():
        print(f"\n{category}:")
        for factor in details.get("factors", [])[:3]:
            print(f"  - {factor}")
