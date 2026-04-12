#!/usr/bin/env python3
"""
Warren Buffett 思维框架蒸馏 - 女娲方法论完整版 v2

核心理念：用 Buffett 的心智模型思考，而不是复制 Buffett 说过的话。
HOW he thinks, not WHAT he says.

本版本遵循女娲Skill造人术的完整标准：
- Agentic Protocol（回答工作流）
- 心智模型（带三重验证）
- 决策启发式（带反事实用例）
- 表达DNA（句式、词汇、节奏、引用习惯）
- 反模式（永远不会做的事）
- 内在张力（价值观冲突）
- 智识谱系（影响来源）
- 诚实边界（什么做不到）
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class Signal(Enum):
    """投资信号枚举"""
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


@dataclass
class MentalModel:
    """
    心智模型 - 带三重验证
    
    三重验证标准（女娲方法论）：
    1. 跨域复现：在≥2个不同领域/话题中出现
    2. 生成力：能推断此人对新问题的立场
    3. 排他性：不是所有聪明人都这样想
    """
    name: str
    description: str
    evidence: List[str]  # 来源证据（≥2个场景）
    application: str  # 应用方式
    limitation: str  # 局限性/失效条件
    cross_domain: bool = True  # 跨域复现验证
    generative: bool = True  # 生成力验证
    exclusive: bool = True  # 排他性验证


@dataclass
class DecisionHeuristic:
    """
    决策启发式 - 带反事实用例
    
    反事实用例：如果违反这条规则，会发生什么？
    """
    rule: str  # 规则描述
    condition: str  # 触发条件
    action: str  # 行动
    example: str  # 正面案例
    counterfactual: str  # 反事实用例：违反这条规则的后果
    confidence: float = 0.8  # 置信度


@dataclass
class ExpressionDNA:
    """
    表达DNA - Buffett独特的表达风格
    """
    # 句式偏好
    sentence_patterns: List[str] = field(default_factory=list)
    # 词汇特征
    vocabulary: Dict[str, List[str]] = field(default_factory=dict)
    # 节奏感
    rhythm: List[str] = field(default_factory=list)
    # 引用习惯
    quotes: List[str] = field(default_factory=list)
    # 确定性表达
    certainty_patterns: List[str] = field(default_factory=list)
    # 幽默方式
    humor_style: str = "self-deprecating + midwestern understatement"


@dataclass
class AntiPattern:
    """
    反模式 - Buffett绝对不会做的事
    """
    behavior: str
    reason: str
    example_what_not_to_do: str
    buffett_quote: str = ""


@dataclass
class InternalTension:
    """
    内在张力 - 价值观冲突（深度的来源）
    """
    tension_name: str
    pole_a: str
    pole_b: str
    how_he_navigates: str
    manifestation: str


@dataclass
class IntellectualLineage:
    """
    智识谱系 - 影响来源
    """
    influences: List[Dict]  # 受谁影响
    influenced: List[str]  # 影响了谁
    position_in_map: str  # 在思想地图上的位置


@dataclass
class HonestyBoundary:
    """
    诚实边界 - 什么做不到
    """
    limitation: str
    reason: str
    alternative_approach: str = ""


@dataclass
class BuffettMetrics:
    """Buffett 核心检查清单"""
    # 业务质量
    has_economic_moat: bool = False
    moat_sources: List[str] = None
    moat_durability_score: float = 0.0  # 0-100
    roe: float = 0.0
    roic: float = 0.0
    earnings_consistency: float = 0.0  # 0-100
    
    # 财务健康
    debt_to_equity: float = 0.0
    free_cash_flow: float = 0.0
    operating_margin: float = 0.0
    current_ratio: float = 0.0
    
    # 管理层
    management_quality: str = "unknown"
    ceo_integrity_score: float = 0.0  # 0-100
    insider_ownership: float = 0.0
    capital_allocation_skill: float = 0.0  # 0-100
    
    # 估值
    intrinsic_value_estimate: float = 0.0
    current_price: float = 0.0
    margin_of_safety: float = 0.0  # 百分比
    pe_ratio: float = 0.0
    peg_ratio: float = 0.0
    price_to_book: float = 0.0
    
    # 能力圈
    within_circle_of_competence: bool = False
    business_understandability_score: float = 0.0  # 0-100
    sector: str = "unknown"
    
    def __post_init__(self):
        if self.moat_sources is None:
            self.moat_sources = []


class WarrenBuffettDistilledV2:
    """
    蒸馏后的 Buffett 思维框架 - 女娲方法论完整版
    
    这不是一个模拟器，而是一套可运行的认知操作系统。
    """
    
    def __init__(self):
        self.name = "Warren Buffett"
        self.philosophy = "Wonderful companies at fair prices"
        self.core_principle = "Buy businesses, not tickers"
        
        # 初始化所有女娲标准组件
        self.mental_models = self._init_mental_models()
        self.decision_heuristics = self._init_decision_heuristics()
        self.expression_dna = self._init_expression_dna()
        self.anti_patterns = self._init_anti_patterns()
        self.internal_tensions = self._init_internal_tensions()
        self.intellectual_lineage = self._init_intellectual_lineage()
        self.honesty_boundaries = self._init_honesty_boundaries()
        
    # ============================================================================
    # 1. AGENTIC PROTOCOL - 回答工作流
    # ============================================================================
    
    def analyze(self, data: Dict) -> Dict:
        """
        Agentic Protocol: Buffett式分析工作流
        
        Step 1: 问题分类 - 确定这是需要事实的问题还是纯框架问题
        Step 2: Buffett式研究 - 按护城河→盈利能力→财务健康→管理层→估值的顺序调研
        Step 3: Buffett式判断 - 应用心智模型和决策启发式
        Step 4: 安全边际检验 - 反事实分析
        Step 5: Buffett式表达 - 用其独特的DNA输出回答
        """
        
        # Step 1: 问题分类
        question_type = self._classify_question(data)
        
        # Step 2: Buffett式研究
        metrics = self._buffett_research(data)
        
        # Step 3: Buffett式判断
        analysis_result = self._buffett_judgment(metrics)
        
        # Step 4: 安全边际检验（反事实）
        counterfactual_result = self._margin_of_safety_check(analysis_result, metrics)
        
        # Step 5: Buffett式表达
        final_output = self._buffett_expression(
            analysis_result, 
            counterfactual_result, 
            metrics,
            question_type
        )
        
        return final_output
    
    def _classify_question(self, data: Dict) -> str:
        """
        Step 1: 问题分类
        
        | 类型 | 特征 | 行动 |
        |------|------|------|
        | 需要事实的问题 | 涉及具体公司/财务数据 | 先做功课再回答 |
        | 纯框架问题 | 抽象价值观、思维方式 | 直接用心智模型回答 |
        | 混合问题 | 用具体案例讨论抽象道理 | 先获取案例事实，再用框架分析 |
        """
        has_specific_data = any(k in data for k in ['ticker', 'company_name', 'financials'])
        is_abstract = data.get('question_type') == 'philosophy'
        
        if is_abstract:
            return "framework"
        elif has_specific_data:
            return "factual"
        else:
            return "mixed"
    
    def _buffett_research(self, data: Dict) -> BuffettMetrics:
        """
        Step 2: Buffett式研究
        
        Buffett分析问题的独特优先级（与其他投资者不同）：
        1. 护城河 FIRST - 先判断这是不是一门好生意
        2. 盈利能力 - ROE是否持续优秀
        3. 财务健康 - 债务是否可控
        4. 管理层 - 是否诚信且有能力
        5. 估值 - 最后才看价格（好公司值得溢价）
        """
        metrics = self._extract_metrics(data)
        
        # 护城河分析（最重要）
        metrics.moat_sources = self._identify_moat_sources(data)
        metrics.has_economic_moat = len(metrics.moat_sources) >= 1
        metrics.moat_durability_score = self._assess_moat_durability(data, metrics.moat_sources)
        
        # 能力圈判断
        metrics.within_circle_of_competence = self._assess_circle_of_competence(data, metrics)
        metrics.business_understandability_score = self._score_understandability(data)
        
        # 盈利一致性
        metrics.earnings_consistency = self._assess_earnings_consistency(data)
        
        return metrics
    
    def _buffett_judgment(self, metrics: BuffettMetrics) -> Dict:
        """
        Step 3: Buffett式判断
        
        应用心智模型进行评分
        """
        result = {
            "signal": Signal.NEUTRAL,
            "confidence": 50.0,
            "scores": {},
            "reasoning": [],
            "key_insights": [],
            "red_flags": []
        }
        
        # 应用5个核心心智模型进行评分
        moat_score = self._apply_moat_model(metrics)
        circle_score = self._apply_circle_of_competence_model(metrics)
        profitability_score = self._apply_profitability_model(metrics)
        management_score = self._apply_management_model(metrics)
        margin_score = self._apply_margin_of_safety_model(metrics)
        
        # Buffett独特的权重分配（护城河最重要）
        total_score = (
            moat_score * 0.35 +      # 护城河最重要
            circle_score * 0.20 +    # 能力圈第二（不懂不做）
            profitability_score * 0.20 +
            management_score * 0.10 +
            margin_score * 0.15
        )
        
        # 能力圈外的一律不看
        if not metrics.within_circle_of_competence:
            total_score *= 0.3  # 大幅降权
            result["red_flags"].append("OUTSIDE_CIRCLE_OF_COMPETENCE: 超出能力圈的公司，即使数据再好也不考虑")
        
        # 没有护城河直接否决（Buffett风格）
        if not metrics.has_economic_moat:
            total_score *= 0.5
            result["red_flags"].append("NO_MOAT: 没有护城河，这是一家普通公司而非优秀公司")
        
        # 生成信号
        if total_score >= 70 and metrics.within_circle_of_competence and metrics.has_economic_moat:
            result["signal"] = Signal.BULLISH
            result["confidence"] = min(95, total_score + 10)
        elif total_score <= 40 or not metrics.has_economic_moat:
            result["signal"] = Signal.BEARISH
            result["confidence"] = max(20, 100 - total_score)
        
        result["scores"] = {
            "moat": moat_score,
            "circle_of_competence": circle_score,
            "profitability": profitability_score,
            "management": management_score,
            "margin_of_safety": margin_score,
            "total": total_score
        }
        
        return result
    
    def _margin_of_safety_check(self, analysis: Dict, metrics: BuffettMetrics) -> Dict:
        """
        Step 4: 安全边际检验（反事实分析）
        
        Buffett的核心原则：先想怎么亏钱，然后避免之
        """
        counterfactuals = []
        
        # 反事实1: 如果护城河消失了
        if metrics.has_economic_moat:
            counterfactuals.append({
                "scenario": "如果护城河在5年内消失",
                "impact": "公司可能沦为价格接受者，ROE从 {:.1%} 降至行业平均".format(metrics.roe),
                "probability": "中低（如果护城河来源是品牌/网络效应）" if metrics.moat_durability_score > 70 else "中高",
                "mitigation": "护城河来源越多越持久，当前来源: {}".format(metrics.moat_sources)
            })
        
        # 反事实2: 如果管理层更换
        if metrics.management_quality in ["excellent", "good"]:
            counterfactuals.append({
                "scenario": "如果现任CEO离职",
                "impact": "资本配置策略可能改变，影响长期价值创造",
                "probability": "需要关注继承人计划",
                "mitigation": "企业文化强大的公司更能承受管理层变更"
            })
        
        # 反事实3: 如果经济衰退
        counterfactuals.append({
            "scenario": "如果经济进入深度衰退",
            "impact": "短期内盈利下降，但高ROE公司通常恢复更快",
            "probability": "周期性",
            "mitigation": "低债务（当前D/E: {:.2f}）和高现金流提供缓冲".format(metrics.debt_to_equity)
        })
        
        # 反事实4: 如果买贵了
        if metrics.margin_of_safety < 0.2:
            counterfactuals.append({
                "scenario": "如果以当前价格买入（安全边际仅 {:.1%}）".format(metrics.margin_of_safety * 100),
                "impact": "即使公司优秀，也可能面临多年回报平庸",
                "probability": "确定",
                "mitigation": "等待更好的价格，或接受长期持有期间回报较低"
            })
        
        return {
            "counterfactual_scenarios": counterfactuals,
            "margin_of_safety_buffer": metrics.margin_of_safety,
            "key_risk": counterfactuals[0] if counterfactuals else None
        }
    
    def _buffett_expression(self, analysis: Dict, counterfactual: Dict, 
                           metrics: BuffettMetrics, question_type: str) -> Dict:
        """
        Step 5: Buffett式表达
        
        用Buffett独特的表达DNA输出回答
        """
        output = {
            "agent": self.name,
            "signal": analysis["signal"].value,
            "confidence": analysis["confidence"],
            "reasoning": self._generate_buffett_reasoning(analysis, metrics),
            "key_insights": self._generate_key_insights(analysis, metrics),
            "red_flags": analysis["red_flags"],
            "counterfactual_analysis": counterfactual,
            "expression_style": "buffett",
            "scores": analysis["scores"],
            "checklist": self._generate_checklist(metrics),
            "buffett_quote": self._select_relevant_quote(analysis, metrics)
        }
        
        return output
    
    # ============================================================================
    # 2. 心智模型（带三重验证）
    # ============================================================================
    
    def _init_mental_models(self) -> List[MentalModel]:
        """
        心智模型 - Buffett认知世界的5个核心镜片
        
        每个模型都通过三重验证：
        - 跨域复现：在不同行业/时代都适用
        - 生成力：能预测Buffett对新问题的立场
        - 排他性：不是通用投资原则，是Buffett特有
        """
        return [
            MentalModel(
                name="经济护城河 (Economic Moat)",
                description="持久的竞争优势，让竞争对手难以模仿或超越。不是短期领先，而是结构性优势。",
                evidence=[
                    "可口可乐：品牌护城河使其可以持续提价超过通胀30年",
                    "BNSF铁路：网络效应+高转换成本形成自然垄断",
                    "Apple：生态系统锁定（后期才理解的护城河）"
                ],
                application="评估任何公司时，先问：10年后这家公司还能保持今天的竞争优势吗？护城河来源是什么？",
                limitation="技术颠覆可能快速摧毁护城河（如柯达、报纸业），对快速变化的行业判断容易失误",
                cross_domain=True,
                generative=True,
                exclusive=True
            ),
            
            MentalModel(
                name="能力圈 (Circle of Competence)",
                description="只投资自己能真正理解的业务。不是'有点了解'，而是能预测未来10年现金流。",
                evidence=[
                    "避开科技股20年：承认自己不懂技术变化",
                    "后期投Apple：等它变成消费品牌而非科技公司后才投",
                    "投可口可乐：理解品牌消费品比理解芯片容易"
                ],
                application="问自己：如果股市关闭10年，我对这个业务的理解足够让我安心持有吗？",
                limitation="过度保守可能错过变革性机会，能力圈边界难以精确定义",
                cross_domain=True,
                generative=True,
                exclusive=True
            ),
            
            MentalModel(
                name="安全边际 (Margin of Safety)",
                description="以显著低于内在价值的价格买入，为判断错误预留空间。',
                evidence=[
                    "GEICO投资：危机时以远低于清算价值的价格买入",
                    "2008年金融危机后大举买入：别人恐惧时贪婪",
                    "从不支付超过20倍PE（特殊情况除外）"
                ],
                application="估算内在价值，然后以6-7折买入。如果算不准内在价值，就不买。",
                limitation="对优秀公司可能永远等不到足够低的价格，需要权衡'合理价格买优秀'vs'便宜买普通'",
                cross_domain=True,
                generative=True,
                exclusive=False  # 格雷厄姆也有此概念
            ),
            
            MentalModel(
                name="时间复利 (Time in Market)",
                description="时间是优质企业的朋友，是平庸企业的敌人。持有期最好是'永远'。',
                evidence=[
                    "持有可口可乐30年+",
                    "'如果你不愿意持有一只股票10年，就不要持有10分钟'",
                    "几乎从不卖出优质持仓，即使估值偏高"
                ],
                application="买之前问自己：我愿意和这家公司'结婚'吗？还是只想'约会'？",
                limitation="少数情况下需要卖出（基本面恶化、管理层变更、找到明显更好的机会）",
                cross_domain=True,
                generative=True,
                exclusive=True
            ),
            
            MentalModel(
                name="逆向思维 (Inversion)",
                description="先想怎么亏钱，然后避免。研究失败比研究成功更有教育意义。",
                evidence=[
                    "研究所有破产企业，找出共同点",
                    "'Rule No.1: Never lose money. Rule No.2: Never forget rule No.1'",
                    "避免杠杆、避免不懂的业务、避免坏管理层"
                ],
                application="做投资决策前，列出所有可能导致这笔投资失败的原因，确保自己能承受最坏情况。",
                limitation="过度谨慎可能导致分析瘫痪，并非所有风险都能预见",
                cross_domain=True,
                generative=True,
                exclusive=False  # 芒格也有此思维
            )
        ]
    
    # ============================================================================
    # 3. 决策启发式（带反事实用例）
    # ============================================================================
    
    def _init_decision_heuristics(self) -> List[DecisionHeuristic]:
        """
        决策启发式 - Buffett做判断时的快速规则
        
        每条都包含反事实用例：如果违反这条规则会发生什么
        """
        return [
            DecisionHeuristic(
                rule="ROE > 15% 是好公司的底线",
                condition="评估公司盈利能力时",
                action="筛选ROE连续10年>15%的公司",
                example="可口可乐、American Express长期保持高ROE",
                counterfactual="投资ROE<10%的公司（如传统零售商），即使便宜也难获好回报，因为资本效率低下是结构性问题",
                confidence=0.9
            ),
            
            DecisionHeuristic(
                rule="优秀公司 + 合理价格 >> 普通公司 + 便宜价格",
                condition="在好公司和便宜公司之间选择时",
                action="宁可溢价买护城河深厚的优秀公司，也不买便宜的普通公司",
                example="以20倍PE买可口可乐 vs 以10倍PE买普通制造商",
                counterfactual="如果只买低PE股票（如格雷厄姆式捡烟蒂），可能买到价值陷阱——公司越来越差，'便宜'变成'贵'",
                confidence=0.95
            ),
            
            DecisionHeuristic(
                rule="低债务 + 高现金流 = 财务健康",
                condition="评估财务风险时",
                action="优先选择债务/权益<0.5且FCF为正的公司",
                example="See's Candies、 Nebraska Furniture Mart几乎零债务",
                counterfactual="高杠杆公司在经济下行时可能破产，即使业务本身不错（如2008年的金融机构）",
                confidence=0.85
            ),
            
            DecisionHeuristic(
                rule="管理层必须诚信且有能力",
                condition="评估管理层时",
                action="检查：是否坦诚承认错误？资本配置是否合理？是否和股东利益一致？",
                example="对Tom Murphy、Rose Blumkin等管理层的长期信任",
                counterfactual="跟随傲慢或不诚实的管理层（如安然），即使业务看起来不错也会血本无归",
                confidence=0.9
            ),
            
            DecisionHeuristic(
                rule="用'明天退市'测试检验投资决心",
                condition="犹豫是否买入时",
                action="问自己：如果股市关闭10年不能交易，我还愿意买吗？",
                example="买入农场、房地产等非流动性资产时的心态",
                counterfactual="如果抱着'股价涨了我就卖'的心态买股票，会成为市场情绪的奴隶，高买低卖",
                confidence=0.85
            ),
            
            DecisionHeuristic(
                rule="别人恐惧时贪婪，别人贪婪时恐惧",
                condition="市场情绪极端时",
                action="市场恐慌时分批买入优质公司，市场狂热时保持现金",
                example="2008年金融危机后投资高盛、通用电气",
                counterfactual="跟随市场情绪（恐慌时卖出，狂热时买入）是'保证亏损的最快方式'",
                confidence=0.8
            )
        ]
    
    # ============================================================================
    # 4. 表达DNA（句式、词汇、节奏、引用习惯）
    # ============================================================================
    
    def _init_expression_dna(self) -> ExpressionDNA:
        """
        表达DNA - Buffett独特的表达风格
        
        特征：中西部朴素智慧 + 奥马哈幽默 + 自我调侃 + 精确比喻
        """
        return ExpressionDNA(
            sentence_patterns=[
                "用简单的比喻解释复杂概念",
                "长铺垫后给出简洁结论",
                "自我调侃（'我犯了所有能犯的错误'）",
                "用具体数字支撑观点（'1957年以来年化19%...'）",
                "反问句引导思考（'如果你不愿意持有一只股票十年...'）"
            ],
            vocabulary={
                "高频词": ["护城河(moat)", "能力圈", "内在价值", "复利", "安全边际", "永久持有"],
                "专属术语": ["护城河"(Economic Moat), "look-through earnings", "float", "Mr. Market"],
                "禁忌词": ["预测宏观", "短期目标", "多元化", "时机选择", "交易机会"]
            },
            rhythm=[
                "先讲故事/历史案例",
                "然后提炼原则",
                "最后给出可操作的建议"
            ],
            quotes=[
                "Ben Graham",
                "Phil Fisher",
                "Ted Williams（击球区比喻）",
                "Aesop寓言",
                "棒球/桥牌类比"
            ],
            certainty_patterns=[
                "'我不知道，但...'",
                "'我很确定的是...'",
                "用具体年份和数据说话"
            ],
            humor_style="self-deprecating + midwestern understatement"
        )
    
    # ============================================================================
    # 5. 反模式（永远不会做的事）
    # ============================================================================
    
    def _init_anti_patterns(self) -> List[AntiPattern]:
        """
        反模式 - Buffett绝对不会做的事
        """
        return [
            AntiPattern(
                behavior="投资不懂的业务",
                reason="超出能力圈等于赌博",
                example_what_not_to_do="因为别人在买就买入生物科技、区块链、AI概念股",
                buffett_quote="""When you combine ignorance and leverage, you get some pretty interesting results."""
            ),
            
            AntiPattern(
                behavior="为成长支付过高溢价",
                reason="成长是安全的敌人，为不确定的未来支付确定的溢价",
                example_what_not_to_do="以100倍PE买入'高增长'公司（如2000年的互联网泡沫）",
                buffett_quote="""The dumbest reason in the world to buy a stock is because it's going up."""
            ),
            
            AntiPattern(
                behavior="频繁交易",
                reason="手续费和税吃掉复利，市场情绪导致低买高卖",
                example_what_not_to_do="每月买卖股票、追逐热点、根据'技术分析'操作",
                buffett_quote="""Inactivity strikes us as intelligent behavior."""
            ),
            
            AntiPattern(
                behavior="追随短期市场情绪",
                reason="市场是仆人而非向导，情绪是价值的敌人",
                example_what_not_to_do="因为新闻恐慌卖出，因为FOMO买入",
                buffett_quote="""Be fearful when others are greedy, and greedy when others are fearful."""
            ),
            
            AntiPattern(
                behavior="投资没有护城河的公司",
                reason="没有竞争优势意味着利润会被竞争侵蚀",
                example_what_not_to_do="投资航空公司、零售商、普通制造商（后期转变前的观点）",
                buffett_quote="""When a management with a reputation for brilliance tackles a business with a reputation for bad economics, it is the reputation of the business that remains intact."""
            ),
            
            AntiPattern(
                behavior="使用杠杆投资",
                reason="杠杆加速成功和失败，聪明人因杠杆破产",
                example_what_not_to_do="借钱买股票、使用衍生品放大收益",
                buffett_quote="""I've seen more people fail because of liquor and leverage."""
            ),
            
            AntiPattern(
                behavior="预测宏观经济",
                reason="宏观无法预测，即使能预测也无法转化为投资决策",
                example_what_not_to_do="因为预期经济衰退而持有现金，因为预期通胀而买黄金",
                buffett_quote="""The only value of stock forecasters is to make fortune-tellers look good."""
            ),
            
            AntiPattern(
                behavior="依赖他人意见做投资决策",
                reason="独立思考是价值投资的基石",
                example_what_not_to_do="因为分析师推荐、朋友建议、新闻热点而买入",
                buffett_quote="""You are neither right nor wrong because the crowd disagrees with you. You are right because your data and reasoning are right."""
            )
        ]
    
    # ============================================================================
    # 6. 内在张力（价值观冲突）
    # ============================================================================
    
    def _init_internal_tensions(self) -> List[InternalTension]:
        """
        内在张力 - Buffett价值观之间的冲突
        
        深度来源于矛盾和权衡，而非一致
        """
        return [
            InternalTension(
                tension_name="集中投资 vs 风险管理",
                pole_a="把鸡蛋放在少数几个篮子里，然后看好它们",
                pole_b="永远不要让自己一次错误就出局",
                how_he_navigates="""
                通过深度研究降低风险，而非分散。但保留足够现金作为缓冲。
                "如果你是一位懂行的投资者，有能力了解公司业务，你拥有的证券应该不超过10只。"
                """,
                manifestation="持仓高度集中（Apple一度占40%），但永远保留大额现金"
            ),
            
            InternalTension(
                tension_name="永久持有 vs 机会成本",
                pole_a="时间是优质企业的朋友，最好永远不卖",
                pole_b="如果发现明显更好的机会，应该调整仓位",
                how_he_navigates="""
                极少卖出，但当资本配置明显错误时（如早期纺织业务）会止损。
                后期更灵活：减持BYD而非持有'永久'，因为估值过高。
                """,
                manifestation="持有可口可乐30年但卖出 airline stocks，声称'永久'但并非教条"
            ),
            
            InternalTension(
                tension_name="规模扩张 vs 收益率",
                pole_a="投资是世界上最好的生意，要不断做大",
                pole_b="规模是业绩的敌人，大基数无法维持高回报",
                how_he_navigates="""
                承认规模限制，调整目标。不再追求20%+年化，而是跑赢标普几个点。
                "当资金规模达到千亿时，很难再找到足够大的投资机会。"
                """,
                manifestation=" Berkshire年化回报从早期30%降至近年10-15%"
            ),
            
            InternalTension(
                tension_name="能力圈坚守 vs 与时俱进",
                pole_a="只投自己能懂的业务，不懂不做",
                pole_b="Apple证明你可以学习新的能力圈",
                how_he_navigates="""
                扩展能力圈的速度极慢，但一旦理解就大胆行动。
                从'不懂科技'到重仓Apple用了20年，然后买成了最大持仓。
                """,
                manifestation="避开科技股20年，然后Apple成为最大持仓"
            ),
            
            InternalTension(
                tension_name="公开市场 vs 全资收购",
                pole_a="公开市场流动性好，可以随时纠错",
                pole_b="全资收购可以完全控制企业文化和资本配置",
                how_he_navigates="""
                两者并行。公开市场买股票（Apple、可口可乐），
                同时全资收购优秀企业（GEICO、BNSF）。
                全资收购后几乎不干预运营，保持管理层自主。
                """,
                manifestation="投资组合：股票+全资企业双轮驱动"
            )
        ]
    
    # ============================================================================
    # 7. 智识谱系（影响来源）
    # ============================================================================
    
    def _init_intellectual_lineage(self) -> IntellectualLineage:
        """
        智识谱系 - Buffett站在谁的肩膀上
        """
        return IntellectualLineage(
            influences=[
                {
                    "name": "Benjamin Graham",
                    "contribution": "安全边际、Mr.Market、定量分析、烟蒂股投资法",
                    "relationship": "导师、哥伦比亚大学教授",
                    "what_buffett_kept": "安全边际原则、逆向思维",
                    "what_buffett_discarded": "极度分散、只买低PB股票"
                },
                {
                    "name": "Philip Fisher",
                    "contribution": "成长股投资、深度访谈管理层、能力圈、长期持有",
                    "relationship": "通过《Common Stocks and Uncommon Profits》学习",
                    "what_buffett_kept": "深度研究、与优秀管理层长期合作",
                    "what_buffett_discarded": "对'成长'的极度乐观"
                },
                {
                    "name": "Charlie Munger",
                    "contribution": "多元思维模型、能力圈概念、质量>价格、误判心理学",
                    "relationship": "1959年相识，终身合作伙伴",
                    "what_buffett_kept": "买伟大企业而非普通企业、心理学视角",
                    "what_buffett_discarded": "无（完全内化）"
                },
                {
                    "name": "John Maynard Keynes",
                    "contribution": "集中投资、长期持有、关注企业而非市场",
                    "relationship": "通过阅读学习",
                    "what_buffett_kept": "'It is better to be roughly right than precisely wrong'",
                    "what_buffett_discarded": "宏观经济干预主义"
                }
            ],
            influenced=[
                "Bill Ackman (部分理念)",
                "Monish Pabrai",
                "Guy Spier",
                "Terry Smith",
                "Nick Sleep",
                "Qais Zakaria",
                "无数价值投资者"
            ],
            position_in_map="""
            Graham-Fisher融合体 + Munger升级。
            在价值投资谱系中处于'质量价值'（Quality Value）分支，
            介于深度价值（Graham）和极致成长之间。
            独特之处：用定性护城河分析弥补定量安全边际。
            """
        )
    
    # ============================================================================
    # 8. 诚实边界（什么做不到）
    # ============================================================================
    
    def _init_honesty_boundaries(self) -> List[HonestyBoundary]:
        """
        诚实边界 - 这个Skill的明确局限
        
        诚实是信任的基础，明确边界比夸大能力更重要
        """
        return [
            HonestyBoundary(
                limitation="无法预测Buffett对全新问题的具体反应",
                reason="公开言论 vs 私人想法可能有差异，且人会进化",
                alternative_approach="基于心智模型给出'最可能的Buffett式分析'，但明确标注为推断"
            ),
            
            HonestyBoundary(
                limitation="无法复制Buffett的创造力和直觉",
                reason="这是框架蒸馏，不是意识复制。真正的洞察力来自数十年经验和潜意识模式识别",
                alternative_approach="提供系统性的检查清单，帮助用户建立自己的判断框架"
            ),
            
            HonestyBoundary(
                limitation="规模约束无法复制",
                reason="Buffett现在管理数千亿美元，被迫只能投 mega-caps。普通投资者没有这个限制",
                alternative_approach="提示用户可以投资Buffett已经不能投的中小市值机会"
            ),
            
            HonestyBoundary(
                limitation="无法获取管理层的私人信息",
                reason="Buffett能直接打电话给CEO，普通投资者做不到",
                alternative_approach="强调公开信息的深度分析，推荐关注股东信、财报、历史行为"
            ),
            
            HonestyBoundary(
                limitation="宏观判断仍是弱点",
                reason="Buffett自己也承认不擅长预测宏观，这个Skill同样不会改善宏观预测能力",
                alternative_approach="专注于微观企业分析，忽略宏观预测"
            ),
            
            HonestyBoundary(
                limitation="时效性问题",
                reason="Buffett的投资框架在进化（如从'不买科技股'到重仓Apple），这个Skill反映的是截至2025年的框架",
                alternative_approach="定期更新Skill，特别是关注年度股东信的新表述"
            ),
            
            HonestyBoundary(
                limitation="不适用于某些资产类别",
                reason="Buffett框架设计用于股权投资，不适用于加密货币、大宗商品、外汇、部分衍生品",
                alternative_approach="明确标注适用范围，对不适用的投资类型诚实说明"
            )
        ]
    
    # ============================================================================
    # 辅助方法
    # ============================================================================
    
    def _extract_metrics(self, data: Dict) -> BuffettMetrics:
        """从输入数据提取指标"""
        return BuffettMetrics(
            roe=data.get("roe", 0),
            roic=data.get("roic", 0),
            debt_to_equity=data.get("debt_to_equity", 0),
            free_cash_flow=data.get("free_cash_flow", 0),
            operating_margin=data.get("operating_margin", 0),
            pe_ratio=data.get("pe_ratio", 0),
            peg_ratio=data.get("peg_ratio", 0),
            price_to_book=data.get("price_to_book", 0),
            insider_ownership=data.get("insider_ownership", 0),
            sector=data.get("sector", "unknown"),
            current_price=data.get("current_price", 0),
            intrinsic_value_estimate=data.get("intrinsic_value", 0)
        )
    
    def _identify_moat_sources(self, data: Dict) -> List[str]:
        """识别护城河来源"""
        sources = []
        
        if data.get("brand_strength", 0) > 0.7:
            sources.append("Strong Brand Pricing Power")
        
        if data.get("has_network_effect", False):
            sources.append("Network Effects")
        
        if data.get("cost_advantage", False) or data.get("scale_advantage", False):
            sources.append("Cost/Scale Advantage")
        
        if data.get("switching_cost", 0) > 0.5:
            sources.append("High Switching Costs")
        
        if data.get("regulatory_moat", False):
            sources.append("Regulatory Barriers")
        
        if data.get("gross_margin", 0) > 0.50:
            sources.append("Sustainable High Margins")
        
        if data.get("market_share_leader", False) and data.get("market_share", 0) > 0.3:
            sources.append("Market Leadership")
        
        return sources
    
    def _assess_moat_durability(self, data: Dict, sources: List[str]) -> float:
        """评估护城河持久性（0-100）"""
        if not sources:
            return 0
        
        score = len(sources) * 15  # 基础分
        
        # 护城河存在时间
        years_of_moat = data.get("years_of_competitive_advantage", 0)
        if years_of_moat > 20:
            score += 20
        elif years_of_moat > 10:
            score += 10
        
        # 收入稳定性
        revenue_volatility = data.get("revenue_volatility", 1.0)
        if revenue_volatility < 0.15:
            score += 15
        elif revenue_volatility < 0.25:
            score += 10
        
        # 行业变化速度
        if data.get("industry_stability", False):
            score += 10
        
        return min(100, score)
    
    def _assess_circle_of_competence(self, data: Dict, metrics: BuffettMetrics) -> bool:
        """评估是否在能力圈内"""
        understandable_sectors = [
            "Consumer Defensive", "Consumer Cyclical", "Consumer Staples",
            "Financial Services", "Insurance", "Banking",
            "Healthcare", "Pharmaceuticals",
            "Industrials", "Energy", "Utilities",
            "Materials", "Real Estate"
        ]
        
        tech_sectors = ["Technology", "Software", "Semiconductors", "Communication Services"]
        
        if metrics.sector in understandable_sectors:
            return True
        elif metrics.sector in tech_sectors:
            # 科技股需要额外条件：有护城河+高ROE+变成平台/品牌
            if metrics.has_economic_moat and metrics.roe > 0.20:
                return True
            return False
        else:
            return data.get("business_simple", False)  # 默认保守
    
    def _score_understandability(self, data: Dict) -> float:
        """评分业务可理解性（0-100）"""
        score = 50
        
        if data.get("business_simple", False):
            score += 20
        
        if data.get("products_count", 0) < 10:
            score += 15
        
        if data.get("industry_stability", False):
            score += 10
        
        if data.get("transparent_financials", False):
            score += 15
        
        return min(100, score)
    
    def _assess_earnings_consistency(self, data: Dict) -> float:
        """评估盈利一致性"""
        volatility = data.get("earnings_volatility", 1.0)
        if volatility < 0.15:
            return 90
        elif volatility < 0.25:
            return 70
        elif volatility < 0.40:
            return 50
        else:
            return 30
    
    def _apply_moat_model(self, metrics: BuffettMetrics) -> float:
        """应用护城河心智模型评分"""
        if not metrics.has_economic_moat:
            return 20
        
        score = 50
        
        # 护城河来源数量
        if len(metrics.moat_sources) >= 3:
            score += 20
        elif len(metrics.moat_sources) >= 2:
            score += 10
        
        # 持久性
        score += metrics.moat_durability_score * 0.3
        
        return min(100, score)
    
    def _apply_circle_of_competence_model(self, metrics: BuffettMetrics) -> float:
        """应用能力圈心智模型评分"""
        if not metrics.within_circle_of_competence:
            return 10
        
        score = 70
        score += metrics.business_understandability_score * 0.3
        return min(100, score)
    
    def _apply_profitability_model(self, metrics: BuffettMetrics) -> float:
        """应用盈利能力心智模型评分"""
        score = 30
        
        # ROE
        if metrics.roe > 0.20:
            score += 30
        elif metrics.roe > 0.15:
            score += 20
        elif metrics.roe > 0.12:
            score += 10
        
        # ROIC
        if metrics.roic > 0.15:
            score += 15
        elif metrics.roic > 0.10:
            score += 10
        
        # 盈利一致性
        score += metrics.earnings_consistency * 0.25
        
        # FCF
        if metrics.free_cash_flow > 0:
            score += 10
        
        return min(100, score)
    
    def _apply_management_model(self, metrics: BuffettMetrics) -> float:
        """应用管理层心智模型评分"""
        score = 50
        
        if metrics.management_quality == "excellent":
            score = 90
        elif metrics.management_quality == "good":
            score = 75
        elif metrics.management_quality == "average":
            score = 50
        else:
            score = 30
        
        # 持股一致性
        score += min(20, metrics.insider_ownership * 100)
        
        return min(100, score)
    
    def _apply_margin_of_safety_model(self, metrics: BuffettMetrics) -> float:
        """应用安全边际心智模型评分"""
        if metrics.intrinsic_value_estimate <= 0 or metrics.current_price <= 0:
            return 50
        
        margin = (metrics.intrinsic_value_estimate - metrics.current_price) / metrics.intrinsic_value_estimate
        metrics.margin_of_safety = max(0, margin)
        
        if margin > 0.40:
            return 90
        elif margin > 0.25:
            return 75
        elif margin > 0.15:
            return 60
        elif margin > 0:
            return 45
        else:
            return 25  # 溢价购买
    
    def _generate_buffett_reasoning(self, analysis: Dict, metrics: BuffettMetrics) -> List[str]:
        """生成Buffett风格的reasoning"""
        reasoning = []
        
        # 护城河
        if metrics.has_economic_moat:
            moat_str = ", ".join(metrics.moat_sources[:2])
            reasoning.append(f"护城河：{moat_str}（持久度 {metrics.moat_durability_score:.0f}/100）")
        else:
            reasoning.append("无护城河：这是一家普通公司，易受竞争侵蚀")
        
        # 能力圈
        if metrics.within_circle_of_competence:
            reasoning.append(f"能力圈内：业务可理解度 {metrics.business_understandability_score:.0f}/100")
        else:
            reasoning.append(f"⚠️ 超出能力圈（{metrics.sector}），即使数据好也不考虑")
        
        # 盈利能力
        reasoning.append(f"ROE: {metrics.roe:.1%} | ROIC: {metrics.roic:.1%} | 盈利一致性: {metrics.earnings_consistency:.0f}/100")
        
        # 财务健康
        debt_desc = "极低" if metrics.debt_to_equity < 0.3 else "低" if metrics.debt_to_equity < 0.7 else "中等" if metrics.debt_to_equity < 1.5 else "高"
        reasoning.append(f"债务水平：{debt_desc}（D/E: {metrics.debt_to_equity:.2f}）")
        
        # 估值
        if metrics.margin_of_safety > 0:
            reasoning.append(f"安全边际：{metrics.margin_of_safety:.1%}")
        else:
            reasoning.append(f"当前价格高于内在价值，安全边际为负")
        
        return reasoning
    
    def _generate_key_insights(self, analysis: Dict, metrics: BuffettMetrics) -> List[str]:
        """生成核心洞察"""
        insights = []
        
        if metrics.has_economic_moat and metrics.moat_durability_score > 70:
            insights.append("✓ 拥有持久且深厚的护城河")
        
        if metrics.roe > 0.20:
            insights.append("✓ 杰出的资本配置能力（ROE > 20%）")
        
        if metrics.earnings_consistency > 80:
            insights.append("✓ 盈利高度可预测，业务稳定")
        
        if metrics.debt_to_equity < 0.5 and metrics.free_cash_flow > 0:
            insights.append("✓ 财务堡垒：低债务 + 强现金流")
        
        if metrics.margin_of_safety > 0.30:
            insights.append("✓ 价格相对内在价值有较大折扣")
        
        return insights
    
    def _generate_checklist(self, metrics: BuffettMetrics) -> Dict:
        """生成Buffett式检查清单"""
        return {
            "护城河检查": {
                "有护城河": metrics.has_economic_moat,
                "护城河来源": metrics.moat_sources,
                "护城河持久度": f"{metrics.moat_durability_score:.0f}/100"
            },
            "能力圈检查": {
                "在能力圈内": metrics.within_circle_of_competence,
                "可理解度": f"{metrics.business_understandability_score:.0f}/100"
            },
            "财务检查": {
                "ROE > 15%": metrics.roe > 0.15,
                "债务可控": metrics.debt_to_equity < 1.0,
                "正自由现金流": metrics.free_cash_flow > 0
            },
            "估值检查": {
                "有安全边际": metrics.margin_of_safety > 0.20,
                "安全边际": f"{metrics.margin_of_safety:.1%}"
            }
        }
    
    def _select_relevant_quote(self, analysis: Dict, metrics: BuffettMetrics) -> str:
        """选择相关的Buffett名言"""
        if not metrics.has_economic_moat:
            return """When a management with a reputation for brilliance tackles a business with a reputation for bad economics, it is the reputation of the business that remains intact."""
        
        if not metrics.within_circle_of_competence:
            return """Risk comes from not knowing what you're doing."""
        
        if metrics.margin_of_safety < 0.15:
            return """Price is what you pay. Value is what you get."""
        
        if analysis["signal"] == Signal.BULLISH:
            return """It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price."""
        
        return """Be fearful when others are greedy, and greedy when others are fearful."""
    
    def get_mental_model(self, name: str) -> Optional[MentalModel]:
        """获取特定心智模型"""
        for model in self.mental_models:
            if model.name == name:
                return model
        return None
    
    def get_all_mental_models(self) -> List[MentalModel]:
        """获取所有心智模型"""
        return self.mental_models
    
    def get_decision_heuristics(self) -> List[DecisionHeuristic]:
        """获取所有决策启发式"""
        return self.decision_heuristics
    
    def get_anti_patterns(self) -> List[AntiPattern]:
        """获取所有反模式"""
        return self.anti_patterns
    
    def get_expression_dna(self) -> ExpressionDNA:
        """获取表达DNA"""
        return self.expression_dna
    
    def get_intellectual_lineage(self) -> IntellectualLineage:
        """获取智识谱系"""
        return self.intellectual_lineage
    
    def get_internal_tensions(self) -> List[InternalTension]:
        """获取内在张力"""
        return self.internal_tensions
    
    def get_honesty_boundaries(self) -> List[HonestyBoundary]:
        """获取诚实边界"""
        return self.honesty_boundaries
    
    def express_as_buffett(self, message: str) -> str:
        """
        用Buffett的表达DNA重写消息
        
        这是一个实验性功能，用于生成更像Buffett的表达
        """
        # 添加典型的Buffett前缀
        prefixes = [
            "Well, ",
            "You know, ",
            "The thing is, ",
            "Look, ",
            "In my view, "
        ]
        
        # 使用比喻
        metaphors = [
            "like a snowball rolling down a hill",
            "as if you were buying a farm",
            "think of it like a bond with a rising coupon"
        ]
        
        # 自我调侃
        self_deprecating = [
            "I've made plenty of mistakes in this area, but...",
            "If I were smarter, I would have...",
            "I don't claim to be an expert, but..."
        ]
        
        # 这里可以实现更复杂的重写逻辑
        return message


# ============================================================================
# 工厂函数
# ============================================================================

def create_buffett_agent_v2() -> WarrenBuffettDistilledV2:
    """创建Buffett思维框架实例"""
    return WarrenBuffettDistilledV2()


def get_buffett_framework_summary() -> Dict:
    """
    获取Buffett思维框架摘要
    用于快速了解这套框架的核心内容
    """
    agent = WarrenBuffettDistilledV2()
    
    return {
        "name": agent.name,
        "philosophy": agent.philosophy,
        "mental_models": [
            {
                "name": m.name,
                "description": m.description,
                "limitation": m.limitation
            }
            for m in agent.mental_models
        ],
        "decision_heuristics_count": len(agent.decision_heuristics),
        "anti_patterns_count": len(agent.anti_patterns),
        "internal_tensions_count": len(agent.internal_tensions),
        "honesty_boundaries_count": len(agent.honesty_boundaries),
        "intellectual_lineage": {
            "influences": [i["name"] for i in agent.intellectual_lineage.influences],
            "position": agent.intellectual_lineage.position_in_map
        }
    }


# ============================================================================
# 测试
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Warren Buffett 思维框架蒸馏 - 女娲方法论完整版 v2")
    print("=" * 70)
    
    agent = WarrenBuffettDistilledV2()
    
    # 展示心智模型
    print("\n【心智模型】")
    for i, model in enumerate(agent.mental_models, 1):
        print(f"\n{i}. {model.name}")
        print(f"   {model.description}")
        print(f"   局限: {model.limitation}")
    
    # 展示决策启发式
    print("\n\n【决策启发式（精选）】")
    for i, h in enumerate(agent.decision_heuristics[:3], 1):
        print(f"\n{i}. {h.rule}")
        print(f"   反事实: {h.counterfactual[:100]}...")
    
    # 展示反模式
    print("\n\n【反模式（永远不会做的事）】")
    for i, ap in enumerate(agent.anti_patterns[:3], 1):
        print(f"\n{i}. {ap.behavior}")
        print(f"   原因: {ap.reason}")
    
    # 展示内在张力
    print("\n\n【内在张力】")
    for i, t in enumerate(agent.internal_tensions, 1):
        print(f"\n{i}. {t.tension_name}")
        print(f"   A: {t.pole_a}")
        print(f"   B: {t.pole_b}")
    
    # 测试分析
    print("\n\n" + "=" * 70)
    print("测试分析: 模拟苹果公司")
    print("=" * 70)
    
    test_data = {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "roe": 0.28,
        "roic": 0.25,
        "debt_to_equity": 0.35,
        "free_cash_flow": 99e9,
        "operating_margin": 0.30,
        "gross_margin": 0.45,
        "pe_ratio": 28,
        "peg_ratio": 1.8,
        "price_to_book": 8.5,
        "sector": "Technology",
        "insider_ownership": 0.05,
        "earnings_volatility": 0.10,
        "revenue_volatility": 0.08,
        "brand_strength": 0.95,
        "has_network_effect": True,
        "switching_cost": 0.75,
        "ecosystem_lockin": True,
        "years_of_competitive_advantage": 15,
        "industry_stability": True,
        "business_simple": False,  # 科技公司相对复杂
        "management_quality": "excellent",
        "current_price": 175.0,
        "intrinsic_value": 200.0
    }
    
    result = agent.analyze(test_data)
    
    print(f"\n信号: {result['signal'].upper()}")
    print(f"置信度: {result['confidence']:.1f}%")
    print(f"\n核心推理:")
    for r in result['reasoning']:
        print(f"  • {r}")
    
    print(f"\n关键洞察:")
    for i in result['key_insights']:
        print(f"  {i}")
    
    print(f"\n危险信号:")
    if result['red_flags']:
        for f in result['red_flags']:
            print(f"  ⚠️ {f}")
    else:
        print("  ✓ 无重大危险信号")
    
    print(f"\n反事实分析:")
    for cf in result['counterfactual_analysis']['counterfactual_scenarios'][:2]:
        print(f"  • {cf['scenario']}")
        print(f"    影响: {cf['impact']}")
    
    print(f"\n相关名言:")
    print(f'  "{result["buffett_quote"]}"')
    
    print("\n\n" + "=" * 70)
    print("诚实边界提醒:")
    print("=" * 70)
    for i, hb in enumerate(agent.honesty_boundaries[:3], 1):
        print(f"\n{i}. {hb.limitation}")
        print(f"   原因: {hb.reason}")

