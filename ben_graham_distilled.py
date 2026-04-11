#!/usr/bin/env python3
"""
Ben Graham 思维框架蒸馏 - 女娲版

核心理念：深度价值 + 安全边际 + 量化筛选

心智模型：
1. 安全边际（Margin of Safety）- 永远是核心
2. 内在价值（Intrinsic Value）- 用数据计算，不是猜
3. 适度分散（Moderate Diversification）- 10-30个证券
4. 简单原则（Simple Rules）- 不需要复杂模型
5. 逆向思维（Contrarian）- 人弃我取

核心原则：
1. "投资的第一原则是不要亏钱"
2. "第二原则是记住第一原则"
3. "用安全边际购买证券"
4. "市场是投票机，不是称重机"
5. "短期是情绪的，长期是基本面的"

决策启发式：
1. 这笔投资有足够的安全边际吗？（至少30-40%）
2. 这家公司盈利稳定吗？
3. 管理层有诚信吗？
4. 这是一个"烟蒂"吗？（便宜到令人发指）
5. 如果市场关闭5年，我还愿意持有吗？

反模式（Graham 绝对不会做的事）：
- 不会买没有安全边际的股票
- 不会买亏损的公司（除非极度便宜）
- 不会追涨
- 不会依赖预测
- 不会买复杂的衍生品

诚实边界：
- 深度价值需要耐心等待
- "烟蒂"可能真的是垃圾
- 需要足够的资金分散
- 在低利率时代策略表现下降
"""

from typing import Dict, List

class BenGrahamDistilled:
    """
    蒸馏后的 Ben Graham 思维框架（现代版）
    """
    
    def __init__(self):
        self.name = "Ben Graham"
        self.philosophy = "Deep Value + Margin of Safety + Quantitative Screening"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "margin_of_safety": "insufficient",
            "deep_value_score": 0,
            "reasoning": [],
            "key_metrics": {}
        }
        
        # 评估安全边际
        mos = self._assess_margin_of_safety(data)
        result["margin_of_safety"] = mos
        
        # 评估深度价值特征
        dv_score = self._assess_deep_value(data)
        result["deep_value_score"] = dv_score
        
        # 财务健康
        financial_score = self._assess_financial_health(data)
        
        # 综合评分
        total_score = (
            mos["score"] * 0.45 +
            dv_score * 0.35 +
            financial_score * 0.20
        )
        
        if total_score >= 75:
            result["signal"] = "bullish"
        elif total_score <= 40:
            result["signal"] = "bearish"
        else:
            result["signal"] = "neutral"
        
        result["confidence"] = total_score
        result["key_metrics"] = {
            "mos_pct": mos["safety_margin"],
            "pe": data.get("pe_ratio", 0),
            "pb": data.get("price_to_book", 0),
            "debt_equity": data.get("debt_to_equity", 0),
            "current_ratio": data.get("current_ratio", 0)
        }
        
        return result
    
    def _assess_margin_of_safety(self, data: Dict) -> Dict:
        """
        评估安全边际
        Graham 的经典标准：
        - P/E < 15
        - P/B < 1.5
        - D/E < 0.5
        """
        mos = {"score": 0, "safety_margin": 0}
        
        # NCAV (Net Current Asset Value) 方法
        # 股价 < 净流动资产 的 2/3
        ncav_per_share = data.get("net_current_asset_value_per_share", 0)
        current_price = data.get("current_price", 0)
        if ncav_per_share > 0 and current_price > 0:
            if current_price < ncav_per_share * 0.67:
                mos["score"] = 95
                mos["safety_margin"] = (ncav_per_share - current_price) / ncav_per_share
                return mos
        
        # 传统 Graham 筛选
        score = 50
        mos_pct = 0
        
        # P/E
        pe = data.get("pe_ratio", 0)
        if 0 < pe < 15:
            score += 20
            mos_pct += (15 - pe) / 15 * 15
        elif pe > 30:
            score -= 20
        
        # P/B
        pb = data.get("price_to_book", 0)
        if 0 < pb < 1.5:
            score += 15
            mos_pct += (1.5 - pb) / 1.5 * 10
        elif pb > 3:
            score -= 15
        
        # D/E
        de = data.get("debt_to_equity", 0)
        if de < 0.5:
            score += 15
        elif de > 1.5:
            score -= 15
        
        # 流动比率
        cr = data.get("current_ratio", 1.5)
        if cr > 2.0:
            score += 10
        elif cr < 1.0:
            score -= 15
        
        mos["score"] = max(10, min(95, score))
        mos["safety_margin"] = mos_pct / 100 if mos_pct > 0 else 0
        
        return mos
    
    def _assess_deep_value(self, data: Dict) -> float:
        """评估深度价值特征"""
        score = 50
        
        # 股息率（高股息 = 价值特征）
        dividend_yield = data.get("dividend_yield", 0)
        if dividend_yield > 0.04:
            score += 15
        elif dividend_yield > 0.02:
            score += 8
        
        # 盈利稳定性
        earnings_stability = data.get("earnings_stability", 0.5)
        score += int(earnings_stability * 20)
        
        # 股价/52周低点
        price = data.get("current_price", 0)
        low_52w = data.get("low_52w", 0)
        if low_52w > 0 and price > 0:
            distance_from_low = (price - low_52w) / low_52w
            if distance_from_low < 0.20:
                score += 15  # 接近低点
            elif distance_from_low > 1.0:
                score -= 10  # 接近高点
        
        return max(15, min(95, score))
    
    def _assess_financial_health(self, data: Dict) -> float:
        """评估财务健康"""
        score = 50
        
        # 盈利稳定性
        if data.get("has_consistent_earnings", False):
            score += 20
        
        # 现金流
        if data.get("free_cash_flow", 0) > 0:
            score += 15
        else:
            score -= 20
        
        # 债务
        if data.get("debt_to_equity", 1) < 0.5:
            score += 15
        elif data.get("debt_to_equity", 1) > 1.5:
            score -= 20
        
        return max(15, min(95, score))
    
    def get_graham_screening_criteria(self) -> Dict:
        """
        Graham 的经典筛选标准
        """
        return {
            "conservative": {
                "pe_max": 15,
                "pb_max": 1.5,
                "debt_equity_max": 0.5,
                "current_ratio_min": 2.0,
                "dividend_yield_min": 0.025,
                "earnings_growth_5y_min": 0.0
            },
            "moderate": {
                "pe_max": 20,
                "pb_max": 2.0,
                "debt_equity_max": 1.0,
                "current_ratio_min": 1.5,
                "dividend_yield_min": 0.02,
                "earnings_growth_5y_min": -0.05
            }
        }


def create_ben_graham_agent() -> BenGrahamDistilled:
    return BenGrahamDistilled()
