#!/usr/bin/env python3
"""
Daniel Loeb 思维框架蒸馏 - 女娲版

核心理念：维权投资 + 激进沟通 + 变革推动

心智模型：
1. 股东维权（Shareholder Activism）- 用影响力推动变革
2. 激进沟通（Aggressive Communication）- 公开信是工具
3. 变革催化剂（Change Catalyst）- 公司需要外部压力
4. 价值发现（Value Discovery）- 市场经常忽视明显机会
5. 专注少数持仓（Concentrated Focus）- 不分散精力

决策启发式：
1. 目标公司有明显的价值破坏问题吗？
2. 管理层有能力解决问题吗？还是需要外部压力？
3. 持有多少股份才能有话语权？
4. 这个投资能在1-2年内实现价值吗？

反模式（Loeb 绝对不会做的事）：
- 不会对无法影响的公司下手
- 不会在明显问题没有解决方案时坚持
- 不会忽视市场共识（但会挑战它）
- 不会分散到没有意义的地步
"""

from typing import Dict, List

class DanielLoebDistilled:
    """
    蒸馏后的 Daniel Loeb (Third Point) 思维框架
    """
    
    def __init__(self):
        self.name = "Daniel Loeb"
        self.philosophy = "Activist Investing + Change Catalyst + Concentrated Bets"
    
    def analyze(self, data: Dict) -> Dict:
        result = {
            "agent": self.name,
            "signal": "neutral",
            "confidence": 50,
            "activist_potential": "low",
            "change_catalyst": "none",
            "reasoning": []
        }
        
        # 评估维权潜力
        activist = self._assess_activist_potential(data)
        result["activist_potential"] = activist
        
        # 评估变革催化剂
        catalyst = self._assess_catalyst(data)
        result["change_catalyst"] = catalyst
        
        # 评估价值
        value_score = self._assess_value(data)
        
        total_score = activist * 0.4 + catalyst * 0.35 + value_score * 0.25
        
        if total_score >= 70:
            result["signal"] = "bullish"
        elif total_score <= 40:
            result["signal"] = "bearish"
        else:
            result["signal"] = "neutral"
        
        result["confidence"] = total_score
        return result
    
    def _assess_activist_potential(self, data: Dict) -> float:
        score = 30
        if data.get("institutional_ownership", 0.8) < 0.7:
            score += 20
        if data.get("free_cash_flow", 0) > 0:
            score += 20
        if data.get("independent_board_pct", 0.5) < 0.6:
            score += 15
        return max(15, min(90, score))
    
    def _assess_catalyst(self, data: Dict) -> float:
        score = 30
        if data.get("has_management_change", False):
            score += 30
        if data.get("has_potential_spinoff", False):
            score += 25
        if data.get("has_share_repurchase", False):
            score += 15
        if data.get("has_activist_involvement", False):
            score += 20
        return max(15, min(95, score))
    
    def _assess_value(self, data: Dict) -> float:
        score = 50
        pb = data.get("price_to_book", 1.5)
        if pb < 1.0:
            score += 25
        elif pb > 3:
            score -= 15
        return max(15, min(90, score))


def create_loeb_agent() -> DanielLoebDistilled:
    return DanielLoebDistilled()
