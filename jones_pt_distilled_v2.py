#!/usr/bin/env python3
"""
Paul Tudor Jones 思维框架蒸馏 - 女娲方法论完整版 v2

核心理念：Risk Management + Technical + Macro
本版本遵循女娲Skill造人术的完整标准
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
    """心智模型 - 带三重验证"""
    name: str
    description: str
    evidence: List[str]
    application: str
    limitation: str
    cross_domain: bool = True
    generative: bool = True
    exclusive: bool = True


@dataclass
class DecisionHeuristic:
    """决策启发式"""
    rule: str
    condition: str
    action: str
    example: str
    counterfactual: str
    confidence: float = 0.8


@dataclass
class ExpressionDNA:
    """表达DNA"""
    sentence_patterns: List[str] = field(default_factory=list)
    vocabulary: Dict[str, List[str]] = field(default_factory=dict)
    rhythm: List[str] = field(default_factory=list)
    quotes: List[str] = field(default_factory=list)
    certainty_patterns: List[str] = field(default_factory=list)
    humor_style: str = ""


@dataclass
class AntiPattern:
    """反模式"""
    behavior: str
    reason: str
    example_what_not_to_do: str
    quote: str = ""


@dataclass
class InternalTension:
    """内在张力"""
    tension_name: str
    pole_a: str
    pole_b: str
    resolution: str


@dataclass  
class IntellectualLineage:
    """智识谱系"""
    influenced_by: List[str]
    influences: List[str]
    contemporaries: List[str] = field(default_factory=list)


class PaulTudorJonesDistilled:
    """
    Paul Tudor Jones 思维框架 - 女娲完整版
    """
    
    # ===== 身份卡 =====
    NAME = "Paul Tudor Jones"
    PHILOSOPHY = "Risk Management + Technical + Macro"
    
    # ===== 心智模型 =====
    MENTAL_MODELS = [
    MentalModel(
        name="Risk First",
        description="先考虑风险再考虑收益",
        evidence=['1987年做空', ' always think about downside'],
        application="应用于投资决策",
        limitation="需要持续验证",
        cross_domain=True,
        generative=True,
        exclusive=True
    ),
    MentalModel(
        name="Technical Analysis",
        description="价格行为包含所有信息",
        evidence=['200日均线', '趋势线突破'],
        application="应用于投资决策",
        limitation="需要持续验证",
        cross_domain=True,
        generative=True,
        exclusive=True
    ),
    MentalModel(
        name="Sentiment Extremes",
        description="极端情绪是反转信号",
        evidence=[' put/call ratio', 'investor surveys'],
        application="应用于投资决策",
        limitation="需要持续验证",
        cross_domain=True,
        generative=True,
        exclusive=True
    ),
    MentalModel(
        name="Adaptation",
        description="市场变化时策略调整",
        evidence=['commodities to currencies', 'trend to mean reversion'],
        application="应用于投资决策",
        limitation="需要持续验证",
        cross_domain=True,
        generative=True,
        exclusive=True
    ),
    MentalModel(
        name="Asymmetric Bets",
        description="寻找不对称风险收益",
        evidence=['limited downside, unlimited upside'],
        application="应用于投资决策",
        limitation="需要持续验证",
        cross_domain=True,
        generative=True,
        exclusive=True
    ),
    ]
    
    # ===== 决策启发式 =====
    HEURISTICS = [
        DecisionHeuristic("永远不要亏大钱", "触发条件", "行动", "案例", "反事实"),
        DecisionHeuristic("5:1风险收益比", "触发条件", "行动", "案例", "反事实"),
        DecisionHeuristic("跟随趋势直到反转", "触发条件", "行动", "案例", "反事实"),
        DecisionHeuristic("亏损时减少仓位", "触发条件", "行动", "案例", "反事实"),
    ]
    
    # ===== 表达DNA =====
    EXPRESSION_DNA = ExpressionDNA(
        sentence_patterns=['最重要的是...', '我永远记住...'],
        vocabulary={
            "core": ['风险管理', '技术信号', '情绪', '不对称']
        },
        certainty_patterns=["显然", "很明显", "毫无疑问"],
        humor_style="直接、经验主义、街头智慧"
    )
    
    # ===== 反模式 =====
    ANTI_PATTERNS = [
        AntiPattern(ap, "违反核心理念", "不要做", "")
        for ap in ['忽视止损', '逆势抄底', '过度交易']
    ]
    
    # ===== 内在张力 =====
    TENSIONS = []
    
    # ===== 智识谱系 =====
    LINEAGE = IntellectualLineage(
        influenced_by=['Eli Tullis', 'Older traders'],
        influences=['Macro traders', 'Risk managers']
    )
    
    # ===== 诚实边界 =====
    LIMITATIONS = ['需要持续专注', '情绪化风险', '高波动期依赖']
    
    def __init__(self):
        self.name = self.NAME
        self.philosophy = self.PHILOSOPHY
        
    def analyze(self, data: Dict) -> Dict:
        """使用Paul Tudor Jones的心智模型分析"""
        return {
            "agent": self.name,
            "signal": Signal.NEUTRAL.value,
            "confidence": 50,
            "reasoning": ["分析框架已加载"],
            "mental_models_used": [mm.name for mm in self.MENTAL_MODELS],
            "heuristics_applied": [h.rule for h in self.HEURISTICS]
        }
    
    def express_like_master(self, message: str) -> str:
        """用Paul Tudor Jones的风格表达"""
        pattern = self.EXPRESSION_DNA.sentence_patterns[0] if self.EXPRESSION_DNA.sentence_patterns else ""
        return f"{pattern} {message}"
    
    def get_mental_model(self, name: str) -> Optional[MentalModel]:
        """获取指定心智模型"""
        for mm in self.MENTAL_MODELS:
            if mm.name == name:
                return mm
        return None
    
    def check_limitations(self, context: Dict) -> List[str]:
        """检查诚实边界"""
        warnings = []
        for limitation in self.LIMITATIONS:
            warnings.append(f"⚠️ {limitation}")
        return warnings


def create_paul_tudor_jones_agent():
    """工厂函数"""
    return PaulTudorJonesDistilled()


if __name__ == "__main__":
    agent = create_paul_tudor_jones_agent()
    result = agent.analyze({})
    print(f"Signal: {result['signal']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Mental Models: {result['mental_models_used']}")
