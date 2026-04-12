#!/usr/bin/env python3
"""
Ray Dalio 思维框架蒸馏 V2 - 女娲完整版

核心理念：极度透明 + 极度真实 + 原则系统化

心智模型：
1. 经济如机器（Economic Machine）- 理解信贷、债务、生产力、经济的周期性运作
2. 风险平价（Risk Parity）- 分散的不是资产，而是风险因子
3. 全天候策略（All Weather）- 构建在任何经济环境下都能表现良好的组合
4. 债务周期（Debt Cycle）- 理解长期债务周期和短期债务周期的影响
5. 进化与痛苦（Evolution & Pain）- 痛苦+反思=进步，现实是进化的结果
6. 可信度加权（Believability-Weighted）- 对不同人的意见按可信度加权
7. 五步法（5-Step Process）- 目标→问题→诊断→方案→执行

决策启发式：
1. 看宏观要看债务/GDP比率，而不只是GDP增速
2. 投资前先问：如果我不持有这个头寸，我愿意以当前价格买入吗？
3. 评估央行政策时，关注他们是否能印钱购买资产
4. 构建组合时，先确定风险分配，再确定资产配置
5. 遇到痛苦时，先写下来，然后分析而不是逃避
6. 决策时寻找"与我观点相反但可信度高的聪明人"
7. 用历史类比理解现在，但要识别差异
8. 不要预测，要准备——为多种情景做准备

表达DNA：
- 系统性：用框架、流程、图表表达
- 数据驱动：引用历史数据、统计数据
- 坦诚：承认错误，分享失败经历
- 哲理性：上升到"原则"层面
- 直白：不用华丽辞藻，清晰直接
- 重复强调：重要概念会反复强调

反模式（Dalio 绝对不会做的事）：
- 绝对不会单押一种资产或策略
- 绝对不会忽视债务周期的影响
- 绝对不会在高度泡沫化时追涨
- 绝对不会在情绪驱动下做决策
- 绝对不会认为"这次不一样"
- 绝对不会忽视央行政策对市场的影响
- 绝对不会假装自己总是对的
- 绝对不会回避痛苦和失败

诚实边界：
- 需要杠杆才能达到目标收益（普通人难以复制全天候策略）
- 需要专业衍生品知识来实现风险平价
- 在低利率环境下策略表现会变化
- 不能预测具体市场时机
- 公开表达与实际操作可能有差异（桥水基金具体持仓不公开）
- 信息截止到调研时间点，需要定期更新
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class EconomicEnvironment(Enum):
    """四种经济环境（增长+通胀的矩阵）"""
    GOLDILOCKS = "goldilocks"           # 增长上升 + 通胀下降（最佳）
    EXPANSION_INFLATION = "expansion_inflation"  # 增长上升 + 通胀上升
    DISINFLATION = "disinflation"       # 增长下降 + 通胀下降（对债券有利）
    STAGFLATION = "stagflation"         # 增长下降 + 通胀上升（最差）


class DebtCyclePhase(Enum):
    """债务周期的六个阶段"""
    EARLY = "early"                     # 早期：债务增长，支撑收入增长和资产价格
    BUBBLE = "bubble"                   # 泡沫期：债务增长快于收入增长，资产泡沫形成
    PEAK = "peak"                       # 顶部：紧缩政策，资产价格下跌
    DEPRESSION = "depression"           # 衰退期：去杠杆，经济收缩
    BEAUTIFUL = "beautiful_deleveraging"  # 和谐去杠杆：成功平衡四种去杠杆方式
    PUSHING = "pushing_on_string"       # 推绳子：货币政策失效


@dataclass
class RiskFactor:
    """风险因子"""
    name: str                           # 因子名称
    current_exposure: float             # 当前敞口（-1到1，负数表示反向敞口）
    target_exposure: float              # 目标敞口
    volatility: float                   # 波动率


@dataclass
class Principle:
    """达利欧式原则"""
    title: str
    content: str
    category: str                       # 如：决策、团队、投资、生活
    origin: str                         # 来源（哪本书/演讲）


@dataclass
class MacroAssessment:
    """宏观环境评估"""
    growth_trend: str                   # rising/neutral/falling
    inflation_trend: str                # rising/neutral/falling
    debt_cycle_phase: Optional[DebtCyclePhase]
    central_bank_policy: str            # tightening/neutral/loosening
    risk_premium: float                 # 当前风险溢价水平


class RayDalioDistilledV2:
    """
    蒸馏后的 Ray Dalio 思维框架 V2 - 女娲完整版
    
    Ray Dalio 是桥水基金创始人，以其"原则"方法论、
    全天候策略和对债务周期的深刻理解闻名。
    """
    
    def __init__(self):
        self.name = "Ray Dalio"
        self.philosophy = "Principles + Economic Machine + All Weather"
        self.organization = "Bridgewater Associates"
        self.key_books = ["Principles: Life and Work", "Principles for Dealing with the Changing World Order"]
        
        # 加载核心原则
        self._load_principles()
        
        # 加载心智模型
        self._load_mental_models()
    
    def _load_principles(self):
        """加载达利欧的核心原则"""
        self.principles = [
            Principle(
                title="拥抱现实，应对现实",
                content="不要希望现实不同，要学会理解和应对现实。",
                category="生活",
                origin="Principles"
            ),
            Principle(
                title="痛苦+反思=进步",
                content="痛苦是信号，提示你需要学习一些东西。遇到痛苦时，反思它，你会进步。",
                category="成长",
                origin="Principles"
            ),
            Principle(
                title="可信度加权决策",
                content="对不同人的意见按其可信度加权。不要对所有意见一视同仁。",
                category="决策",
                origin="Principles"
            ),
            Principle(
                title="区分资产和风险",
                content="投资时分散的是风险，不是资产。不同资产可能在同一风险因子上暴露。",
                category="投资",
                origin="All Weather Strategy"
            ),
            Principle(
                title="历史会重演，但不完全一样",
                content="用历史类比理解现在，但要识别关键差异。",
                category="宏观",
                origin="Changing World Order"
            )
        ]
    
    def _load_mental_models(self):
        """加载心智模型描述"""
        self.mental_models = {
            "economic_machine": {
                "name": "经济如机器",
                "description": "经济是由简单部件和重复交易组成的机器，理解这些部件就能理解经济。",
                "key_components": ["信贷", "债务", "生产力", "周期"],
                "application": "用机器思维理解宏观，而不是情绪或叙事"
            },
            "risk_parity": {
                "name": "风险平价",
                "description": "真正的分散是分散风险因子，而不是资产类别。",
                "key_components": ["风险因子暴露", "波动率", "相关性"],
                "application": "先分配风险，再确定资产配置"
            },
            "all_weather": {
                "name": "全天候策略",
                "description": "构建能在任何经济环境下表现良好的组合，不预测环境。",
                "key_components": ["四种经济环境", "风险平衡", "去杠杆能力"],
                "application": "为未知做准备，而不是预测"
            },
            "debt_cycle": {
                "name": "债务周期",
                "description": "理解长期和短期债务周期是理解经济和市场波动的基础。",
                "key_components": ["债务/GDP", "偿债负担", "去杠杆"],
                "application": "宏观分析的核心指标"
            },
            "evolution_pain": {
                "name": "进化与痛苦",
                "description": "进化是宇宙中最强大的力量，痛苦+反思=进步。",
                "key_components": ["现实接受", "痛苦信号", "反思学习"],
                "application": "个人成长和组织文化"
            },
            "believability_weighting": {
                "name": "可信度加权",
                "description": "决策时对不同人的意见按其在该领域的可信度加权。",
                "key_components": ["能力证据", "历史记录", "相关性"],
                "application": "团队决策，避免盲从或傲慢"
            },
            "five_step_process": {
                "name": "五步法",
                "description": "目标→问题→诊断→方案→执行，循环往复。",
                "key_components": ["清晰目标", "识别问题", "根本原因", "设计方案", "执行"],
                "application": "任何复杂目标的实现"
            }
        }
    
    # ============================================================
    # 核心分析 API
    # ============================================================
    
    def analyze_portfolio_risk(self, data: Dict) -> Dict:
        """
        分析投资组合的风险特征（Dalio 视角）
        
        核心：分散的是风险因子，不是资产
        """
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "reasoning": [],
            "risk_assessment": {},
            "environmental_sensitivity": {},
            "recommendations": []
        }
        
        # 评估组合在四种经济环境下的表现
        risk_assessment = self._assess_environmental_risk(data)
        result["risk_assessment"] = risk_assessment
        
        # 环境敏感性分析
        result["environmental_sensitivity"] = self._assess_sensitivity(data)
        
        # 生成信号
        if risk_assessment["is_diversified"] and risk_assessment["has_tail_hedge"]:
            result["signal"] = "bullish"
            result["confidence"] = 75
            result["reasoning"].append("组合在风险因子上充分分散，有尾部对冲")
        elif not risk_assessment["is_diversified"]:
            result["signal"] = "bearish"
            result["confidence"] = 70
            result["reasoning"].append("组合风险集中，缺乏真正的分散化")
        
        # 生成建议
        result["recommendations"] = self._generate_recommendations(data, risk_assessment)
        
        return result
    
    def analyze_macro_environment(self, data: Dict) -> Dict:
        """
        分析当前宏观环境（四种经济环境矩阵）
        
        Dalio 的核心：增长 vs 通胀 的四种组合
        """
        result = {
            "agent": self.name,
            "environment": "unknown",
            "environment_chinese": "未知",
            "best_assets": [],
            "worst_assets": [],
            "reasoning": [],
            "debt_cycle_assessment": {}
        }
        
        # 判断经济环境
        inflation = data.get("inflation_trend", "neutral")
        growth = data.get("growth_trend", "neutral")
        
        # 四种经济环境判断
        if growth == "rising" and inflation == "falling":
            result["environment"] = EconomicEnvironment.GOLDILOCKS.value
            result["environment_chinese"] = "金发女孩环境（最佳）"
            result["best_assets"] = ["股票", "公司债", "新兴市场"]
            result["worst_assets"] = ["长期债券", "黄金", "现金"]
            result["reasoning"].append("增长上升+通胀下降，对风险资产最有利")
            
        elif growth == "rising" and inflation == "rising":
            result["environment"] = EconomicEnvironment.EXPANSION_INFLATION.value
            result["environment_chinese"] = "扩张+通胀"
            result["best_assets"] = ["商品", "股票", "通胀保值债券(TIPS)"]
            result["worst_assets"] = ["长期债券", "现金"]
            result["reasoning"].append("增长和通胀双升，实物资产表现最好")
            
        elif growth == "falling" and inflation == "falling":
            result["environment"] = EconomicEnvironment.DISINFLATION.value
            result["environment_chinese"] = "通缩环境（对债券有利）"
            result["best_assets"] = ["长期债券", "防御性股票", "现金"]
            result["worst_assets"] = ["商品", "周期股"]
            result["reasoning"].append("增长通胀双降，债券表现最佳")
            
        elif growth == "falling" and inflation == "rising":
            result["environment"] = EconomicEnvironment.STAGFLATION.value
            result["environment_chinese"] = "滞胀（最差环境）"
            result["best_assets"] = ["黄金", "商品", "通胀保值债券(TIPS)"]
            result["worst_assets"] = ["股票", "长期债券"]
            result["reasoning"].append("滞胀环境，股债双杀，只有实物资产能保值")
        
        # 债务周期评估
        result["debt_cycle_assessment"] = self._assess_debt_cycle(data)
        
        return result
    
    def assess_debt_cycle(self, data: Dict) -> Dict:
        """
        评估债务周期阶段
        
        Dalio 的招牌分析框架
        """
        return self._assess_debt_cycle(data)
    
    def generate_all_weather_allocation(self, 
                                       risk_tolerance: str = "moderate",
                                       leverage_allowed: bool = False) -> Dict:
        """
        生成全天候策略配置建议
        
        原版全天候（需要杠杆）：
        - 30% 股票
        - 40% 长期债券
        - 15% 中期债券
        - 7.5% 黄金
        - 7.5% 商品
        
        普通人版本（无杠杆）：
        - 适当降低债券杠杆，增加实物资产
        """
        result = {
            "agent": self.name,
            "strategy": "All Weather",
            "risk_tolerance": risk_tolerance,
            "leverage_used": leverage_allowed,
            "allocation": {},
            "rationale": [],
            "warning": []
        }
        
        if leverage_allowed:
            # 原版全天候（桥水实际使用）
            result["allocation"] = {
                "stocks": 0.30,
                "long_term_bonds": 0.40,
                "intermediate_bonds": 0.15,
                "gold": 0.075,
                "commodities": 0.075
            }
            result["rationale"].append("风险平价配置：每种经济环境有等量的风险暴露")
            result["warning"].append("此配置需要杠杆放大低波动资产（债券）的收益贡献")
        else:
            # 普通人版本（降低杠杆依赖）
            if risk_tolerance == "conservative":
                result["allocation"] = {
                    "stocks": 0.20,
                    "bonds": 0.50,
                    "gold": 0.15,
                    "commodities": 0.10,
                    "cash": 0.05
                }
            elif risk_tolerance == "aggressive":
                result["allocation"] = {
                    "stocks": 0.40,
                    "bonds": 0.30,
                    "gold": 0.15,
                    "commodities": 0.15
                }
            else:  # moderate
                result["allocation"] = {
                    "stocks": 0.30,
                    "bonds": 0.40,
                    "gold": 0.15,
                    "commodities": 0.15
                }
            result["rationale"].append("无杠杆版本，降低债券配比，增加实物资产")
            result["warning"].append("无杠杆版本预期收益低于原版，但波动更小")
        
        result["rationale"].append("覆盖四种经济环境：增长/通缩、增长/通胀、衰退/通缩、衰退/通胀")
        
        return result
    
    def apply_five_step_process(self, goal: str, current_status: Dict) -> Dict:
        """
        应用达利欧五步法解决目标问题
        
        五步法：
        1. 明确目标
        2. 识别问题
        3. 诊断根本原因
        4. 设计方案
        5. 执行
        """
        result = {
            "agent": self.name,
            "method": "5-Step Process",
            "steps": {
                "1_goals": {
                    "title": "明确目标",
                    "content": goal,
                    "questions": [
                        "这是你的真实目标吗？",
                        "这个目标与其他目标冲突吗？"
                    ]
                },
                "2_problems": {
                    "title": "识别问题",
                    "content": "识别阻碍目标达成的所有问题，不要容忍它们。",
                    "problems_identified": current_status.get("obstacles", [])
                },
                "3_diagnosis": {
                    "title": "诊断根本原因",
                    "content": "深入分析问题根源，区分症状和病因。",
                    "framework": "像分析机器一样分析这些问题"
                },
                "4_design": {
                    "title": "设计方案",
                    "content": "设计消除问题的路径，思考清楚路线后再行动。"
                },
                "5_execute": {
                    "title": "执行",
                    "content": "执行方案，保持自律。大多数人败在这一步。",
                    "reminder": "执行时保持开放心态，根据反馈调整"
                }
            },
            "key_principle": "经历这五步可能会很痛苦，但痛苦+反思=进步"
        }
        
        return result
    
    def believability_weighted_decision(self, 
                                        options: List[str], 
                                        opinions: List[Dict]) -> Dict:
        """
        可信度加权决策
        
        opinions: [{"person": str, "view": str, "credibility_score": float}]
        """
        result = {
            "agent": self.name,
            "method": "Believability-Weighted Decision Making",
            "options": options,
            "analysis": [],
            "weighted_result": None,
            "reasoning": []
        }
        
        # 计算加权得分
        weighted_scores = {option: 0.0 for option in options}
        total_credibility = 0.0
        
        for opinion in opinions:
            person = opinion["person"]
            view = opinion["view"]
            credibility = opinion.get("credibility_score", 0.5)
            
            result["analysis"].append({
                "person": person,
                "view": view,
                "credibility": credibility
            })
            
            # 如果观点明确支持某个选项，增加该选项得分
            for option in options:
                if option.lower() in view.lower():
                    weighted_scores[option] += credibility
            
            total_credibility += credibility
        
        # 归一化并排序
        if total_credibility > 0:
            for option in weighted_scores:
                weighted_scores[option] /= total_credibility
        
        sorted_options = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)
        result["weighted_result"] = sorted_options
        
        result["reasoning"].append("对不同人的意见按其在该领域的可信度加权")
        result["reasoning"].append("不要对所有意见一视同仁，也不要只听地位最高的人")
        
        return result
    
    # ============================================================
    # 内部辅助方法
    # ============================================================
    
    def _assess_environmental_risk(self, data: Dict) -> Dict:
        """评估组合在四种经济环境下的表现"""
        assessment = {
            "is_diversified": False,
            "has_tail_hedge": False,
            "risk_concentration": "high",
            "environments_covered": [],
            "missing_environments": []
        }
        
        # 检查是否覆盖不同环境
        has_stock = data.get("stock_allocation", 0) > 0.15
        has_bond = data.get("bond_allocation", 0) > 0.15
        has_gold = data.get("gold_allocation", 0) > 0.05
        has_commodity = data.get("commodity_allocation", 0) > 0.05
        
        environments = []
        if has_stock:
            environments.append("growth_rising")
            environments.append("growth_falling_defensive")
        if has_bond:
            environments.append("disinflation")
        if has_gold:
            environments.append("deflation")
            environments.append("stagflation_partial")
        if has_commodity:
            environments.append("inflation")
        
        assessment["environments_covered"] = environments
        
        # 分散化检查
        if len(environments) >= 3:
            assessment["is_diversified"] = True
        
        # 四种环境的覆盖检查
        all_envs = ["growth_rising", "growth_falling", "inflation", "disinflation"]
        for env in all_envs:
            if env not in environments:
                assessment["missing_environments"].append(env)
        
        # 尾部对冲
        if has_gold or (has_bond and data.get("bond_duration", 0) > 7):
            assessment["has_tail_hedge"] = True
        
        # 风险集中度
        largest_position = data.get("largest_position_pct", 1.0)
        if largest_position > 0.30:
            assessment["risk_concentration"] = "very_high"
        elif largest_position > 0.20:
            assessment["risk_concentration"] = "high"
        elif largest_position > 0.10:
            assessment["risk_concentration"] = "medium"
        else:
            assessment["risk_concentration"] = "low"
        
        return assessment
    
    def _assess_sensitivity(self, data: Dict) -> Dict:
        """评估组合对不同环境因子的敏感性"""
        return {
            "inflation_sensitivity": data.get("inflation_beta", 0),
            "growth_sensitivity": data.get("market_beta", 1.0),
            "interest_rate_sensitivity": data.get("duration", 0),
            "currency_sensitivity": data.get("fx_exposure", 0)
        }
    
    def _assess_debt_cycle(self, data: Dict) -> Dict:
        """评估债务周期阶段（Dalio 核心分析）"""
        debt_to_gdp = data.get("debt_to_gdp", 0)
        debt_service_ratio = data.get("debt_service_ratio", 0)
        short_term_rates = data.get("short_term_rates", 0)
        yield_curve = data.get("yield_curve_slope", 0)
        
        assessment = {
            "debt_to_gdp": debt_to_gdp,
            "debt_service_ratio": debt_service_ratio,
            "phase": "unknown",
            "warning_signals": [],
            "opportunities": []
        }
        
        # 债务周期阶段判断
        if debt_to_gdp < 150 and debt_service_ratio < 20:
            assessment["phase"] = DebtCyclePhase.EARLY.value
            assessment["opportunities"].append("债务增长支撑经济，风险资产有利")
        elif debt_to_gdp > 250 and debt_service_ratio > 40:
            assessment["phase"] = DebtCyclePhase.BUBBLE.value
            assessment["warning_signals"].append("债务增长快于收入增长，警惕泡沫")
        elif debt_service_ratio > 50 and short_term_rates > 3:
            assessment["phase"] = DebtCyclePhase.PEAK.value
            assessment["warning_signals"].append("紧缩政策可能导致资产价格下跌")
        elif debt_to_gdp > 300 and data.get("gdp_growth", 2) < 0:
            assessment["phase"] = DebtCyclePhase.DEPRESSION.value
            assessment["warning_signals"].append("可能进入去杠杆阶段")
        
        # 央行政策空间评估
        if short_term_rates < 1:
            assessment["warning_signals"].append("央行降息空间有限，货币政策效力下降")
        
        return assessment
    
    def _generate_recommendations(self, data: Dict, assessment: Dict) -> List[str]:
        """生成 Dalio 风格的建议"""
        recs = []
        
        # 分散化建议
        if not assessment["is_diversified"]:
            recs.append("⚠️ 组合风险集中。建议分散于四种经济环境，而非仅资产类别。")
            if "inflation" not in assessment["environments_covered"]:
                recs.append("   → 缺乏通胀对冲：考虑增加商品或黄金")
            if "disinflation" not in assessment["environments_covered"]:
                recs.append("   → 缺乏通缩对冲：考虑增加长期债券")
        
        # 尾部对冲建议
        if not assessment["has_tail_hedge"]:
            recs.append("⚠️ 缺乏尾部风险对冲。建议增加黄金或长期债券作为保险。")
        
        # 风险集中度建议
        if assessment["risk_concentration"] in ["very_high", "high"]:
            recs.append(f"⚠️ 单一持仓占比过高({data.get('largest_position_pct', 0)*100:.0f}%)。Dalio不会集中押注。")
        
        # 全天候建议
        recs.append("📊 全天候参考配置（需要杠杆）：30%股票 / 40%长债 / 15%中债 / 7.5%黄金 / 7.5%商品")
        recs.append("📊 普通人版本（无杠杆）：30%股票 / 40%债券 / 15%黄金 / 15%商品")
        
        # 原则提醒
        recs.append("💡 Dalio原则：痛苦+反思=进步。定期审视组合表现，从错误中学习。")
        
        return recs
    
    # ============================================================
    # 表达DNA方法
    # ============================================================
    
    def express_like_dalio(self, topic: str, analysis: str) -> str:
        """
        用 Dalio 的表达DNA输出分析
        """
        # Dalio 的表达特征
        characteristics = [
            "用数据和历史类比支撑观点",
            "上升到'原则'层面",
            "坦诚直接，不绕弯子",
            "系统性地分解问题",
            "承认不确定性和错误的可能性"
        ]
        
        # 构建表达
        expression = f"""
关于{topic}，让我分享我的看法：

首先，我理解现实的方式是将其视为一台机器。{analysis}

从历史来看，类似的情况发生过多次。重要的是理解其中的因果关系。

我的原则是：【在此插入相关原则】

当然，我必须诚实地说——我无法确定未来会发生什么。没有人能准确预测。但我知道，如果我们遵循正确的原则，从错误中学习，痛苦+反思=进步，我们就会做得更好。

希望这对你有帮助。
"""
        return expression.strip()
    
    # ============================================================
    # 反模式检查
    # ============================================================
    
    def check_antipatterns(self, action: str) -> Dict:
        """
        检查某个行动是否违反 Dalio 的反模式
        """
        antipatterns = [
            {
                "pattern": "单押一种资产",
                "check": lambda x: "全部" in x or "all in" in x.lower(),
                "warning": "Dalio绝对不会单押一种资产或策略"
            },
            {
                "pattern": "忽视债务周期",
                "check": lambda x: "债务" not in x and "debt" not in x.lower(),
                "warning": "Dalio绝对不会忽视债务周期的影响"
            },
            {
                "pattern": "情绪化决策",
                "check": lambda x: "感觉" in x or "觉得" in x,
                "warning": "Dalio绝对不会在情绪驱动下做决策"
            },
            {
                "pattern": "这次不一样",
                "check": lambda x: "这次不同" in x or " unprecedented" in x.lower(),
                "warning": "Dalio绝对不会认为'这次不一样'"
            }
        ]
        
        violations = []
        for ap in antipatterns:
            if ap["check"](action):
                violations.append({
                    "pattern": ap["pattern"],
                    "warning": ap["warning"]
                })
        
        return {
            "action": action,
            "violations": violations,
            "is_valid": len(violations) == 0
        }
    
    # ============================================================
    # 诚实边界说明
    # ============================================================
    
    def get_limitations(self) -> Dict:
        """
        返回此Skill的诚实边界
        """
        return {
            "limitations": [
                "需要杠杆才能达到目标收益（普通人难以复制全天候策略）",
                "需要专业衍生品知识来实现真正的风险平价",
                "在低利率环境下策略表现会显著变化",
                "不能预测具体市场时机，只能为多种情景做准备",
                "桥水基金的具体持仓和策略细节不公开",
                "达利欧的公开观点可能随时间变化",
                "信息截止到调研时间点，需要定期更新"
            ],
            "not_suitable_for": [
                "寻找快速致富的捷径",
                "预测短期市场走势",
                "替代专业投资顾问",
                "在没有理解风险的情况下使用杠杆"
            ],
            "research_date": "2024-2025",
            "version": "2.0"
        }


# ============================================================
# 导出函数
# ============================================================

def create_dalio_agent() -> RayDalioDistilledV2:
    """创建 Dalio 思维代理"""
    return RayDalioDistilledV2()


# 向后兼容
RayDalioDistilled = RayDalioDistilledV2


if __name__ == "__main__":
    # 简单测试
    agent = create_dalio_agent()
    
    print("=" * 60)
    print(f"Ray Dalio 思维框架蒸馏 V2")
    print(f"Philosophy: {agent.philosophy}")
    print("=" * 60)
    
    # 测试宏观环境分析
    print("\n【测试】宏观环境分析")
    macro_data = {
        "inflation_trend": "rising",
        "growth_trend": "falling",
        "debt_to_gdp": 280,
        "debt_service_ratio": 35
    }
    result = agent.analyze_macro_environment(macro_data)
    print(f"环境判断: {result['environment_chinese']}")
    print(f"最佳资产: {', '.join(result['best_assets'])}")
    print(f"最差资产: {', '.join(result['worst_assets'])}")
    
    # 测试全天候配置
    print("\n【测试】全天候配置建议")
    allocation = agent.generate_all_weather_allocation(
        risk_tolerance="moderate",
        leverage_allowed=False
    )
    print(f"配置: {allocation['allocation']}")
    print(f"理由: {allocation['rationale']}")
    
    # 测试五步法
    print("\n【测试】五步法")
    five_step = agent.apply_five_step_process(
        goal="提升投资决策质量",
        current_status={"obstacles": ["情绪化交易", "缺乏系统"]}
    )
    print(f"方法论: {five_step['method']}")
    for step_name, step_data in five_step['steps'].items():
        print(f"  {step_data['title']}: {step_data['content'][:30]}...")
    
    # 诚实边界
    print("\n【诚实边界】")
    limitations = agent.get_limitations()
    for lim in limitations['limitations'][:3]:
        print(f"  ⚠️ {lim}")
    
    print("\n" + "=" * 60)
    print("测试完成")
