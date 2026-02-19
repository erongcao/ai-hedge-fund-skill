"""
Base classes for AI Hedge Fund
Separated to avoid circular imports
"""

from dataclasses import dataclass
from typing import Dict, List, Literal, Optional


@dataclass
class AgentSignal:
    """Signal from an investment agent"""
    agent_name: str
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int  # 0-100
    reasoning: str
    key_metrics: Optional[Dict] = None


@dataclass
class ConsensusResult:
    """Final consensus from all agents"""
    ticker: str
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int
    agreement: str
    agent_signals: List[AgentSignal]
    key_risks: List[str]
    recommendation: str
    analysis_date: str
    enhanced_data: Optional[Dict] = None


class InvestmentAgent:
    """Base class for investment agents"""
    
    def __init__(self, name: str, philosophy: str):
        self.name = name
        self.philosophy = philosophy
    
    def analyze(self, data: Dict) -> AgentSignal:
        """Analyze stock data and return signal - override in subclass"""
        raise NotImplementedError
