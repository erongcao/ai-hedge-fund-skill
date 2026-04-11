#!/usr/bin/env python3
"""
Carl Icahn 思维框架蒸馏 - 女娲版

核心理念：激进维权 + 企业治理改造 + 释放隐藏价值

心智模型：
1. 股东维权主义（Activist Investing）- 大股东介入推动变革
2. 代理权之争（Proxy Fight）- 通过董事会席位改变公司决策
3. 分拆套利（Breakup Arbitrage）- 分拆被低估的子公司
4. 资本回报优先（Capital Return）- 逼迫管理层回购或分红
5. 现金堆叠识别（Cash Pile Recognition）- 发现资产负债表上的隐藏价值

决策启发式：
1. 找到"有问题"但有潜力的公司（管理差、有闲置资产）
2. 大比例持股才能有话语权
3. 威胁比实际行动更有效（谈判杠杆）
4. 不需要经营公司，只需要让管理层做正确的事
5. 卖出时机：价值实现或耐心耗尽

反模式（Icahn 绝对不会做的事）：
- 不会投资自己无法影响的公司
- 不会持有流动性差的股票
- 不会长期陪跑失败的管理层
- 不会在明显低估时还袖手旁观

诚实边界：
- 需要大资金才能成为维权股东
- 需要有耐心和心理承受能力（可能耗时数年）
- 公司可能长期不回应
- 争议性高，可能引发法律纠纷
"""

from typing import Dict, List

class CarlIcahnDistilled:
    """
    蒸馏后的 Carl Icahn 思维框架
    """
    
    def __init__(self):
        self.name = "Carl Icahn"
        self.philosophy = "Activist Investing + Corporate Governance + Unlock Hidden Value"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "reasoning": [],
            "activist_potential": "low",
            "value_unlock_estimate": 0,
            "catalysts": [],
            "red_flags": []
        }
        
        # 评估维权潜力
        activist_score = self._assess_activist_potential(data)
        result["activist_potential"] = activist_score
        
        # 隐藏价值评估
        hidden_value = self._assess_hidden_value(data)
        result["hidden_value"] = hidden_value
        
        # 催化剂
        catalysts = self._identify_catalysts(data)
        result["catalysts"] = catalysts
        
        # 公司治理评估
        governance_score = self._assess_governance(data)
        
        # 综合评分
        total_score = (
            activist_score * 0.40 +
            hidden_value * 0.30 +
            governance_score * 0.30
        )
        
        # 生成信号
        if total_score >= 70 and len(catalysts) > 0:
            result["signal"] = "bullish"
            result["confidence"] = min(90, total_score)
        elif total_score <= 35:
            result["signal"] = "bearish"
            result["confidence"] = max(20, total_score)
        else:
            result["signal"] = "neutral"
            result["confidence"] = total_score
        
        result["red_flags"] = self._identify_red_flags(data)
        
        return result
    
    def _assess_activist_potential(self, data: Dict) -> float:
        """评估公司被维权的可能性"""
        score = 30  # 默认低
        
        # 市值规模（太小的难以维权）
        market_cap = data.get("market_cap", 0)
        if market_cap > 5e9:
            score += 20
        elif market_cap > 1e9:
            score += 10
        
        # 股东结构（股权分散更容易）
        institutional_ownership = data.get("institutional_ownership", 0.8)
        if institutional_ownership < 0.70:
            score += 15
        elif institutional_ownership > 0.90:
            score -= 10  # 大机构持股难以撼动
        
        # 现金流状况（有现金才能回购/分红）
        if data.get("free_cash_flow", 0) > 0:
            score += 15
        
        # 董事会结构（独立董事少更容易推动变革）
        independent_board = data.get("independent_board_pct", 0.5)
        if independent_board < 0.60:
            score += 10
        
        # 管理层的career risk（任期长的更保守）
        if data.get("ceo_tenure_years", 10) > 15:
            score += 10  # 老管理层可能更容易被说服
        
        return max(10, min(90, score))
    
    def _assess_hidden_value(self, data: Dict) -> float:
        """评估隐藏价值"""
        score = 50
        
        # 净现金（cash - debt）
        net_cash = data.get("net_cash_per_share", 0)
        stock_price = data.get("current_price", 0)
        if stock_price > 0 and net_cash > 0:
            cash_ratio = net_cash / stock_price
            if cash_ratio > 0.30:
                score += 25  # 大量净现金
            elif cash_ratio > 0.15:
                score += 15
        
        # 低估值指标
        pb = data.get("price_to_book", 0)
        if pb > 0 and pb < 1.0:
            score += 20  # 股价低于账面价值
        
        ev_ebitda = data.get("ev_ebitda", 0)
        if ev_ebitda > 0 and ev_ebitda < 6:
            score += 15
        
        # 可出售资产
        if data.get("has_real_estate_assets", False):
            score += 10
        
        if data.get("has_subsidiaries", False):
            score += 10
        
        return max(15, min(95, score))
    
    def _identify_catalysts(self, data: Dict) -> List[str]:
        """识别价值释放催化剂"""
        catalysts = []
        
        if data.get("has_share_repurchase_authorized", False):
            catalysts.append("Authorized share buyback program")
        
        if data.get("has_dividend", False) and not data.get("dividend_growing", False):
            catalysts.append("Dividend could be increased or eliminated")
        
        if data.get("has_activist_持有", False):
            catalysts.append("Other activist already involved")
        
        if data.get("has_potential_spinoff", False):
            catalysts.append("Potential business unit spinoff")
        
        if data.get("management_change_possible", False):
            catalysts.append("Management change could unlock value")
        
        if data.get("has_debt_refinancing_opportunity", False):
            catalysts.append("Debt refinancing could reduce interest costs")
        
        return catalysts
    
    def _assess_governance(self, data: Dict) -> float:
        """评估公司治理质量"""
        score = 50
        
        insider_ownership = data.get("insider_ownership", 0)
        if insider_ownership < 0.03:
            score -= 15  # 管理层没有足够利益
        
        if data.get("has_poison_pill", False):
            score -= 20  # 毒丸防御
        
        if data.get("has_staggered_board", False):
            score -= 10  # 交错董事会更难替换
        
        if data.get("dual_class_shares", False):
            score -= 15  # 双层股权结构
        
        # 检查过往资本配置
        if data.get("has_history_of_poor_capital_allocation", False):
            score -= 20
        
        return max(10, min(85, score))
    
    def _identify_red_flags(self, data: Dict) -> List[str]:
        """识别风险"""
        flags = []
        
        if data.get("has_poison_pill", False):
            flags.append("Poison pill defense in place")
        
        if data.get("dual_class_shares", False):
            flags.append("Dual class share structure limits shareholder power")
        
        if data.get("has_leveraged_buyout_history", False):
            flags.append("Previous LBO left heavy debt burden")
        
        if data.get("industry_disruption_high", False):
            flags.append("Industry facing structural disruption")
        
        return flags


def create_icahn_agent() -> CarlIcahnDistilled:
    return CarlIcahnDistilled()
