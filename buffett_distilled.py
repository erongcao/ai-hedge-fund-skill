#!/usr/bin/env python3
"""
Warren Buffett 思维框架蒸馏 - 女娲版

核心理念：用 Buffett 的心智模型思考，而不是复制 Buffett 说过的话。

心智模型：
1. 能力圈（Circle of Competence）- 只买自己能理解的东西
2. 护城河（Economic Moat）- 持久的竞争优势让竞争对手难以模仿
3. 安全边际（Margin of Safety）- 用合理价格买优秀公司，而非便宜价买普通公司
4. 逆向思维（Inversion）- 先想怎么亏钱，然后避免之
5. 时间复利（Time in Market）- 喜欢"永远"持有

决策启发式：
1. 优秀公司 + 合理价格 >> 普通公司 + 便宜价格
2. ROE > 15% 是好公司的底线
3. 低债务 + 高现金流 = 财务健康
4. 管理层必须是诚信且有能力的人
5. 用"如果这个股票明天退市我是否还愿意持有"来检验

反模式（Buffett 绝对不会做的事）：
- 不会买自己看不懂的业务
- 不会为成长付过高的溢价
- 不会频繁交易
- 不会追随短期市场情绪
- 不会投资没有护城河的公司

诚实边界：
- 规模太大时，收益率会被稀释
- 不擅长早期科技股（后期才投苹果）
- 也会在市场恐慌时卖出（虽然少）
- 宏观预测不是他的强项
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class BuffettMetrics:
    """Buffett 核心检查清单"""
    # 业务质量
    has_economic_moat: bool = False
    moat_sources: List[str] = None  # 品牌、网络效应、成本优势等
    roe: float = 0.0
    roic: float = 0.0  # 投资资本回报率
    
    # 财务健康
    debt_level: str = "unknown"  # low/medium/high
    free_cash_flow: float = 0.0
    consistent_earnings: bool = False
    
    # 管理层
    management_quality: str = "unknown"  # excellent/good/average/poor
    ceo_integrity: bool = False
    
    # 估值
    intrinsic_value_estimate: float = 0.0
    margin_of_safety: float = 0.0  # 当前价格vs内在价值的折扣
    
    # 能力圈
    within_circle_of_competence: bool = False
    business_understandable: bool = False


class WarrenBuffettDistilled:
    """
    蒸馏后的 Buffett 思维框架
    
    HOW he thinks, not WHAT he says.
    """
    
    def __init__(self):
        self.name = "Warren Buffett"
        self.philosophy = "Wonderful companies at fair prices"
        
    def analyze(self, data: Dict) -> Dict:
        """
        使用 Buffett 的心智模型分析股票
        """
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "reasoning": [],
            "key_insights": [],
            "red_flags": [],
            "checklist": {}
        }
        
        # 执行 Buffett 的核心检查清单
        checklist = self._buffett_checklist(data)
        
        # 1. 护城河检查（最重要）
        moat_score = self._evaluate_moat(data, checklist)
        
        # 2. ROE/ROIC 检查
        profitability_score = self._evaluate_profitability(data, checklist)
        
        # 3. 财务健康检查
        financial_score = self._evaluate_financial_health(data, checklist)
        
        # 4. 管理层检查
        management_score = self._evaluate_management(data, checklist)
        
        # 5. 估值检查（安全边际）
        valuation_score = self._evaluate_valuation(data, checklist)
        
        # 综合评分
        total_score = (
            moat_score * 0.30 +      # 护城河最重要
            profitability_score * 0.25 +
            financial_score * 0.20 +
            management_score * 0.10 +
            valuation_score * 0.15
        )
        
        # 生成信号
        if total_score >= 70 and checklist["within_circle_of_competence"]:
            result["signal"] = "bullish"
            result["confidence"] = min(90, total_score + 10)
        elif total_score <= 40:
            result["signal"] = "bearish"
            result["confidence"] = max(20, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        # 填充 reasoning
        result["reasoning"] = self._generate_reasoning(checklist, moat_score, profitability_score)
        result["checklist"] = checklist
        
        # 核心洞察
        result["key_insights"] = self._generate_key_insights(checklist)
        result["red_flags"] = self._identify_red_flags(checklist)
        
        return result
    
    def _buffett_checklist(self, data: Dict) -> Dict:
        """
        Buffett 的投资检查清单
        """
        checklist = {
            # 护城河指标
            "has_moat": False,
            "moat_sources": [],
            "moat_durable": False,
            
            # 盈利指标
            "roe": data.get("roe", 0),
            "roic": data.get("roic", 0),
            "has_consistent_earnings": False,
            
            # 财务健康
            "debt_to_equity": data.get("debt_to_equity", 0),
            "free_cash_flow": data.get("free_cash_flow", 0),
            "operating_margin": data.get("operating_margin", 0),
            
            # 管理层
            "management_quality": "unknown",
            "insider_ownership": data.get("insider_ownership", 0),
            "share_repurchase_program": False,
            
            # 估值
            "pe_ratio": data.get("pe_ratio", 0),
            "price_to_book": data.get("price_to_book", 0),
            "peg_ratio": data.get("peg_ratio", 0),
            
            # 能力圈
            "within_circle_of_competence": True,  # 默认True除非能证明不可理解
            "business_understandable": True,
            "sector": data.get("sector", "unknown")
        }
        
        # 检查护城河来源
        checklist["moat_sources"] = self._identify_moat_sources(data)
        checklist["has_moat"] = len(checklist["moat_sources"]) > 0
        checklist["moat_durable"] = self._assess_moat_durability(data, checklist["moat_sources"])
        
        # 检查盈利一致性
        earnings_volatility = data.get("earnings_volatility", 1.0)
        checklist["has_consistent_earnings"] = earnings_volatility < 0.3  # 低波动 = 一致
        
        # 检查管理层质量
        if checklist["insider_ownership"] > 0.1:  # 管理层持股 > 10%
            checklist["management_quality"] = "excellent"
        elif checklist["insider_ownership"] > 0.03:
            checklist["management_quality"] = "good"
        elif data.get("return_on_assets", 0) > 0.1:
            checklist["management_quality"] = "good"
        else:
            checklist["management_quality"] = "average"
        
        # 能力圈判断
        understandable_sectors = [
            "Consumer Defensive", "Consumer Cyclical", "Financial Services",
            "Healthcare", "Industrials", "Energy", "Utilities"
        ]
        tech_sectors = ["Technology", "Communication Services"]
        
        if checklist["sector"] in understandable_sectors:
            checklist["within_circle_of_competence"] = True
            checklist["business_understandable"] = True
        elif checklist["sector"] in tech_sectors:
            # Buffett 后期才投科技股，且只投有护城河的平台型
            if checklist["has_moat"] and checklist["roe"] > 0.20:
                checklist["within_circle_of_competence"] = True
            else:
                checklist["within_circle_of_competence"] = False
        
        return checklist
    
    def _identify_moat_sources(self, data: Dict) -> List[str]:
        """识别护城河来源"""
        sources = []
        
        # 品牌护城河
        if data.get("brand_strength", 0) > 0.7 or data.get("gross_margin", 0) > 0.40:
            sources.append("Strong Brand")
        
        # 网络效应
        if data.get("has_network_effect", False):
            sources.append("Network Effect")
        
        # 低成本优势
        if data.get("cost_advantage", False):
            sources.append("Cost Advantage")
        
        # 转换成本
        if data.get("switching_cost", 0) > 0.5:
            sources.append("High Switching Cost")
        
        # 监管护城河
        if data.get("has_regulatory_advantage", False):
            sources.append("Regulatory Moat")
        
        # 超高毛利率
        if data.get("gross_margin", 0) > 0.50:
            sources.append("High Margins")
        
        return sources
    
    def _assess_moat_durability(self, data: Dict, sources: List[str]) -> bool:
        """评估护城河持久性"""
        if not sources:
            return False
        
        # 护城河持久性指标
        revenue_growth = data.get("revenue_growth", 0)
        market_share_trend = data.get("market_share_trend", 0)
        
        # 如果护城河来源多且收入稳定增长，说明持久
        return len(sources) >= 2 and abs(revenue_growth) < 0.5
    
    def _evaluate_moat(self, data: Dict, checklist: Dict) -> float:
        """评估护城河（占30%权重）"""
        score = 0
        
        if checklist["has_moat"]:
            score += 40
            
            # 护城河来源越多越好
            if len(checklist["moat_sources"]) >= 3:
                score += 20
            elif len(checklist["moat_sources"]) >= 2:
                score += 10
            
            # 护城河持久
            if checklist["moat_durable"]:
                score += 15
        else:
            # 没有护城河是严重负面信号
            score = 10
        
        return min(75, score)
    
    def _evaluate_profitability(self, data: Dict, checklist: Dict) -> float:
        """评估盈利能力（占25%权重）"""
        score = 0
        
        # ROE 检查（Buffett 最看重）
        roe = checklist["roe"]
        if roe > 0.20:
            score += 40
        elif roe > 0.15:
            score += 30
        elif roe > 0.12:
            score += 20
        elif roe > 0.10:
            score += 10
        else:
            score = 5  # ROE 低于10%是严重问题
        
        # ROIC 检查
        roic = checklist["roic"]
        if roic > 0.15:
            score += 15
        elif roic > 0.10:
            score += 10
        
        # 盈利一致性
        if checklist["has_consistent_earnings"]:
            score += 10
        
        # 自由现金流
        fcf = checklist["free_cash_flow"]
        if fcf > 0:
            score += 10
        else:
            score -= 10  # 负现金流是严重问题
        
        return max(0, min(75, score))
    
    def _evaluate_financial_health(self, data: Dict, checklist: Dict) -> float:
        """评估财务健康（占20%权重）"""
        score = 50
        
        # 债务水平
        de = checklist["debt_to_equity"]
        if de < 0.5:
            score += 20
        elif de < 1.0:
            score += 10
        elif de < 2.0:
            score -= 5
        else:
            score -= 20  # 高杠杆是危险信号
        
        # 营业利润率
        margin = checklist["operating_margin"]
        if margin > 0.20:
            score += 15
        elif margin > 0.15:
            score += 10
        elif margin > 0.10:
            score += 5
        elif margin > 0:
            score -= 5
        else:
            score -= 15
        
        return max(0, min(80, score))
    
    def _evaluate_management(self, data: Dict, checklist: Dict) -> float:
        """评估管理层（占10%权重）"""
        score = 50
        
        quality = checklist["management_quality"]
        if quality == "excellent":
            score = 90
        elif quality == "good":
            score = 70
        elif quality == "average":
            score = 50
        else:
            score = 30
        
        # 管理层持股是正面信号
        if checklist["insider_ownership"] > 0.05:
            score += 10
        
        return max(20, min(95, score))
    
    def _evaluate_valuation(self, data: Dict, checklist: Dict) -> float:
        """
        评估估值（占15%权重）
        
        Buffett 的估值原则：
        - 用合理价格买优秀公司，不是用便宜价格买普通公司
        - P/E 本身不重要，重要的是 earnings power
        - 安全边际不是找到最低价，而是确保不会亏大钱
        """
        score = 50
        
        pe = checklist["pe_ratio"]
        if pe == 0:
            return 50  # 无法评估
        
        # 不同行业的合理 P/E 不同
        sector = checklist["sector"]
        
        # 稳定行业合理 P/E 更高
        if sector in ["Utilities", "Consumer Defensive"]:
            if pe < 20:
                score = 80
            elif pe < 25:
                score = 70
            elif pe < 30:
                score = 60
            else:
                score = 40
        # 成长行业要看 PEG
        else:
            peg = checklist["peg_ratio"]
            if 0 < peg < 1:
                score = 80
            elif peg < 1.5:
                score = 65
            elif peg < 2:
                score = 50
            else:
                score = 30
            
            # P/B 辅助判断
            pb = checklist["price_to_book"]
            if pb > 0:
                if pb < 3:
                    score += 10
                elif pb > 10:
                    score -= 15
        
        # 核心洞察：Buffett 更看重 earnings power 而非绝对 P/E
        # 如果公司能持续产生高回报，P/E 高一些也值得
        roe = checklist["roe"]
        if roe > 0.20 and score < 70:
            score += 10  # 高 ROE 公司值得溢价
        
        return max(15, min(85, score))
    
    def _generate_reasoning(self, checklist: Dict, moat_score: float, 
                           profitability_score: float) -> List[str]:
        """生成 Buffett 风格的 reasoning"""
        reasoning = []
        
        # 护城河
        if checklist["has_moat"]:
            moat_str = ", ".join(checklist["moat_sources"][:3])
            reasoning.append(f"Moat: {moat_str}")
        else:
            reasoning.append("No discernible competitive moat")
        
        # 盈利能力
        roe = checklist["roe"]
        if roe > 0:
            reasoning.append(f"ROE: {roe:.1%}")
        
        # 财务健康
        de = checklist["debt_to_equity"]
        if de > 0:
            debt_desc = "Low" if de < 0.5 else "Moderate" if de < 1.5 else "High"
            reasoning.append(f"Debt: {debt_desc} ({de:.2f}x)")
        
        # 能力圈
        if not checklist["within_circle_of_competence"]:
            reasoning.append(f"Outside circle of competence ({checklist['sector']})")
        
        return reasoning
    
    def _generate_key_insights(self, checklist: Dict) -> List[str]:
        """生成核心洞察"""
        insights = []
        
        # 护城河洞察
        if checklist["has_moat"] and checklist["moat_durable"]:
            insights.append("Durable competitive advantage identified")
        elif checklist["has_moat"]:
            insights.append("Has competitive moat but durability uncertain")
        
        # 盈利洞察
        if checklist["roe"] > 0.20:
            insights.append("Exceptional capital efficiency (ROE > 20%)")
        elif checklist["roe"] < 0.10:
            insights.append("Below-average returns on equity")
        
        # 管理层洞察
        if checklist["management_quality"] == "excellent":
            insights.append("Management with significant skin in the game")
        
        return insights
    
    def _identify_red_flags(self, checklist: Dict) -> List[str]:
        """识别危险信号"""
        flags = []
        
        if not checklist["has_moat"]:
            flags.append("No competitive moat - vulnerable to competition")
        
        if checklist["debt_to_equity"] > 2.0:
            flags.append("Excessive leverage")
        
        if checklist["free_cash_flow"] < 0:
            flags.append("Negative free cash flow")
        
        if checklist["roe"] < 0.10 and checklist["roe"] > 0:
            flags.append("Low ROE questions business quality")
        
        if not checklist["within_circle_of_competence"]:
            flags.append("Business outside Buffett's circle of competence")
        
        return flags


# 导出供主程序使用
def create_buffett_agent() -> WarrenBuffettDistilled:
    return WarrenBuffettDistilled()


if __name__ == "__main__":
    # 测试
    test_data = {
        "roe": 0.25,
        "roic": 0.18,
        "debt_to_equity": 0.4,
        "free_cash_flow": 5e9,
        "operating_margin": 0.28,
        "gross_margin": 0.45,
        "pe_ratio": 22,
        "price_to_book": 4.5,
        "peg_ratio": 1.2,
        "sector": "Consumer Cyclical",
        "insider_ownership": 0.15,
        "earnings_volatility": 0.15,
        "revenue_growth": 0.08,
        "brand_strength": 0.8,
        "switching_cost": 0.6,
    }
    
    agent = WarrenBuffettDistilled()
    result = agent.analyze(test_data)
    
    print(f"Signal: {result['signal']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reasoning: {result['reasoning']}")
    print(f"Key Insights: {result['key_insights']}")
    print(f"Red Flags: {result['red_flags']}")
