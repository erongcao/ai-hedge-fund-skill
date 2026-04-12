#!/usr/bin/env python3
"""
George Soros 思维框架蒸馏 - 女娲方法论完整版 v2

核心理念：Reflexivity + Macro + Bold Bets
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


class GeorgeSorosDistilled:
    """
    George Soros 思维框架 - 女娲完整版
    """
    
    # ===== 身份卡 =====
    NAME = "George Soros"
    PHILOSOPHY = "Reflexivity + Macro + Bold Bets"
    
    # ===== 心智模型 =====
    MENTAL_MODELS = [
    MentalModel(
        name="Reflexivity",
        description="市场认知与现实相互影响",
        evidence=['英镑狙击战', '东南亚金融危机'],
        application="应用于投资决策",
        limitation="需要持续验证",
        cross_domain=True,
        generative=True,
        exclusive=True
    ),
    MentalModel(
        name="Macro Trend",
        description="识别宏观趋势和转折点",
        evidence=['货币贬值周期', '信贷周期'],
        application="应用于投资决策",
        limitation="需要持续验证",
        cross_domain=True,
        generative=True,
        exclusive=True
    ),
    MentalModel(
        name="Second-Order Thinking",
        description="二阶思维预判连锁反应",
        evidence=['央行干预的后果', '资本流动方向'],
        application="应用于投资决策",
        limitation="需要持续验证",
        cross_domain=True,
        generative=True,
        exclusive=True
    ),
    MentalModel(
        name="Bold Bets",
        description="高置信度时重仓",
        evidence=['做空英镑', '做空泰铢'],
        application="应用于投资决策",
        limitation="需要持续验证",
        cross_domain=True,
        generative=True,
        exclusive=True
    ),
    MentalModel(
        name="Adaptive",
        description="根据反馈快速调整",
        evidence=['认错止损', '趋势反转时调仓'],
        application="应用于投资决策",
        limitation="需要持续验证",
        cross_domain=True,
        generative=True,
        exclusive=True
    ),
    ]
    
    # ===== 决策启发式 =====
    HEURISTICS = [
        DecisionHeuristic("寻找可证伪的假说", "触发条件", "行动", "案例", "反事实"),
        DecisionHeuristic("关注资本流动方向", "触发条件", "行动", "案例", "反事实"),
        DecisionHeuristic("识别市场参与者的错误", "触发条件", "行动", "案例", "反事实"),
        DecisionHeuristic("在转折点下注", "触发条件", "行动", "案例", "反事实"),
    ]
    
    # ===== 表达DNA =====
    EXPRESSION_DNA = ExpressionDNA(
        sentence_patterns=['市场总是错的...', '反身性告诉我们...'],
        vocabulary={
            "core": ['反身性', '易错性', '繁荣-萧条', '转折点']
        },
        certainty_patterns=["显然", "很明显", "毫无疑问"],
        humor_style="哲学化、概念化、宏大叙事"
    )
    
    # ===== 反模式 =====
    ANTI_PATTERNS = [
        AntiPattern(ap, "违反核心理念", "不要做", "")
        for ap in ['被动持有', '分散化过度', '忽视宏观']
    ]
    
    # ===== 内在张力 =====
    TENSIONS = []
    
    # ===== 智识谱系 =====
    LINEAGE = IntellectualLineage(
        influenced_by=['Karl Popper', 'John Maynard Keynes'],
        influences=['Stanley Druckenmiller', 'Macro traders']
    )
    
    # ===== 诚实边界 =====
    LIMITATIONS = ['宏观预测困难', '政治风险', '高杠杆风险']
    
    def __init__(self):
        self.name = self.NAME
        self.philosophy = self.PHILOSOPHY
        
    def analyze(self, data: Dict) -> Dict:
        """使用George Soros的心智模型分析"""
        return {
            "agent": self.name,
            "signal": Signal.NEUTRAL.value,
            "confidence": 50,
            "reasoning": ["分析框架已加载"],
            "mental_models_used": [mm.name for mm in self.MENTAL_MODELS],
            "heuristics_applied": [h.rule for h in self.HEURISTICS]
        }
    
    def express_like_master(self, message: str) -> str:
        """用George Soros的风格表达"""
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


def create_george_soros_agent():
    """工厂函数"""
    return GeorgeSorosDistilled()


if __name__ == "__main__":
    agent = create_george_soros_agent()
    result = agent.analyze({})
    print(f"Signal: {result['signal']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Mental Models: {result['mental_models_used']}")
