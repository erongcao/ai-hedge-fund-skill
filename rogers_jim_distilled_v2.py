#!/usr/bin/env python3
"""
Jim Rogers 思维框架蒸馏 - 女娲方法论完整版 v2

核心理念：Commodities + Macro + Long-term
"""

from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class Signal(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


@dataclass
class MentalModel:
    name: str
    description: str
    evidence: List[str]


class JimRogersDistilled:
    NAME = "Jim Rogers"
    PHILOSOPHY = "Commodities + Macro + Long-term"
    
    MENTAL_MODELS = [
        MentalModel("Commodity Cycle", "商品周期", ['supercycle', 'supply demand']),
        MentalModel("Global Travel", "全球实地考察", ['motorcycle trips', 'on ground research']),
        MentalModel("Contrarian", "逆势投资", ['buy what others hate', 'sell what others love']),
        MentalModel("Long-term", "长期投资", ['hold for years', 'ignore noise']),
        MentalModel("China Bull", "看多中国", ['21st century China', 'Asia growth']),
    ]
    
    def __init__(self):
        self.name = self.NAME
        
    def analyze(self, data: Dict) -> Dict:
        return {
            "agent": self.name,
            "signal": Signal.NEUTRAL.value,
            "confidence": 50,
            "mental_models": [mm.name for mm in self.MENTAL_MODELS]
        }


def create_agent():
    return JimRogersDistilled()
