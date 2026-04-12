#!/usr/bin/env python3
"""
Bill Ackman 思维框架蒸馏 V2 - 女娲方法论完整版

核心理念：高置信度集中投资 + 催化剂驱动维权

【心智模型】(5个)
1. 高置信度集中持仓模型 - 只投最好的，重仓下注
2. 催化剂驱动模型 - 每个投资必须有明确的事件催化剂
3. 企业家式所有权模型 - 像运营公司一样做投资
4. 错误定价发现模型 - 市场错配 = 超额收益来源
5. 运营改善创造价值模型 - α来自管理层变革

【决策启发式】(8条)
1. 只投你敢重仓10%的标的
2. 必须有清晰的"这会在X时间因为Y原因上涨" thesis
3. 失败的教训比成功更重要
4. 等待是一种美德
5. 运营改善比行业β更重要
6. 简单易懂的业务 > 复杂业务
7. 强大的自由现金流是底线
8. 管理层持股是激励对齐的前提

【反模式】
- 不会撒胡椒面式分散投资
- 不会投资没有清晰thesis的标的
- 不会在下跌时盲目加仓
- 不会忽视公司治理问题
- 不会投资自己无法影响的小公司

【内在张力】
- 高集中度 vs 高波动性
- 长期价值创造 vs 短期催化剂驱动
- 主动维权 vs 被动持有

【诚实边界】
- 高波动性不可避免
- 需要深入研究和高参与度
- 维权投资需要大资金门槛
- 单一持仓可能亏损50%以上
- 历史教训：Valeant 证明了忽视商业模式的致命风险

【智识谱系】
受格雷厄姆、巴菲特、查理·芒格影响
影响：新一代维权投资者

调研时间：2026年4月
来源：Ackman投资者信、CNBC采访、播客、Valeant/Herbalife案例研究
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Signal(Enum):
    """投资信号枚举"""
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class ThesisStrength(Enum):
    """Thesis 强度等级"""
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    CONVICTION = "high_conviction"


@dataclass
class Catalyst:
    """催化剂数据结构"""
    type: str
    description: str
    timeline: str
    probability: float
    impact: float


@dataclass
class AnalysisResult:
    """分析结果数据结构"""
    agent: str
    signal: Signal
    confidence: float
    thesis_strength: ThesisStrength
    reasoning: List[str]
    catalysts: List[Catalyst]
    red_flags: List[str]
    key_metrics: Dict[str, float]
    position_recommendation: Dict
    limitations: List[str]


class BillAckmanDistilled:
    """
    Bill Ackman 思维框架 - 女娲方法论完整版
    
    Ackman 的投资哲学建立在三个核心支柱上：
    1. 高置信度集中投资 - 只投最好的，重仓下注
    2. 催化剂驱动 - 每个投资必须有明确的催化剂
    3. 企业家式所有权 - 像运营公司一样做投资
    
    这个框架适用于：
    - 价值投资分析
    - 公司治理评估
    - 催化剂识别
    - 仓位管理决策
    """
    
    # === 心智模型定义 ===
    MENTAL_MODELS = {
        "high_conviction_concentration": {
            "name": "高置信度集中持仓模型",
            "description": "找到最好的机会，重仓下注。分散是对无知的保护。",
            "core_thesis": "如果你知道自己在做什么，分散是愚蠢的",
            "application": "只有当thesis强度达到conviction级别时才投资",
            "limitation": "需要极高的研究深度和正确率"
        },
        "catalyst_driven": {
            "name": "催化剂驱动模型", 
            "description": "投资必须有明确的催化剂推动价值实现",
            "core_thesis": "价值会自己说话，但需要催化剂让它开口",
            "application": "每个投资必须有'这会在X时间因为Y原因上涨'的清晰逻辑",
            "limitation": "催化剂可能延迟或失效"
        },
        "ownership_mentality": {
            "name": "企业家式所有权模型",
            "description": "像企业家一样思考和行动，不只是被动持有者",
            "core_thesis": "买股票就是买公司的一部分",
            "application": "主动参与公司治理，推动运营改善",
            "limitation": "需要足够规模和影响力"
        },
        "mispricing_discovery": {
            "name": "错误定价发现模型",
            "description": "市场错配是超额收益的主要来源",
            "core_thesis": "找到市场错误定价的机会，等待价值回归",
            "application": "寻找market misunderstanding导致的低估机会",
            "limitation": "市场可能长期非理性"
        },
        "operational_improvement": {
            "name": "运营改善创造价值模型",
            "description": "真正的α来自主动推动运营改善",
            "core_thesis": "好的管理可以让普通生意变好，坏的管理可以让好生意变糟",
            "application": "评估运营改善空间和执行力",
            "limitation": "需要管理层配合和市场环境支持"
        }
    }
    
    # === 决策启发式 ===
    DECISION_HEURISTICS = [
        {
            "rule": "只投你敢重仓10%的标的",
            "rationale": "如果不敢重仓，说明信心不足",
            "test": "问：如果这只股票跌30%，我敢加仓吗？"
        },
        {
            "rule": "必须有清晰的 catalyst + timeline + thesis",
            "rationale": "模糊的投资逻辑无法管理",
            "test": "能否用一句话说清楚为什么现在买，什么时候卖？"
        },
        {
            "rule": "失败的教训比成功更重要",
            "rationale": "Valeant、Herbalife的教训塑造了更好的投资者",
            "test": "研究这个投资可能怎么失败，而不是只盯着上行"
        },
        {
            "rule": "等待是一种美德",
            "rationale": "现金是一种选择权，可以在机会不明显时空仓",
            "test": "如果现在不投，6个月后会后悔吗？"
        },
        {
            "rule": "简单易懂的业务 > 复杂业务",
            "rationale": "你不懂的业务无法真正评估风险",
            "test": "能否向一个高中生解释清楚这家公司怎么赚钱？"
        },
        {
            "rule": "强大的自由现金流是底线",
            "rationale": "没有现金流的账面利润是海市蜃楼",
            "test": "FCF yield是否高于无风险利率+风险溢价？"
        },
        {
            "rule": "管理层持股是激励对齐的前提",
            "rationale": "不跟股东一起下注的管理层不值得信任",
            "test": "insider ownership是否>5%？"
        },
        {
            "rule": "运营改善比行业β更重要",
            "rationale": "行业增长会掩盖管理问题，但运营改善创造持久价值",
            "test": "即使行业增速放缓，这家公司还能不能增长？"
        }
    ]
    
    # === 反模式（Ackman绝对不会做的事） ===
    ANTI_PATTERNS = [
        "撒胡椒面式分散投资（对无知的保护）",
        "投资没有清晰thesis的标的",
        "在下跌时盲目加仓而不基于新信息",
        "忽视公司治理和资本配置问题",
        "投资自己无法影响的小市值公司",
        "做空时没有明确的时间线和催化剂",
        "持有需要持续融资的烧钱业务"
    ]
    
    # === 表达DNA ===
    EXPRESSION_DNA = {
        "sentence_structure": "长句为主，逻辑严密，结论先行",
        "vocabulary": ["conviction", "catalyst", "misunderstanding", "value creation", "opportunity"],
        "certainty": "高确定性表达，'clearly', 'obviously'",
        "rhetoric": "类比丰富，喜欢用具体案例说明抽象概念",
        "pace": "先给出结论，再展开论证",
        "emotion": "理性冷静，但对错误会强烈批判"
    }
    
    # === 内在张力 ===
    INTRINSIC_TENSIONS = [
        {
            "tension": "高集中度 vs 高波动性",
            "ackman_view": "接受波动性作为高回报的代价",
            "resolution": "通过深度研究和积极管理来降低实质风险"
        },
        {
            "tension": "长期价值创造 vs 短期催化剂驱动",
            "ackman_view": "催化剂是推动长期价值实现的加速器",
            "resolution": "寻找既有长期价值又有短期催化剂的标的"
        },
        {
            "tension": "主动维权 vs 被动持有",
            "ackman_view": "被动持有是对管理层的纵容",
            "resolution": "只在必要时维权，但随时准备行动"
        }
    ]
    
    # === 历史教训 ===
    HISTORICAL_LESSONS = [
        {
            "case": "Valeant Pharmaceuticals",
            "lesson": "忽视商业模式的致命风险（药品定价依赖政治风险）",
            "impact": "从巨大成功到失败，彻底改变了对复杂会计的认知"
        },
        {
            "case": "Herbalife",
            "lesson": "即使是高置信度做空也可能错，市场可能长期非理性",
            "impact": "展示了做空的非对称风险（最大损失无限）"
        },
        {
            "case": "Chipotle",
            "lesson": "运营改善可以创造巨大价值，但需要时间和执行力",
            "impact": "强化了运营改善型投资的信心"
        },
        {
            "case": "Canadian Pacific Railway",
            "lesson": "维权投资可以改变公司治理结构，创造价值",
            "impact": "验证了积极投资者模式的潜力"
        }
    ]
    
    def __init__(self):
        self.name = "Bill Ackman"
        self.philosophy = "High Conviction + Catalyst-Driven + Ownership Mentality"
        self.influence = ["Graham", "Buffett", "Munger"]
        self.research_date = "2026-04"
    
    def analyze(self, data: Dict) -> AnalysisResult:
        """
        使用 Ackman 的思维框架分析股票
        
        流程：
        1. 评估 thesis 强度（35%权重）
        2. 识别催化剂（必须有）
        3. 评估护城河（25%权重）
        4. 评估估值（20%权重）
        5. 评估治理（20%权重）
        6. 综合判断
        """
        reasoning = []
        
        # 1. 评估 thesis 强度
        thesis_score = self._assess_thesis(data)
        thesis_strength = self._get_thesis_strength(thesis_score)
        reasoning.append(f"Thesis score: {thesis_score:.1f}/100 ({thesis_strength.value})")
        
        # 2. 识别催化剂
        catalysts = self._identify_catalysts(data)
        catalyst_score = min(100, len(catalysts) * 20)
        reasoning.append(f"Identified {len(catalysts)} catalysts")
        
        # 3. 评估护城河
        moat_score = self._assess_moat(data)
        reasoning.append(f"Moat score: {moat_score:.1f}/100")
        
        # 4. 评估估值
        valuation_score = self._assess_valuation(data)
        reasoning.append(f"Valuation score: {valuation_score:.1f}/100")
        
        # 5. 评估治理
        governance_score = self._assess_governance(data)
        reasoning.append(f"Governance score: {governance_score:.1f}/100")
        
        # 6. 综合评分
        total_score = (
            thesis_score * 0.35 +
            moat_score * 0.25 +
            valuation_score * 0.20 +
            governance_score * 0.20
        )
        
        # 生成信号
        signal, confidence = self._generate_signal(total_score, catalysts)
        
        # 7. 识别风险
        red_flags = self._identify_red_flags(data)
        
        # 8. 仓位建议
        position_recommendation = self._assess_position_size(thesis_score, data)
        
        # 9. 诚实边界
        limitations = self._get_limitations(data)
        
        key_metrics = {
            "thesis_score": round(thesis_score, 1),
            "moat_score": round(moat_score, 1),
            "valuation_score": round(valuation_score, 1),
            "governance_score": round(governance_score, 1),
            "total_score": round(total_score, 1),
            "catalyst_count": len(catalysts)
        }
        
        return AnalysisResult(
            agent=self.name,
            signal=signal,
            confidence=confidence,
            thesis_strength=thesis_strength,
            reasoning=reasoning,
            catalysts=catalysts,
            red_flags=red_flags,
            key_metrics=key_metrics,
            position_recommendation=position_recommendation,
            limitations=limitations
        )
    
    def _assess_thesis(self, data: Dict) -> float:
        """
        评估投资 thesis 的清晰度和强度
        
        Ackman 要求：
        1. 清晰的 value thesis（为什么被低估）
        2. 明确的催化剂
        3. 具体的时间线
        4. 对风险的理解
        5. 强大的自由现金流
        6. 业务可预测性
        """
        score = 50.0
        
        # 价值 thesis 清晰度
        if data.get("has_value_thesis", False):
            score += 15
        
        # 催化剂存在性
        if len(data.get("catalysts", [])) > 0:
            score += 15
        
        # 时间线明确性
        if data.get("has_estimated_timeline", False):
            score += 10
        
        # 风险识别完整性
        if data.get("has_risk_assessment", False):
            score += 5
        
        # 自由现金流生成能力
        fcf_yield = data.get("free_cash_flow_yield", 0)
        if fcf_yield > 0.10:
            score += 10
        elif fcf_yield > 0.05:
            score += 5
        elif fcf_yield < 0:
            score -= 15
        
        # 业务可预测性
        business_predictability = data.get("business_predictability", 0.5)
        score += business_predictability * 10
        
        # 商业模式简单性
        if data.get("simple_business_model", False):
            score += 5
        
        return max(20.0, min(95.0, score))
    
    def _get_thesis_strength(self, score: float) -> ThesisStrength:
        """根据分数返回 thesis 强度等级"""
        if score >= 80:
            return ThesisStrength.CONVICTION
        elif score >= 65:
            return ThesisStrength.STRONG
        elif score >= 50:
            return ThesisStrength.MODERATE
        else:
            return ThesisStrength.WEAK
    
    def _identify_catalysts(self, data: Dict) -> List[Catalyst]:
        """识别可能的催化剂并评估质量"""
        catalysts = []
        
        # 催化剂类型映射
        catalyst_mapping = [
            ("has_activist_investor", "Activist involvement", "6-12 months", 0.7),
            ("has_share_repurchase", "Share buybacks", "Ongoing", 0.6),
            ("has_dividend_increase", "Dividend growth", "12-24 months", 0.6),
            ("has_management_change", "New management", "6-18 months", 0.75),
            ("has_operational_improvement", "Operational improvement", "12-36 months", 0.65),
            ("has_asset_light_strategy", "Asset restructuring", "12-24 months", 0.7),
            ("has_merger_speculation", "M&A/Spin-off", "6-18 months", 0.5),
            ("has_regulatory_resolution", "Regulatory clarity", "3-12 months", 0.8),
            ("has_new_product_launch", "Product launch", "6-18 months", 0.55),
        ]
        
        for key, description, timeline, probability in catalyst_mapping:
            if data.get(key, False):
                catalysts.append(Catalyst(
                    type=key.replace("has_", ""),
                    description=description,
                    timeline=timeline,
                    probability=probability,
                    impact=0.2 + probability * 0.3  # 基础影响 + 概率加成
                ))
        
        return catalysts
    
    def _assess_moat(self, data: Dict) -> float:
        """
        评估护城河 - Ackman 非常看重长期竞争壁垒
        
        关注：
        - 市场份额稳定性
        - 品牌实力
        - 转换成本
        - 自由现金流利润率
        - 资本回报可持续性
        """
        score = 50.0
        
        # 市场份额
        market_share = data.get("market_share", 0)
        if market_share > 0.30:
            score += 20
        elif market_share > 0.15:
            score += 10
        
        # 品牌实力
        brand_strength = data.get("brand_strength", 0)
        if brand_strength > 0.7:
            score += 15
        elif brand_strength > 0.5:
            score += 8
        
        # 转换成本
        switching_cost = data.get("switching_cost", 0)
        if switching_cost > 0.5:
            score += 10
        elif switching_cost > 0.3:
            score += 5
        
        # 自由现金流利润率
        fcf_margin = data.get("free_cash_flow_margin", 0)
        if fcf_margin > 0.15:
            score += 15
        elif fcf_margin > 0.10:
            score += 8
        elif fcf_margin < 0.05:
            score -= 10
        
        # ROIC 持续性
        roic = data.get("return_on_invested_capital", 0)
        if roic > 0.15:
            score += 10
        elif roic < 0.10:
            score -= 5
        
        return max(20.0, min(95.0, score))
    
    def _assess_valuation(self, data: Dict) -> float:
        """
        评估估值 - Ackman 倾向用 DCF 和 EV/EBITDA
        
        关键指标：
        - EV/EBITDA
        - P/S（用于成长型）
        - FCF Yield
        - 与历史平均比较
        """
        score = 50.0
        
        # EV/EBITDA 评估
        ev_ebitda = data.get("ev_ebitda", 0)
        if ev_ebitda > 0:
            if ev_ebitda < 8:
                score += 25
            elif ev_ebitda < 12:
                score += 15
            elif ev_ebitda < 15:
                score += 5
            elif ev_ebitda > 20:
                score -= 15
            elif ev_ebitda > 25:
                score -= 25
        
        # P/S 评估（成长型公司）
        ps_ratio = data.get("price_to_sales", 0)
        if ps_ratio > 0:
            if ps_ratio < 2:
                score += 15
            elif ps_ratio < 4:
                score += 8
            elif ps_ratio > 10:
                score -= 15
            elif ps_ratio > 15:
                score -= 25
        
        # FCF Yield
        fcf_yield = data.get("free_cash_flow_yield", 0)
        if fcf_yield > 0.12:
            score += 15
        elif fcf_yield > 0.08:
            score += 8
        elif fcf_yield < 0.03:
            score -= 15
        
        # 相对于历史估值
        vs_historical = data.get("valuation_vs_historical", 1.0)
        if vs_historical < 0.8:
            score += 10
        elif vs_historical > 1.5:
            score -= 10
        
        return max(15.0, min(90.0, score))
    
    def _assess_governance(self, data: Dict) -> float:
        """
        评估公司治理 - Ackman 作为维权投资者非常看重这点
        
        关注：
        - 管理层持股
        - 独立董事比例
        - 历史不当行为
        - 资本配置记录
        - 管理层稳定性
        """
        score = 50.0
        
        # 管理层持股
        insider_ownership = data.get("insider_ownership", 0)
        if insider_ownership > 0.15:
            score += 20
        elif insider_ownership > 0.10:
            score += 15
        elif insider_ownership > 0.03:
            score += 8
        elif insider_ownership < 0.01:
            score -= 15
        
        # 独立董事比例
        independent_board_pct = data.get("independent_board_pct", 0.5)
        if independent_board_pct > 0.75:
            score += 10
        elif independent_board_pct < 0.50:
            score -= 10
        
        # 治理问题
        has_governance_issues = data.get("has_governance_issues", False)
        if has_governance_issues:
            score = max(10, score - 30)
        
        # 资本配置
        has_good_capital_allocation = data.get("has_good_capital_allocation", True)
        if not has_good_capital_allocation:
            score -= 20
        
        # CEO 任期（稳定性）
        ceo_tenure_years = data.get("ceo_tenure_years", 3)
        if ceo_tenure_years > 10:
            score += 5
        elif ceo_tenure_years < 2:
            score -= 5  # 新管理层不确定性
        
        return max(15.0, min(95.0, score))
    
    def _identify_red_flags(self, data: Dict) -> List[str]:
        """识别风险信号 - Valeant 教训的结晶"""
        flags = []
        
        # 业务风险
        if data.get("has_turnaround_risk", False):
            flags.append("⚠️ Business turnaround required - higher risk")
        
        if data.get("has_regulatory_risk", False):
            flags.append("⚠️ Significant regulatory risk (Valeant lesson)")
        
        if data.get("has_technology_disruption", False):
            flags.append("⚠️ Technology disruption threat")
        
        if data.get("political_pricing_risk", False):
            flags.append("🚫 Political pricing risk - Ackman avoids (Valeant)")
        
        # 财务风险
        debt_to_ebitda = data.get("debt_to_ebitda", 0)
        if debt_to_ebitda > 4:
            flags.append(f"⚠️ High leverage (D/EBITDA {debt_to_ebitda:.1f}x)")
        elif debt_to_ebitda > 6:
            flags.append("🚫 Excessive leverage - major red flag")
        
        if data.get("negative_fcf", False):
            flags.append("🚫 Negative free cash flow")
        
        if data.get("requires_continuous_funding", False):
            flags.append("🚫 Requires continuous external funding")
        
        # 治理风险
        if data.get("has_governance_issues", False):
            flags.append("🚫 Corporate governance concerns")
        
        if data.get("insider_ownership", 0) < 0.01:
            flags.append("⚠️ Minimal insider ownership - misalignment risk")
        
        if data.get("accounting_complexity", 0) > 0.7:
            flags.append("⚠️ Complex accounting (Valeant lesson)")
        
        return flags
    
    def _generate_signal(self, total_score: float, catalysts: List[Catalyst]) -> Tuple[Signal, float]:
        """生成投资信号和置信度"""
        # 必须有催化剂才能看涨
        has_catalyst = len(catalysts) > 0
        
        if total_score >= 75 and has_catalyst:
            signal = Signal.BULLISH
            confidence = min(95.0, total_score + 5)
        elif total_score >= 75 and not has_catalyst:
            signal = Signal.NEUTRAL
            confidence = 55.0  # 低置信度因为没有催化剂
        elif total_score <= 40:
            signal = Signal.BEARISH
            confidence = max(20.0, 100 - total_score)
        else:
            signal = Signal.NEUTRAL
            confidence = total_score
        
        return signal, round(confidence, 1)
    
    def _assess_position_size(self, thesis_score: float, data: Dict) -> Dict:
        """
        Ackman 的仓位管理：thesis越强，仓位越大
        
        原则：
        - 高 conviction: 5-10%
        - 中等 conviction: 2-5%
        - 低 conviction: 0-2%
        """
        risk_factors = 1.0
        
        # 风险调整
        if data.get("has_regulatory_risk", False):
            risk_factors *= 0.7
        if data.get("debt_to_ebitda", 0) > 4:
            risk_factors *= 0.8
        if len(data.get("catalysts", [])) < 2:
            risk_factors *= 0.9
        
        base_allocation = thesis_score / 10  # 理论上最大10%
        recommended_pct = min(10, max(0, base_allocation * risk_factors))
        
        # 确定等级
        if recommended_pct >= 7:
            allocation_level = "High Conviction - Core Position"
        elif recommended_pct >= 4:
            allocation_level = "Moderate Conviction - Standard Position"
        elif recommended_pct >= 1:
            allocation_level = "Low Conviction - Speculative"
        else:
            allocation_level = "Insufficient Conviction - Pass"
        
        return {
            "recommended_allocation_pct": round(recommended_pct, 1),
            "allocation_level": allocation_level,
            "rationale": f"Thesis score {thesis_score:.0f}/100, Risk factor {risk_factors:.2f}",
            "max_ackman_style": "5-10% for highest conviction bets",
            "cash_is_option": "OK to hold cash if no high-conviction ideas"
        }
    
    def _get_limitations(self, data: Dict) -> List[str]:
        """诚实边界 - 明确说明框架的局限性"""
        return [
            "⚠️ High concentration means high volatility - expect 30-50% drawdowns in individual positions",
            "⚠️ Requires deep research and high engagement - not passive investing",
            "⚠️ Activist investing requires substantial capital - retail investors cannot replicate",
            "⚠️ Single positions can lose 50%+ - Herbalife/Valeant lessons",
            "⚠️ Catalyst timing is uncertain - investments may underperform for years",
            "⚠️ Framework assumes ability to influence management - not applicable to small caps",
            "⚠️ High confidence can still be wrong - Ackman's track record includes major failures",
            "⚠️ This is a simulation based on public statements, not Ackman's actual thinking"
        ]
    
    def get_mental_model(self, model_name: str) -> Optional[Dict]:
        """获取特定心智模型的详细说明"""
        return self.MENTAL_MODELS.get(model_name)
    
    def list_mental_models(self) -> List[str]:
        """列出所有心智模型"""
        return list(self.MENTAL_MODELS.keys())
    
    def get_decision_heuristics(self) -> List[Dict]:
        """获取所有决策启发式"""
        return self.DECISION_HEURISTICS
    
    def get_anti_patterns(self) -> List[str]:
        """获取反模式列表"""
        return self.ANTI_PATTERNS
    
    def get_historical_lessons(self) -> List[Dict]:
        """获取历史教训"""
        return self.HISTORICAL_LESSONS
    
    def get_expression_dna(self) -> Dict:
        """获取表达DNA"""
        return self.EXPRESSION_DNA
    
    def print_analysis_summary(self, result: AnalysisResult) -> None:
        """打印分析摘要"""
        print(f"\n{'='*60}")
        print(f"🎯 Bill Ackman 分析结果")
        print(f"{'='*60}")
        print(f"信号: {result.signal.value.upper()}")
        print(f"置信度: {result.confidence}%")
        print(f"Thesis强度: {result.thesis_strength.value}")
        print(f"\n📊 关键指标:")
        for k, v in result.key_metrics.items():
            print(f"  • {k}: {v}")
        print(f"\n💰 仓位建议:")
        for k, v in result.position_recommendation.items():
            print(f"  • {k}: {v}")
        if result.catalysts:
            print(f"\n🚀 催化剂 ({len(result.catalysts)}个):")
            for c in result.catalysts:
                print(f"  • {c.description} ({c.timeline}, 概率{c.probability:.0%})")
        if result.red_flags:
            print(f"\n🚩 风险信号:")
            for flag in result.red_flags:
                print(f"  {flag}")
        print(f"\n🧠 推理过程:")
        for r in result.reasoning:
            print(f"  • {r}")
        print(f"{'='*60}\n")


# === 导出函数 ===
def create_ackman_agent() -> BillAckmanDistilled:
    """创建 Bill Ackman 蒸馏代理"""
    return BillAckmanDistilled()


# === 示例用法 ===
if __name__ == "__main__":
    # 创建代理
    ackman = create_ackman_agent()
    
    # 示例数据（模拟一个典型 Ackman 风格的投资机会）
    example_data = {
        # Thesis 相关
        "has_value_thesis": True,
        "has_estimated_timeline": True,
        "has_risk_assessment": True,
        "simple_business_model": True,
        
        # 财务指标
        "free_cash_flow_yield": 0.12,
        "business_predictability": 0.8,
        "ev_ebitda": 10,
        "price_to_sales": 2.5,
        "free_cash_flow_margin": 0.18,
        "return_on_invested_capital": 0.18,
        "debt_to_ebitda": 2.5,
        
        # 护城河
        "market_share": 0.25,
        "brand_strength": 0.75,
        "switching_cost": 0.4,
        
        # 催化剂
        "has_management_change": True,
        "has_share_repurchase": True,
        "has_operational_improvement": True,
        "catalysts": ["management_change", "buybacks", "ops_improvement"],
        
        # 治理
        "insider_ownership": 0.12,
        "independent_board_pct": 0.80,
        "has_good_capital_allocation": True,
        "ceo_tenure_years": 5,
        
        # 估值
        "valuation_vs_historical": 0.85,
        
        # 风险
        "has_governance_issues": False,
        "has_regulatory_risk": False,
        "negative_fcf": False
    }
    
    # 执行分析
    result = ackman.analyze(example_data)
    ackman.print_analysis_summary(result)
    
    # 展示心智模型
    print("\n📚 Bill Ackman 心智模型:")
    for name, model in ackman.MENTAL_MODELS.items():
        print(f"\n  • {model['name']}")
        print(f"    {model['description']}")
        print(f"    应用: {model['application']}")
    
    # 展示决策启发式
    print("\n🧭 决策启发式 (Top 3):")
    for i, h in enumerate(ackman.get_decision_heuristics()[:3], 1):
        print(f"  {i}. {h['rule']}")
        print(f"     测试: {h['test']}")
