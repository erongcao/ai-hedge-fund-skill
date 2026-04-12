#!/usr/bin/env python3
"""
自适应权重系统 - 根据市场环境动态调整大师权重

核心逻辑:
- 牛市: 增加成长股大师权重 (Wood, Druckenmiller)
- 熊市: 增加价值大师权重 (Buffett, Graham)
- 震荡市: 增加期货交易员权重 (Jones, Seykota)
- 高波动: 增加宏观对冲大师权重 (Dalio, Soros)
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import json


class MarketRegime(Enum):
    """市场状态"""
    BULL_GROWTH = "牛市-成长"      # 增长+通胀回落
    BULL_VALUE = "牛市-价值"       # 增长+温和通胀
    BEAR_DEFLATION = "熊市-通缩"   # 衰退+低通胀
    BEAR_INFLATION = "熊市-滞胀"   # 衰退+高通胀
    RANGE_VOLATILE = "震荡-高波动" # 震荡+高波动
    RANGE_CALM = "震荡-低波动"     # 震荡+低波动


@dataclass
class MarketIndicators:
    """市场指标"""
    # 趋势指标
    sp500_trend: str  # up/down/sideways
    nasdaq_trend: str
    
    # 波动率指标
    vix_level: float  # VIX指数
    
    # 宏观指标
    interest_rate_trend: str  # rising/falling/stable
    inflation_trend: str      # rising/falling/stable
    gdp_growth: str           # strong/moderate/weak/recession
    
    # 流动性指标
    liquidity: str  # abundant/normal/tight
    
    # 情绪指标
    sentiment: str  # greedy/neutral/fear/extreme_fear


class AdaptiveWeightSystem:
    """
    自适应权重系统
    
    使用示例:
        aws = AdaptiveWeightSystem()
        weights = aws.get_weights(MarketRegime.BULL_GROWTH)
        # Returns: {'wood': 0.25, 'druckenmiller': 0.20, ...}
    """
    
    # 基础权重配置
    BASE_WEIGHTS = {
        # 价值型
        "buffett": {"category": "value", "base_weight": 0.05},
        "graham": {"category": "value", "base_weight": 0.05},
        "pabrai": {"category": "value", "base_weight": 0.04},
        "einhorn": {"category": "value", "base_weight": 0.04},
        
        # 成长型
        "wood": {"category": "growth", "base_weight": 0.05},
        "cohen": {"category": "growth", "base_weight": 0.04},
        "griffin": {"category": "growth", "base_weight": 0.04},
        
        # 宏观型
        "dalio": {"category": "macro", "base_weight": 0.05},
        "soros": {"category": "macro", "base_weight": 0.05},
        "druckenmiller": {"category": "macro", "base_weight": 0.05},
        "jones": {"category": "macro", "base_weight": 0.04},
        "kovner": {"category": "macro", "base_weight": 0.03},
        
        # 期货/交易型
        "dennis": {"category": "futures", "base_weight": 0.04},
        "seykota": {"category": "futures", "base_weight": 0.04},
        "livermore": {"category": "futures", "base_weight": 0.03},
        "williams": {"category": "futures", "base_weight": 0.03},
        "rogers": {"category": "futures", "base_weight": 0.03},
        
        # 量化型
        "simons": {"category": "quant", "base_weight": 0.05},
        "yass": {"category": "quant", "base_weight": 0.04},
        
        # 维权型
        "ackman": {"category": "activist", "base_weight": 0.04},
        "icahn": {"category": "activist", "base_weight": 0.04},
        "loeb": {"category": "activist", "base_weight": 0.03},
    }
    
    # 市场环境权重乘数
    REGIME_MULTIPLIERS = {
        MarketRegime.BULL_GROWTH: {
            "growth": 2.0,    # 成长股大师权重翻倍
            "macro": 1.3,
            "quant": 1.2,
            "value": 0.5,     # 价值大师权重减半
            "futures": 0.7,
            "activist": 1.0,
        },
        MarketRegime.BULL_VALUE: {
            "value": 1.8,
            "growth": 1.2,
            "macro": 1.0,
            "quant": 1.0,
            "futures": 0.6,
            "activist": 1.2,
        },
        MarketRegime.BEAR_DEFLATION: {
            "value": 2.2,     # 价值大师在熊市通缩表现最好
            "macro": 1.5,
            "quant": 1.0,
            "growth": 0.2,    # 成长股在熊市受重创
            "futures": 0.8,
            "activist": 0.7,
        },
        MarketRegime.BEAR_INFLATION: {
            "macro": 2.0,     # 宏观大师在滞胀表现最好
            "futures": 1.5,
            "value": 1.2,
            "quant": 0.8,
            "growth": 0.3,
            "activist": 0.6,
        },
        MarketRegime.RANGE_VOLATILE: {
            "futures": 2.0,   # 期货交易员在震荡高波动表现最好
            "quant": 1.5,
            "macro": 1.3,
            "value": 0.6,
            "growth": 0.5,
            "activist": 0.8,
        },
        MarketRegime.RANGE_CALM: {
            "value": 1.3,
            "activist": 1.5,
            "growth": 1.1,
            "macro": 0.8,
            "futures": 0.5,
            "quant": 1.2,
        },
    }
    
    def __init__(self):
        self.current_regime: MarketRegime = MarketRegime.BULL_GROWTH
        self.current_weights: Dict[str, float] = {}
    
    def detect_regime(self, indicators: MarketIndicators) -> MarketRegime:
        """
        根据市场指标识别当前市场环境
        
        逻辑:
        - 牛市判断: 主要指数上涨 + 情绪贪婪/中性
        - 熊市判断: 主要指数下跌 + 情绪恐惧
        - 震荡判断: 指数横盘 + VIX适中
        - 高波动: VIX > 25
        - 低波动: VIX < 15
        """
        # 简化的判断逻辑
        is_bull = indicators.sp500_trend == "up" and indicators.nasdaq_trend == "up"
        is_bear = indicators.sp500_trend == "down" and indicators.sentiment in ["fear", "extreme_fear"]
        is_volatile = indicators.vix_level > 25
        
        if is_bull and not is_volatile:
            # 判断是成长牛还是价值牛
            if indicators.nasdaq_trend == "up" and indicators.interest_rate_trend in ["stable", "falling"]:
                return MarketRegime.BULL_GROWTH
            else:
                return MarketRegime.BULL_VALUE
        
        elif is_bear:
            if indicators.inflation_trend == "rising":
                return MarketRegime.BEAR_INFLATION  # 滞胀
            else:
                return MarketRegime.BEAR_DEFLATION  # 通缩型熊市
        
        else:  # 震荡市
            if is_volatile:
                return MarketRegime.RANGE_VOLATILE
            else:
                return MarketRegime.RANGE_CALM
    
    def calculate_weights(self, regime: MarketRegime) -> Dict[str, float]:
        """
        计算指定市场环境下的权重
        """
        multipliers = self.REGIME_MULTIPLIERS[regime]
        
        # 计算加权后的权重
        weighted_weights = {}
        for master, config in self.BASE_WEIGHTS.items():
            category = config["category"]
            base_weight = config["base_weight"]
            multiplier = multipliers.get(category, 1.0)
            
            weighted_weights[master] = base_weight * multiplier
        
        # 归一化 (使权重总和为1)
        total = sum(weighted_weights.values())
        normalized_weights = {
            k: round(v / total, 4) 
            for k, v in weighted_weights.items()
        }
        
        return normalized_weights
    
    def get_weights(self, regime: MarketRegime = None) -> Dict[str, float]:
        """
        获取当前权重配置
        """
        if regime is None:
            regime = self.current_regime
        
        return self.calculate_weights(regime)
    
    def update_regime(self, indicators: MarketIndicators):
        """
        更新市场环境并重新计算权重
        """
        new_regime = self.detect_regime(indicators)
        
        if new_regime != self.current_regime:
            print(f"🔄 市场环境切换: {self.current_regime.value} → {new_regime.value}")
            self.current_regime = new_regime
            self.current_weights = self.calculate_weights(new_regime)
        
        return self.current_regime
    
    def get_top_masters(self, n: int = 5) -> List[Tuple[str, float]]:
        """
        获取当前权重最高的n位大师
        """
        weights = self.get_weights()
        sorted_masters = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        return sorted_masters[:n]
    
    def explain_weights(self, regime: MarketRegime = None) -> str:
        """
        解释当前权重配置的原因
        """
        if regime is None:
            regime = self.current_regime
        
        explanations = {
            MarketRegime.BULL_GROWTH: """
当前市场: 牛市-成长环境
特征: 经济增长 + 通胀回落 + 流动性充裕
策略: 重仓成长股大师，轻仓价值大师
原因: 成长股在流动性充裕、低利率环境下表现最佳
""",
            MarketRegime.BEAR_DEFLATION: """
当前市场: 熊市-通缩环境
特征: 经济衰退 + 低通胀 + 流动性收紧
策略: 重仓价值大师，规避成长股
原因: 价值股防御性强，现金流稳定，在衰退期相对抗跌
""",
            MarketRegime.BEAR_INFLATION: """
当前市场: 熊市-滞胀环境
特征: 经济衰退 + 高通胀
策略: 重仓宏观对冲大师，轻仓成长股
原因: 滞胀期需要灵活资产配置，商品和宏观对冲表现较好
""",
            MarketRegime.RANGE_VOLATILE: """
当前市场: 震荡-高波动环境
特征: 指数横盘 + 波动率高
策略: 重仓期货交易员，轻仓长期投资者
原因: 震荡市适合趋势跟踪和波段交易， Buy & Hold策略失效
""",
        }
        
        return explanations.get(regime, "市场环境未定义")


# 便捷函数
def get_adaptive_weights(indicators: MarketIndicators) -> Dict[str, float]:
    """根据市场指标获取自适应权重"""
    aws = AdaptiveWeightSystem()
    regime = aws.detect_regime(indicators)
    return aws.get_weights(regime)


def print_weight_table(weights: Dict[str, float]):
    """打印权重表"""
    print("\n📊 大师权重配置")
    print("=" * 50)
    sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    
    for i, (master, weight) in enumerate(sorted_weights[:10], 1):
        bar = "█" * int(weight * 100)
        print(f"{i:2}. {master:15} {weight*100:5.1f}% {bar}")


if __name__ == "__main__":
    # 测试
    print("🧪 自适应权重系统测试")
    
    aws = AdaptiveWeightSystem()
    
    # 测试不同市场环境
    test_regimes = [
        MarketRegime.BULL_GROWTH,
        MarketRegime.BEAR_DEFLATION,
        MarketRegime.RANGE_VOLATILE,
    ]
    
    for regime in test_regimes:
        print(f"\n{'='*60}")
        print(f"市场环境: {regime.value}")
        print("="*60)
        
        weights = aws.get_weights(regime)
        print_weight_table(weights)
        
        # 显示推荐大师
        top_masters = aws.get_top_masters(5)
        print(f"\n🎯 推荐大师: {', '.join([m[0] for m in top_masters])}")
        
        print(aws.explain_weights(regime))
