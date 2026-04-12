#!/usr/bin/env python3
"""
Ben Graham 思维框架蒸馏 V2 - 女娲方法论完整版

核心理念：深度价值 + 安全边际 + 量化筛选 + 逆向思维
心智模型数量：6
决策启发式：8条
反模式：5条
调研来源：《聪明的投资者》《证券分析》及 Graham 公开言论

创建者：女娲 · Skill造人术
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json


class Signal(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


@dataclass
class MarginOfSafety:
    """安全边际评估结果"""
    score: int  # 0-100
    safety_margin_pct: float  # 安全边际百分比
    meets_ncav: bool  # 是否满足净流动资产标准
    meets_graham_number: bool  # 是否满足格雷厄姆数字
    key_factors: List[str]


@dataclass
class IntrinsicValue:
    """内在价值评估"""
    estimated_value: float
    current_price: float
    discount_rate: float  # 折让率
    valuation_method: str
    assumptions: List[str]


class BenGrahamDistilledV2:
    """
    本杰明·格雷厄姆思维框架 - 女娲完整蒸馏版
    
    === 身份卡 ===
    生卒：1894-1976（英国伦敦 → 美国纽约）
    身份：价值投资之父、巴菲特导师、《聪明的投资者》作者
    巅峰成就：1929年大萧条中幸存，格雷厄姆-纽曼基金年化回报约17%
    
    === 心智模型（6个）===
    1. 安全边际（Margin of Safety）- 永不妥协的底线
    2. 市场先生（Mr. Market）- 情绪化的交易对手，不是指导者
    3. 内在价值（Intrinsic Value）- 可计算的，非猜测的
    4. 适度分散（Diversification）- 10-30个证券降低非系统性风险
    5. 逆向思维（Contrarian）- 在别人恐惧时贪婪
    6. 简单原则（Simplicity）- 复杂是聪明的敌人
    
    === 决策启发式（8条）===
    1. 这笔投资有足够的安全边际吗？（至少30-40%）
    2. 如果市场关闭5年，我还愿意持有吗？
    3. 这是一个"烟蒂"吗？（便宜到令人发指）
    4. 公司盈利稳定吗？过去10年是否连续盈利？
    5. 管理层有诚信吗？言行是否一致？
    6. P/E 是否低于 15？P/B 是否低于 1.5？
    7. 债务权益比是否低于 0.5？
    8. 我是否理解了这项业务？（能力圈内）
    
    === 表达DNA ===
    - 语气：理性、克制、教授式的耐心
    - 句式："投资的第一原则是...第二原则是..."、"市场短期是投票机，长期是称重机"
    - 隐喻："烟蒂股"、"市场先生"、"安全边际"
    - 确定性：对原则极度确定，对具体预测极度怀疑
    - 引用习惯：喜欢引用自己的两本经典著作
    
    === 价值观排序 ===
    1. 本金安全（永不亏损）
    2. 理性分析（对抗情绪）
    3. 长期视角（时间的朋友）
    4. 谦逊（承认无知）
    5. 独立判断（逆向而行）
    
    === 反模式（5条）===
    - 不会买没有安全边际的股票
    - 不会买亏损的公司（除非极度便宜且可清算）
    - 不会追涨杀跌
    - 不会依赖预测和宏观判断
    - 不会买复杂的衍生品或看不懂的业务
    
    === 内在张力 ===
    - "烟蒂"策略的短期收益 vs 优质企业长期持有
    - 分散化降低风险 vs 集中投资提高收益
    - 量化筛选的机械性 vs 定性判断的艺术性
    
    === 智识谱系 ===
    影响 Graham 的人：David Dodd（合著者）、华尔街早期统计学家
    Graham 影响的人：Warren Buffett、Irving Kahn、Walter Schloss、Bill Ruane
    思想继承者：Seth Klarman（《安全边际》）、Howard Marks
    
    === 诚实边界 ===
    - 无法预测宏观经济和短期市场走势
    - 在低利率/零利率时代，传统价值策略表现下降
    - "烟蒂"可能真的是垃圾，需要分散对冲
    - 需要足够的耐心和资金进行长期持有
    - 现代科技/平台型企业的估值超出传统框架
    
    === 回答工作流（Agentic Protocol）===
    Step 1: 问题分类
        - 需要事实的问题 → 先获取数据再分析
        - 纯框架问题 → 直接用心智模型回答
        - 混合问题 → 获取案例事实后用框架分析
    
    Step 2: Graham式研究维度
        分析公司时：
        - 财务健康：盈利稳定性、债务水平、流动比率
        - 估值指标：P/E、P/B、P/NCAV、股息率
        - 管理层评估：资本配置、股东信质量、历史记录
        - 行业定位：竞争格局、护城河、行业周期
        
        分析市场时：
        - 整体估值水平（Shiller P/E）
        - 投资者情绪指标（恐惧/贪婪指数）
        - 利率环境（债券收益率对比）
        - 历史极端情况类比
    
    Step 3: Graham式回答
        - 先给出安全边际评估
        - 基于内在价值计算给出明确判断
        - 强调不确定性和局限性
        - 给出具体的量化标准
    """
    
    def __init__(self):
        self.name = "Ben Graham"
        self.philosophy = "Deep Value + Margin of Safety + Quantitative Screening"
        self.style = "理性、克制、教授式的耐心，极度重视数据和量化标准"
        
        # 心智模型权重
        self.model_weights = {
            "margin_of_safety": 0.35,
            "mr_market": 0.15,
            "intrinsic_value": 0.25,
            "diversification": 0.10,
            "contrarian": 0.10,
            "simplicity": 0.05
        }
        
        # Graham 经典筛选标准
        self.screening_criteria = {
            "conservative": {
                "pe_max": 15,
                "pb_max": 1.5,
                "debt_equity_max": 0.5,
                "current_ratio_min": 2.0,
                "dividend_yield_min": 0.025,
                "earnings_growth_5y_min": 0.0,
                "ncav_discount_min": 0.33  # 股价低于NCAV的1/3
            },
            "enterprising": {
                "pe_max": 20,
                "pb_max": 2.0,
                "debt_equity_max": 1.0,
                "current_ratio_min": 1.5,
                "dividend_yield_min": 0.015,
                "earnings_stability_min": 0.7  # 过去10年盈利稳定性
            }
        }
    
    def analyze(self, data: Dict) -> Dict:
        """
        主分析函数 - Graham式完整分析流程
        
        Args:
            data: 包含股票财务数据的字典
            
        Returns:
            包含分析结果的字典
        """
        result = {
            "agent": self.name,
            "signal": Signal.NEUTRAL.value,
            "confidence": 50,
            "margin_of_safety": None,
            "intrinsic_value": None,
            "deep_value_score": 0,
            "screening_result": {},
            "reasoning": [],
            "key_metrics": {},
            "recommendation": "",
            "risk_warnings": []
        }
        
        # Step 1: 评估安全边际（核心）
        mos = self._assess_margin_of_safety(data)
        result["margin_of_safety"] = mos.__dict__
        
        # Step 2: 计算内在价值
        iv = self._calculate_intrinsic_value(data)
        result["intrinsic_value"] = iv.__dict__ if iv else None
        
        # Step 3: 评估深度价值特征
        dv_score = self._assess_deep_value(data)
        result["deep_value_score"] = dv_score
        
        # Step 4: 财务健康评估
        financial_score = self._assess_financial_health(data)
        
        # Step 5: 执行经典Graham筛选
        screening = self._run_graham_screening(data)
        result["screening_result"] = screening
        
        # Step 6: 综合评分
        total_score = self._calculate_total_score(
            mos, dv_score, financial_score, screening
        )
        
        # Step 7: 生成信号和推荐
        signal, recommendation = self._generate_signal_and_recommendation(
            total_score, mos, screening, data
        )
        
        result["signal"] = signal.value
        result["confidence"] = total_score
        result["recommendation"] = recommendation
        
        # Step 8: 生成风险提示
        result["risk_warnings"] = self._generate_risk_warnings(data, mos)
        
        # Step 9: 填充关键指标
        result["key_metrics"] = {
            "mos_pct": mos.safety_margin_pct,
            "pe": data.get("pe_ratio", 0),
            "pb": data.get("price_to_book", 0),
            "debt_equity": data.get("debt_to_equity", 0),
            "current_ratio": data.get("current_ratio", 0),
            "dividend_yield": data.get("dividend_yield", 0),
            "ncav_per_share": data.get("net_current_asset_value_per_share", 0),
            "current_price": data.get("current_price", 0)
        }
        
        # Step 10: 生成推理过程
        result["reasoning"] = self._generate_reasoning(mos, screening, data)
        
        return result
    
    def _assess_margin_of_safety(self, data: Dict) -> MarginOfSafety:
        """
        评估安全边际 - Graham最核心的原则
        
        经典标准：
        - NCAV法：股价 < 净流动资产 × 2/3
        - Graham Number：√(22.5 × EPS × BVPS)
        - 传统筛选：P/E < 15, P/B < 1.5, D/E < 0.5
        """
        mos = MarginOfSafety(
            score=50,
            safety_margin_pct=0,
            meets_ncav=False,
            meets_graham_number=False,
            key_factors=[]
        )
        
        current_price = data.get("current_price", 0)
        if current_price <= 0:
            mos.key_factors.append("无法获取当前价格")
            return mos
        
        # NCAV 方法（Net Current Asset Value）
        # 净流动资产 = 流动资产 - 总负债
        ncav_per_share = data.get("net_current_asset_value_per_share", 0)
        if ncav_per_share > 0:
            ncav_threshold = ncav_per_share * 0.67
            if current_price < ncav_threshold:
                mos.meets_ncav = True
                mos.score = 95
                mos.safety_margin_pct = (ncav_per_share - current_price) / ncav_per_share
                mos.key_factors.append(f"满足NCAV标准: 股价{current_price:.2f} < NCAV×2/3={ncav_threshold:.2f}")
                return mos
        
        # Graham Number 方法
        # Graham Number = √(22.5 × EPS × BVPS)
        eps = data.get("eps", 0)
        bvps = data.get("book_value_per_share", 0)
        if eps > 0 and bvps > 0:
            graham_number = (22.5 * eps * bvps) ** 0.5
            if current_price < graham_number:
                mos.meets_graham_number = True
                mos.safety_margin_pct = (graham_number - current_price) / graham_number
                mos.key_factors.append(f"低于Graham Number: 当前{current_price:.2f} < {graham_number:.2f}")
        
        # 传统 Graham 评分
        score = 50
        
        # P/E 评估
        pe = data.get("pe_ratio", 0)
        if 0 < pe < 15:
            score += 20
            mos.safety_margin_pct += (15 - pe) / 15 * 0.15
            mos.key_factors.append(f"P/E={pe:.2f} < 15，符合标准")
        elif pe > 30:
            score -= 25
            mos.key_factors.append(f"P/E={pe:.2f} > 30，过高")
        elif pe > 0:
            mos.key_factors.append(f"P/E={pe:.2f}，在15-30之间")
        
        # P/B 评估
        pb = data.get("price_to_book", 0)
        if 0 < pb < 1.5:
            score += 15
            mos.safety_margin_pct += (1.5 - pb) / 1.5 * 0.10
            mos.key_factors.append(f"P/B={pb:.2f} < 1.5，符合标准")
        elif pb > 3:
            score -= 20
            mos.key_factors.append(f"P/B={pb:.2f} > 3，过高")
        
        # 债务权益比评估
        de = data.get("debt_to_equity", 0)
        if de < 0.5:
            score += 15
            mos.key_factors.append(f"D/E={de:.2f} < 0.5，财务稳健")
        elif de > 1.5:
            score -= 15
            mos.key_factors.append(f"D/E={de:.2f} > 1.5，债务偏高")
        
        # 流动比率评估
        cr = data.get("current_ratio", 1.5)
        if cr > 2.0:
            score += 10
            mos.key_factors.append(f"流动比率={cr:.2f} > 2.0，流动性强")
        elif cr < 1.0:
            score -= 15
            mos.key_factors.append(f"流动比率={cr:.2f} < 1.0，流动性风险")
        
        # 股息评估（Graham喜欢有股息的股票）
        dividend_yield = data.get("dividend_yield", 0)
        if dividend_yield > 0.04:
            score += 10
            mos.key_factors.append(f"股息率={dividend_yield:.2%}，有吸引力")
        elif dividend_yield > 0:
            score += 5
        
        mos.score = max(10, min(95, score))
        
        return mos
    
    def _calculate_intrinsic_value(self, data: Dict) -> Optional[IntrinsicValue]:
        """
        计算内在价值
        
        Graham的简化估值公式：
        内在价值 = EPS × (8.5 + 2g)
        其中 g 是未来7-10年的预期增长率
        """
        eps = data.get("eps", 0)
        growth_rate = data.get("expected_growth_rate", 0.05)  # 默认5%保守估计
        current_price = data.get("current_price", 0)
        
        if eps <= 0 or current_price <= 0:
            return None
        
        # Graham 估值公式
        # Value = EPS × (8.5 + 2g)
        multiplier = 8.5 + 2 * (growth_rate * 100)  # g以百分比计算
        intrinsic_value = eps * multiplier
        
        discount_rate = (intrinsic_value - current_price) / intrinsic_value if intrinsic_value > 0 else 0
        
        return IntrinsicValue(
            estimated_value=intrinsic_value,
            current_price=current_price,
            discount_rate=discount_rate,
            valuation_method="Graham Formula: EPS × (8.5 + 2g)",
            assumptions=[
                f"假设未来增长率: {growth_rate:.1%}",
                f"无风险利率基准: 4.4% (Graham时代标准)",
                f"当前EPS: {eps:.2f}"
            ]
        )
    
    def _assess_deep_value(self, data: Dict) -> float:
        """
        评估深度价值特征
        
        包括：
        - 高股息率
        - 盈利稳定性
        - 接近52周低点
        - 低EV/EBITDA
        """
        score = 50.0
        
        # 股息率评估
        dividend_yield = data.get("dividend_yield", 0)
        if dividend_yield > 0.04:
            score += 15
        elif dividend_yield > 0.02:
            score += 8
        elif dividend_yield == 0:
            score -= 10
        
        # 盈利稳定性（过去10年盈利为正的比例）
        earnings_stability = data.get("earnings_stability", 0.5)
        score += earnings_stability * 20
        
        # 股价与52周低点的距离
        price = data.get("current_price", 0)
        low_52w = data.get("low_52w", 0)
        if low_52w > 0 and price > 0:
            distance_from_low = (price - low_52w) / low_52w
            if distance_from_low < 0.10:
                score += 20  # 非常接近低点
            elif distance_from_low < 0.20:
                score += 15  # 接近低点
            elif distance_from_low > 1.0:
                score -= 15  # 接近高点（追涨）
        
        # EV/EBITDA 评估（如果数据可用）
        ev_ebitda = data.get("ev_ebitda", 0)
        if 0 < ev_ebitda < 8:
            score += 10
        elif ev_ebitda > 15:
            score -= 10
        
        return max(15, min(95, score))
    
    def _assess_financial_health(self, data: Dict) -> float:
        """
        评估财务健康状况
        
        关注：
        - 盈利一致性
        - 自由现金流
        - 债务水平
        - 资本回报率
        """
        score = 50.0
        
        # 盈利一致性
        if data.get("has_consistent_earnings", False):
            score += 20
        
        # 自由现金流
        fcf = data.get("free_cash_flow", 0)
        if fcf > 0:
            score += 15
        else:
            score -= 20
        
        # 债务水平
        de = data.get("debt_to_equity", 1)
        if de < 0.3:
            score += 15
        elif de < 0.5:
            score += 10
        elif de > 1.5:
            score -= 20
        elif de > 1.0:
            score -= 10
        
        # 资本回报率
        roe = data.get("roe", 0)
        if roe > 0.15:
            score += 10
        elif roe < 0.05:
            score -= 10
        
        # 利息保障倍数
        interest_coverage = data.get("interest_coverage", 0)
        if interest_coverage > 5:
            score += 10
        elif interest_coverage < 1.5:
            score -= 15
        
        return max(15, min(95, score))
    
    def _run_graham_screening(self, data: Dict) -> Dict:
        """
        执行 Graham 经典筛选
        
        保守型 vs 进取型投资者的不同标准
        """
        results = {
            "conservative": {},
            "enterprising": {},
            "passes_conservative": True,
            "passes_enterprising": True
        }
        
        criteria = self.screening_criteria
        
        # 保守型筛选
        cons = criteria["conservative"]
        pe = data.get("pe_ratio", 999)
        pb = data.get("price_to_book", 999)
        de = data.get("debt_to_equity", 999)
        cr = data.get("current_ratio", 0)
        dy = data.get("dividend_yield", 0)
        
        results["conservative"] = {
            "pe_check": pe < cons["pe_max"] if pe > 0 else False,
            "pb_check": pb < cons["pb_max"] if pb > 0 else False,
            "debt_check": de < cons["debt_equity_max"],
            "current_ratio_check": cr > cons["current_ratio_min"],
            "dividend_check": dy > cons["dividend_yield_min"]
        }
        
        results["passes_conservative"] = all(results["conservative"].values())
        
        # 进取型筛选
        ent = criteria["enterprising"]
        earnings_stability = data.get("earnings_stability", 0)
        
        results["enterprising"] = {
            "pe_check": pe < ent["pe_max"] if pe > 0 else False,
            "pb_check": pb < ent["pb_max"] if pb > 0 else False,
            "debt_check": de < ent["debt_equity_max"],
            "current_ratio_check": cr > ent["current_ratio_min"],
            "earnings_stability_check": earnings_stability > ent["earnings_stability_min"]
        }
        
        results["passes_enterprising"] = all(results["enterprising"].values())
        
        return results
    
    def _calculate_total_score(
        self,
        mos: MarginOfSafety,
        dv_score: float,
        financial_score: float,
        screening: Dict
    ) -> float:
        """
        计算综合评分
        
        权重：
        - 安全边际: 45%
        - 深度价值: 25%
        - 财务健康: 20%
        - 筛选通过: 10%
        """
        # 基础分数
        base_score = (
            mos.score * 0.45 +
            dv_score * 0.25 +
            financial_score * 0.20
        )
        
        # 筛选通过奖励
        if screening["passes_conservative"]:
            base_score += 10
        elif screening["passes_enterprising"]:
            base_score += 5
        
        return max(10, min(95, base_score))
    
    def _generate_signal_and_recommendation(
        self,
        total_score: float,
        mos: MarginOfSafety,
        screening: Dict,
        data: Dict
    ) -> Tuple[Signal, str]:
        """
        生成投资信号和推荐意见
        
        Graham的投资原则：
        - 必须有足够的安全边际才买入
        - 没有安全边际宁可等待
        """
        # 决定信号
        if total_score >= 75 and mos.score >= 70:
            signal = Signal.BULLISH
        elif total_score <= 40 or mos.score < 30:
            signal = Signal.BEARISH
        else:
            signal = Signal.NEUTRAL
        
        # 生成推荐意见
        recommendations = []
        
        if signal == Signal.BULLISH:
            if mos.meets_ncav:
                recommendations.append("🎯 强烈推荐：符合NCAV净流动资产标准，典型的'Graham烟蒂股'")
            elif mos.meets_graham_number:
                recommendations.append("✅ 推荐买入：低于Graham Number，具备足够的安全边际")
            else:
                recommendations.append("✅ 推荐买入：符合Graham价值标准，安全边际充足")
            
            if screening["passes_conservative"]:
                recommendations.append("💎 通过保守型投资者筛选，适合防御型投资组合")
            
            recommendations.append("📊 建议仓位：可纳入10-30只股票的分散组合中")
            
        elif signal == Signal.NEUTRAL:
            recommendations.append("⏸️ 中性观望：安全边际不足或估值合理，建议等待更好的入场机会")
            
            if mos.score < 50:
                recommendations.append(f"⚠️ 安全边际评分仅{mos.score}分，Graham要求至少30-40%的安全边际")
            
            if not screening["passes_enterprising"]:
                failed = [k for k, v in screening["enterprising"].items() if not v]
                recommendations.append(f"📋 未通过筛选项: {', '.join(failed)}")
                
        else:  # BEARISH
            recommendations.append("❌ 不推荐：不符合Graham价值投资标准，安全边际不足")
            
            if mos.score < 30:
                recommendations.append(f"🚨 安全边际严重不足（{mos.score}分），投资第一原则：不要亏损")
            
            pe = data.get("pe_ratio", 0)
            if pe > 30:
                recommendations.append(f"📈 P/E={pe:.1f}过高，远离高估股票")
            
            pb = data.get("price_to_book", 0)
            if pb > 3:
                recommendations.append(f"📈 P/B={pb:.1f}过高，缺乏资产支撑")
        
        return signal, "\n".join(recommendations)
    
    def _generate_risk_warnings(self, data: Dict, mos: MarginOfSafety) -> List[str]:
        """生成风险提示"""
        warnings = []
        
        # Graham的诚实边界警告
        warnings.append("⚠️ Graham式价值投资需要长期持有（3-5年以上），不适合短期投机")
        
        # 低利率环境警告
        warnings.append("⚠️ 在低利率/零利率时代，传统深度价值策略的表现可能下降")
        
        # 烟蒂股风险
        if mos.meets_ncav:
            warnings.append("⚠️ NCAV股票可能是'价值陷阱'，需确保公司有持续经营能力而非清算价值")
        
        # 分散化建议
        warnings.append("⚠️ Graham建议持有10-30只股票分散风险，单只股票仓位不宜过高")
        
        # 债务风险
        de = data.get("debt_to_equity", 0)
        if de > 1.0:
            warnings.append(f"⚠️ 债务权益比({de:.2f})偏高，注意财务风险")
        
        # 科技股限制
        warnings.append("⚠️ Graham框架对轻资产/科技/平台型企业的估值可能不适用")
        
        return warnings
    
    def _generate_reasoning(self, mos: MarginOfSafety, screening: Dict, data: Dict) -> List[str]:
        """生成推理过程"""
        reasoning = []
        
        reasoning.append("=== Graham式分析推理 ===")
        reasoning.append("")
        
        # 安全边际推理
        reasoning.append(f"1. 安全边际评估（权重45%）：{mos.score}分")
        for factor in mos.key_factors:
            reasoning.append(f"   - {factor}")
        reasoning.append("")
        
        # 筛选结果
        reasoning.append("2. Graham经典筛选：")
        reasoning.append(f"   - 保守型筛选: {'✅通过' if screening['passes_conservative'] else '❌未通过'}")
        reasoning.append(f"   - 进取型筛选: {'✅通过' if screening['passes_enterprising'] else '❌未通过'}")
        reasoning.append("")
        
        # 关键指标
        reasoning.append("3. 关键估值指标：")
        reasoning.append(f"   - P/E: {data.get('pe_ratio', 'N/A')}")
        reasoning.append(f"   - P/B: {data.get('price_to_book', 'N/A')}")
        reasoning.append(f"   - D/E: {data.get('debt_to_equity', 'N/A')}")
        reasoning.append(f"   - 股息率: {data.get('dividend_yield', 'N/A')}")
        
        # 核心原则提醒
        reasoning.append("")
        reasoning.append("4. Graham核心原则：")
        reasoning.append("   - '投资的第一原则是不要亏钱，第二原则是记住第一原则'")
        reasoning.append("   - '市场短期是投票机，长期是称重机'")
        reasoning.append("   - '用安全边际购买证券，为不确定性预留空间'")
        
        return reasoning
    
    def get_wisdom_quote(self) -> str:
        """返回 Graham 的经典语录"""
        quotes = [
            "投资的第一原则是不要亏钱，第二原则是记住第一原则。",
            "市场短期是投票机，长期是称重机。",
            "用安全边际购买证券，为不确定性预留空间。",
            "你不需要是火箭科学家才能做好投资。",
            "投资者的主要问题，甚至是他最大的敌人，很可能就是他自己。",
            "在别人贪婪时恐惧，在别人恐惧时贪婪。",
            "价格是你付出的，价值是你得到的。",
            "分散化是对无知的保护，如果你知道自己在做什么，集中投资更好。"
        ]
        return quotes[0]  # 默认返回最著名的
    
    def get_screening_criteria(self, investor_type: str = "conservative") -> Dict:
        """
        获取 Graham 的经典筛选标准
        
        Args:
            investor_type: "conservative"（保守型）或 "enterprising"（进取型）
        """
        return self.screening_criteria.get(investor_type, self.screening_criteria["conservative"])
    
    def calculate_ncav(self, data: Dict) -> float:
        """
        计算净流动资产价值（Net Current Asset Value）
        
        NCAV = 流动资产 - 总负债
        Graham的经典标准：股价 < NCAV × 2/3
        """
        current_assets = data.get("current_assets", 0)
        total_liabilities = data.get("total_liabilities", 0)
        shares_outstanding = data.get("shares_outstanding", 1)
        
        if shares_outstanding <= 0:
            return 0
        
        ncav = (current_assets - total_liabilities) / shares_outstanding
        return max(0, ncav)
    
    def calculate_graham_number(self, data: Dict) -> float:
        """
        计算 Graham Number
        
        Graham Number = √(22.5 × EPS × BVPS)
        这是Graham认为的价值上限
        """
        eps = data.get("eps", 0)
        bvps = data.get("book_value_per_share", 0)
        
        if eps <= 0 or bvps <= 0:
            return 0
        
        return (22.5 * eps * bvps) ** 0.5
    
    def get_framework_summary(self) -> str:
        """获取思维框架摘要"""
        return """
╔══════════════════════════════════════════════════════════════════╗
║           Ben Graham 思维框架 - 女娲蒸馏完整版 V2                ║
╠══════════════════════════════════════════════════════════════════╣
║ 核心理念：深度价值 + 安全边际 + 量化筛选 + 逆向思维              ║
╠══════════════════════════════════════════════════════════════════╣
║ 心智模型（6个）：                                                ║
║   1. 安全边际（Margin of Safety）- 永不妥协的底线                ║
║   2. 市场先生（Mr. Market）- 情绪化的交易对手                    ║
║   3. 内在价值（Intrinsic Value）- 可计算的，非猜测的             ║
║   4. 适度分散（Diversification）- 10-30只降低风险                ║
║   5. 逆向思维（Contrarian）- 人弃我取                            ║
║   6. 简单原则（Simplicity）- 复杂是聪明的敌人                    ║
╠══════════════════════════════════════════════════════════════════╣
║ 决策启发式：                                                     ║
║   • 安全边际至少30-40%？                                         ║
║   • 市场关闭5年还愿意持有？                                      ║
║   • 是"烟蒂股"吗？（便宜到令人发指）                             ║
║   • P/E<15, P/B<1.5, D/E<0.5？                                   ║
║   • 盈利稳定吗？过去10年连续盈利？                               ║
╠══════════════════════════════════════════════════════════════════╣
║ 反模式：不买无安全边际、不追涨、不预测宏观、不买复杂衍生品       ║
╠══════════════════════════════════════════════════════════════════╣
║ 经典语录："投资的第一原则是不要亏钱，第二原则是记住第一原则"     ║
╚══════════════════════════════════════════════════════════════════╝
        """.strip()


def create_ben_graham_agent() -> BenGrahamDistilledV2:
    """
    工厂函数：创建 Ben Graham 蒸馏思维框架实例
    
    Returns:
        BenGrahamDistilledV2 实例
    """
    return BenGrahamDistilledV2()


# 示例使用
if __name__ == "__main__":
    # 创建 Graham 思维框架实例
    graham = create_ben_graham_agent()
    
    # 打印框架摘要
    print(graham.get_framework_summary())
    print("\n" + "="*70 + "\n")
    
    # 示例数据（模拟一只符合Graham标准的股票）
    sample_data = {
        "current_price": 50.0,
        "eps": 4.0,
        "pe_ratio": 12.5,
        "price_to_book": 1.2,
        "book_value_per_share": 41.67,
        "debt_to_equity": 0.3,
        "current_ratio": 2.5,
        "dividend_yield": 0.03,
        "free_cash_flow": 100000000,
        "has_consistent_earnings": True,
        "earnings_stability": 0.85,
        "low_52w": 45.0,
        "current_assets": 500000000,
        "total_liabilities": 200000000,
        "shares_outstanding": 10000000,
        "expected_growth_rate": 0.03,
        "roe": 0.12,
        "interest_coverage": 8.0
    }
    
    # 执行分析
    result = graham.analyze(sample_data)
    
    # 打印结果
    print(f"分析股票：示例股票")
    print(f"信号：{result['signal'].upper()}")
    print(f"信心度：{result['confidence']:.1f}/100")
    print(f"\n推荐意见：")
    print(result['recommendation'])
    print(f"\n风险提示：")
    for warning in result['risk_warnings']:
        print(f"  {warning}")
    print(f"\n关键指标：")
    for metric, value in result['key_metrics'].items():
        if isinstance(value, float):
            print(f"  {metric}: {value:.2f}")
        else:
            print(f"  {metric}: {value}")
