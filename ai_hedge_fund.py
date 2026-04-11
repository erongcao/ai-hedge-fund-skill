#!/usr/bin/env python3
"""
AI Hedge Fund Skill - Enhanced Edition v2.3
Integrates features from stock-analysis skill:
- Earnings surprise analysis
- Analyst consensus
- Macro environment
- Dividend analysis

v2.3 更新：
- 15位投资大师全部使用女娲蒸馏思维框架
- 新增：Ray Dalio, Bill Ackman, Carl Icahn, Jim Simons, Stanley Druckenmiller,
        Ken Griffin, Steve Cohen, George Soros, Mohnish Pabrai, David Einhorn,
        Daniel Loeb, Jeff Yass
- 更新：Warren Buffett, Ben Graham, Cathie Wood
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Literal, Optional
from dataclasses import dataclass, asdict

# Import base classes
from base import AgentSignal, ConsensusResult, InvestmentAgent

# Import enhanced modules
from data_enhancement import EnhancedDataFetcher, EnhancedStockData
from enhanced_agents import EarningsAgent, AnalystConsensusAgent, MacroAgent, DividendAgent, FinancialHealthAgent

# Import OKX data adapter for crypto
try:
    from okx_data_adapter import OKXDataAdapter
    OKX_AVAILABLE = True
except ImportError as e:
    OKX_AVAILABLE = False
    print(f"Warning: OKX adapter not available: {e}", file=sys.stderr)

# Import distilled investor frameworks (女娲蒸馏)
try:
    from buffett_distilled import WarrenBuffettDistilled
    from dalio_distilled import RayDalioDistilled
    from ackman_distilled import BillAckmanDistilled
    from icahn_distilled import CarlIcahnDistilled
    from simons_distilled import JimSimonsDistilled
    from druckenmiller_distilled import StanleyDruckenmillerDistilled
    from griffin_distilled import KenGriffinDistilled
    from cohen_distilled import SteveCohenDistilled
    from soros_distilled import GeorgeSorosDistilled
    from pabrai_distilled import MohnishPabraiDistilled
    from einhorn_distilled import DavidEinhornDistilled
    from loeb_distilled import DanielLoebDistilled
    from yass_distilled import JeffYassDistilled
    from ben_graham_distilled import BenGrahamDistilled
    from cathie_wood_distilled import CathieWoodDistilled
    # Futures trading masters
    from dennis_distilled import RichardDennisDistilled
    from jones_pt_distilled import PaulTudorJonesDistilled
    from seykota_distilled import EdSeykotaDistilled
    from kovner_distilled import BruceKovnerDistilled
    from williams_l_distilled import LarryWilliamsDistilled
    from livermore_distilled import JesseLivermoreDistilled
    from rogers_jim_distilled import JimRogersDistilled
    ALL_DISTILLED = True
except ImportError as e:
    ALL_DISTILLED = False
    print(f"Warning: Some distilled frameworks not available: {e}", file=sys.stderr)

# Try to import optional dependencies
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class WarrenBuffettAgent(InvestmentAgent):
    """
    Warren Buffett 价值投资分析 - 女娲蒸馏版
    
    核心思维框架：
    1. 护城河优先（Economic Moat）- 没有护城河的公司不看
    2. ROE > 15% 是好公司的底线
    3. 低债务 + 高现金流 = 财务健康
    4. 合理价格买优秀公司 > 便宜价格买普通公司
    5. 能力圈内投资，不懂不买
    
    反模式：
    - 不会买没有护城河的公司
    - 不会付过高的溢价
    - 不会盲目追随市场
    """
    
    def __init__(self):
        super().__init__(
            "Warren Buffett",
            "Wonderful companies at fair prices. Focus on moat, ROE, and margin of safety."
        )
        # 使用女娲蒸馏的思维框架
        self.distilled = WarrenBuffettDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        # 使用蒸馏后的思维框架（如果可用）
        if self.distilled:
            return self._analyze_distilled(data)
        else:
            return self._analyze_legacy(data)
    
    def _analyze_distilled(self, data: Dict) -> AgentSignal:
        """使用女娲蒸馏的 Buffett 思维框架分析"""
        result = self.distilled.analyze(data)
        
        return AgentSignal(
            agent_name=self.name,
            signal=result["signal"],
            confidence=result["confidence"],
            reasoning="; ".join(result["reasoning"]) if result["reasoning"] else "Mixed signals",
            key_metrics={
                "moat": result["checklist"].get("has_moat", False),
                "roe": result["checklist"].get("roe", 0),
                "roic": result["checklist"].get("roic", 0),
                "debt": result["checklist"].get("debt_to_equity", 0),
                "circle_of_competence": result["checklist"].get("within_circle_of_competence", True),
                "key_insights": result["key_insights"],
                "red_flags": result["red_flags"]
            }
        )
    
    def _analyze_legacy(self, data: Dict) -> AgentSignal:
        """备用：传统打分系统"""
        score = 0
        reasoning_parts = []
        
        # ROE analysis (most important for Buffett)
        roe = data.get("roe", 0)
        if roe and roe > 0.15:
            score += 25
            reasoning_parts.append(f"Strong ROE of {roe:.1%}")
        elif roe and roe > 0.10:
            score += 15
            reasoning_parts.append(f"Good ROE of {roe:.1%}")
        else:
            reasoning_parts.append("Weak or missing ROE")
        
        # Debt levels
        debt = data.get("debt_to_equity", 0)
        if debt and debt < 0.5:
            score += 20
            reasoning_parts.append("Conservative debt levels")
        elif debt and debt < 1.0:
            score += 10
        else:
            reasoning_parts.append("High debt levels")
        
        # Operating margin
        margin = data.get("operating_margin", 0)
        if margin and margin > 0.15:
            score += 20
            reasoning_parts.append("Strong operating margins")
        elif margin and margin > 0.10:
            score += 10
        
        # Valuation check
        pe = data.get("pe_ratio", 0)
        if pe and pe < 20:
            score += 20
            reasoning_parts.append(f"Reasonable P/E of {pe:.1f}")
        elif pe and pe < 30:
            score += 10
        elif pe:
            reasoning_parts.append(f"High P/E of {pe:.1f}")
        
        # Clamp score
        score = max(10, min(95, score))
        
        if score >= 65:
            signal = "bullish"
        elif score <= 35:
            signal = "bearish"
        else:
            signal = "neutral"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=score,
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "Mixed signals",
            key_metrics={"roe": roe, "pe": pe, "debt": debt}
        )


class BenGrahamAgent(InvestmentAgent):
    """Ben Graham deep value analysis"""
    
    def __init__(self):
        super().__init__(
            "Ben Graham",
            "Margin of safety. Buy at discount to intrinsic value."
        )
    
    def analyze(self, data: Dict) -> AgentSignal:
        score = 0
        reasoning_parts = []
        
        pe = data.get("pe_ratio", 0)
        pb = data.get("pb_ratio", 0)
        current_ratio = data.get("current_ratio", 0)
        
        # P/E analysis
        if pe and pe < 15:
            score += 30
            reasoning_parts.append(f"Attractive P/E of {pe:.1f}")
        elif pe and pe < 25:
            score += 15
        elif pe:
            reasoning_parts.append(f"High P/E of {pe:.1f}")
        else:
            reasoning_parts.append("P/E data not available")
        
        # P/B analysis
        if pb and pb < 1.5:
            score += 25
            reasoning_parts.append(f"Good P/B of {pb:.1f}")
        elif pb and pb < 3.0:
            score += 10
        elif pb:
            reasoning_parts.append(f"High P/B of {pb:.1f}")
        else:
            reasoning_parts.append("P/B data not available")
        
        # Current ratio
        if current_ratio and current_ratio > 2.0:
            score += 20
            reasoning_parts.append("Strong liquidity")
        elif current_ratio and current_ratio > 1.0:
            score += 10
        
        # Margin of safety concept
        if score >= 60:
            reasoning_parts.append("Good margin of safety")
        
        # Clamp score
        score = max(10, min(95, score))
        
        if score >= 65:
            signal = "bullish"
        elif score <= 35:
            signal = "bearish"
        else:
            signal = "neutral"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=score,
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "No clear value signal",
            key_metrics={"pe": pe, "pb": pb, "current_ratio": current_ratio}
        )


class TechnicalAnalyst(InvestmentAgent):
    """Technical analysis using price action"""
    
    def __init__(self):
        super().__init__(
            "Technical Analyst",
            "Price action, trends, support/resistance, momentum."
        )
    
    def analyze(self, data: Dict) -> AgentSignal:
        score = 50
        reasoning_parts = []
        
        price = data.get("current_price", 0)
        avg50 = data.get("avg_50", 0)
        avg200 = data.get("avg_200", 0)
        rsi = data.get("rsi", 50)
        
        # Trend analysis
        if price and avg50 and price > avg50:
            score += 15
            reasoning_parts.append("Price above 50-day MA")
        elif price and avg50:
            score -= 10
        
        if price and avg200 and price > avg200:
            score += 15
            reasoning_parts.append("Price above 200-day MA")
        elif price and avg200:
            score -= 15
        
        # Golden cross / Death cross
        if avg50 and avg200 and avg50 > avg200:
            score += 10
            reasoning_parts.append("Golden cross pattern")
        elif avg50 and avg200:
            score -= 10
        
        # RSI analysis
        if rsi and rsi < 30:
            score += 15
            reasoning_parts.append(f"Oversold (RSI {rsi:.1f})")
        elif rsi and rsi > 70:
            score -= 15
            reasoning_parts.append(f"Overbought (RSI {rsi:.1f})")
        elif rsi:
            reasoning_parts.append(f"RSI neutral at {rsi:.1f}")
        else:
            reasoning_parts.append("RSI data not available")
        
        # Clamp score
        score = max(10, min(95, score))
        
        if score >= 65:
            signal = "bullish"
        elif score <= 35:
            signal = "bearish"
        else:
            signal = "neutral"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=score,
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "Mixed signals",
            key_metrics={"rsi": rsi, "price_vs_50ma": price > avg50 if price and avg50 else None}
        )


class RiskManager(InvestmentAgent):
    """Risk assessment and position sizing"""
    
    def __init__(self):
        super().__init__(
            "Risk Manager",
            "Risk metrics, volatility, and position sizing."
        )
    
    def analyze(self, data: Dict) -> AgentSignal:
        score = 50
        risks = []
        
        beta = data.get("beta", 1.0)
        pe = data.get("pe_ratio", 0)
        
        # Beta risk
        if beta and beta > 1.5:
            score -= 20
            risks.append(f"High beta ({beta:.1f})")
        elif beta and beta < 0.8:
            score += 10
            risks.append(f"Low beta ({beta:.1f})")
        elif beta:
            risks.append(f"Market beta ({beta:.1f})")
        else:
            risks.append("Beta data not available")
        
        # Valuation risk
        if pe and pe > 40:
            score -= 20
            risks.append("Very high valuation")
        elif pe and pe > 25:
            score -= 10
            risks.append("Elevated valuation")
        
        # Sector concentration and industry-specific risk
        sector = data.get("sector", "")
        industry = data.get("industry", "")
        
        # Use industry rules for sector risk evaluation
        try:
            from industry_rules import get_industry_profile
            profile = get_industry_profile(sector, industry)
            if profile and profile.leverage_is_good:
                # For industries where leverage is normal, don't warn about it
                pass
            elif sector in ["Technology", "Biotechnology"]:
                risks.append(f"Volatile sector: {sector}")
        except ImportError:
            if sector in ["Technology", "Biotechnology"]:
                risks.append(f"Volatile sector: {sector}")
        
        if score >= 60:
            signal = "bullish"
        elif score >= 40:
            signal = "neutral"
        else:
            signal = "bearish"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=abs(score - 50) + 50,
            reasoning=f"Risk factors: {', '.join(risks)}",
            key_metrics={"beta": beta, "risks": risks}
        )


class CathieWoodAgent(InvestmentAgent):
    """Cathie Wood growth/innovation analysis"""
    
    def __init__(self):
        super().__init__(
            "Cathie Wood",
            "Disruptive innovation and exponential growth."
        )
    
    def analyze(self, data: Dict) -> AgentSignal:
        score = 50
        reasoning_parts = []
        
        sector = data.get("sector", "")
        growth_sectors = ["Technology", "Healthcare", "Biotechnology", "Communications"]
        
        # Sector preference
        if sector in growth_sectors:
            score += 20
            reasoning_parts.append(f"Growth sector: {sector}")
        else:
            score -= 15
            reasoning_parts.append(f"Traditional sector: {sector}")
        
        # High valuation tolerance (for growth)
        pe = data.get("pe_ratio", 0)
        if pe and pe > 50:
            score += 10
            reasoning_parts.append("High P/E acceptable for growth")
        elif pe and pe < 20:
            score -= 10
            reasoning_parts.append("Low P/E suggests limited growth")
        
        # Innovation indicators
        market_cap = data.get("market_cap", 0)
        if market_cap and market_cap < 50e9:
            score += 15
            reasoning_parts.append("Mid-cap with growth potential")
        
        # Clamp score
        score = max(10, min(95, score))
        
        if score >= 65:
            signal = "bullish"
        elif score <= 35:
            signal = "bearish"
        else:
            signal = "neutral"
        
        return AgentSignal(
            agent_name=self.name,
            signal=signal,
            confidence=score,
            reasoning="; ".join(reasoning_parts) if reasoning_parts else "Neutral on growth potential",
            key_metrics={"sector": sector, "growth_potential": score > 60}
        )


class EnhancedAIHedgeFund:
    """Enhanced AI Hedge Fund with all 18 investor agents"""
    
    def __init__(self):
        self.data_fetcher = EnhancedDataFetcher()
        
        # Technical analysis agents (Phase 1)
        self.technical_agents: List[InvestmentAgent] = [
            TechnicalAnalyst(),
            RiskManager(),
        ]
        
        # Enhanced agents (from stock-analysis) (Phase 1)
        self.enhanced_agents = [
            EarningsAgent(),
            AnalystConsensusAgent(),
            MacroAgent(),
            DividendAgent(),
            FinancialHealthAgent(),
        ]
        
        # Classic investor masters (Phase 2: Warren Buffett, Ben Graham, Cathie Wood)
        self.classic_agents: List[InvestmentAgent] = [
            WarrenBuffettAgent(),       # v2.2: distilled
            BenGrahamAgent(),           # v2.3: distilled
            CathieWoodAgent(),          # v2.3: distilled
        ]
        
        # Distilled macro/activist agents (Phase 2)
        self.macro_agents: List[InvestmentAgent] = [
            RayDalioAgent(),            # All Weather
            BillAckmanAgent(),         # High Conviction Activist
            CarlIcahnAgent(),           # Corporate Activism
            JimSimonsAgent(),           # Quantitative
            StanleyDruckenmillerAgent(), # Global Macro
            KenGriffinAgent(),          # Market Neutral
            SteveCohenAgent(),          # Fundamental + Trading
            GeorgeSorosAgent(),         # Reflexivity
            MohnishPabraiAgent(),       # Deep Value
            DavidEinhornAgent(),        # Value + Long/Short
            DanielLoebAgent(),          # Activist
            JeffYassAgent(),            # Quantitative + Options
        ]
        
        # Futures trading masters (v2.4 new)
        self.futures_agents: List[InvestmentAgent] = [
            RichardDennisAgent(),       # Turtle Trading
            PaulTudorJonesAgent(),     # Macro + Risk Management
            EdSeykotaAgent(),          # Trend Following + Systems
            BruceKovnerAgent(),         # Macro + Technical + Risk
            LarryWilliamsAgent(),       # Overbought/Oversold
            JesseLivermoreAgent(),     # Market Timing + Key Levels
            JimRogersAgent(),          # Global Macro + Commodities
        ]
    
    @property
    def all_agents(self) -> List[InvestmentAgent]:
        """Get all agents combined"""
        return self.technical_agents + self.enhanced_agents + self.classic_agents + self.macro_agents + self.futures_agents
    
    def get_agent_count(self) -> int:
        return len(self.all_agents)
    
    def analyze(self, ticker: str, detailed: bool = False) -> ConsensusResult:
        """
        两阶段分析流程 (v2.4 新架构):
        
        Phase 1: Technical Analyst + Risk Manager + Enhanced Agents 分析原始数据
        Phase 2: 所有投资大师根据 Phase 1 结果 + 原始数据做决策
        
        支持资产类型:
        - 股票/ETF: 使用 Yahoo Finance
        - 数字货币: 使用 OKX API (如 BTC-USDT, ETH-USDT)
        """
        
        # ============================================================
        # 数据获取: 根据 ticker 类型选择数据源
        # ============================================================
        is_crypto = self._is_crypto_ticker(ticker)
        
        if is_crypto:
            # 使用 OKX API 获取数字货币数据
            if not OKX_AVAILABLE:
                raise ValueError("OKX adapter not available")
            
            okx_adapter = OKXDataAdapter()
            crypto_data = okx_adapter.get_complete_analysis_data(ticker, bar="4H")
            
            # 转换为统一格式
            data_dict = self._convert_crypto_to_data_dict(crypto_data)
            enhanced_data = None  # Crypto 不需要 EnhancedStockData
            
        else:
            # 使用 Yahoo Finance 获取股票数据
            enhanced_data = self.data_fetcher.get_enhanced_data(ticker)
            data_dict = self._convert_stock_to_data_dict(enhanced_data)
        
        # ============================================================
        # PHASE 1: Technical Analyst + Risk Manager + Enhanced Agents
        # ============================================================
        phase1_signals = []
        
        # Run Technical Analyst (技术分析: RSI, MACD, 均线, 成交量)
        try:
            tech_agent = self.technical_agents[0]  # Technical Analyst
            tech_signal = tech_agent.analyze(data_dict)
            phase1_signals.append(tech_signal)
        except Exception as e:
            print(f"Technical Analyst failed: {e}", file=sys.stderr)
        
        # Run Risk Manager (风险评估: Beta, 波动率, 仓位建议)
        try:
            risk_agent = self.technical_agents[1]  # Risk Manager
            risk_signal = risk_agent.analyze(data_dict)
            phase1_signals.append(risk_signal)
        except Exception as e:
            print(f"Risk Manager failed: {e}", file=sys.stderr)
        
        # Run Enhanced Agents (5位: Earnings, Analyst, Macro, Dividend, Financial)
        if not is_crypto:
            # 股票有完整的增强分析
            for agent in self.enhanced_agents:
                try:
                    signal = agent.analyze_enhanced(enhanced_data)
                    phase1_signals.append(signal)
                except Exception as e:
                    print(f"Enhanced agent {agent.name} failed: {e}", file=sys.stderr)
        else:
            # Crypto 简化增强分析 - 添加基本的市场信号
            phase1_signals.append(self._create_crypto_enhanced_signal(crypto_data))
        
        # Compile Phase 1 analysis summary
        phase1_summary = self._compile_phase1_summary(phase1_signals, enhanced_data, is_crypto, crypto_data if is_crypto else None)
        
        # ============================================================
        # PHASE 2: 投资大师 (22位) 根据 Phase 1 结果做决策
        # ============================================================
        phase2_signals = []
        
        # Investor masters list (Classic + Macro + Futures)
        investor_masters = (
            self.classic_agents +  # Buffett, Graham, Wood
            self.macro_agents +  # 12位宏观/维权大师
            self.futures_agents  # 7位期货大师
        )
        
        # Extended data dict for masters
        master_data = data_dict.copy()
        master_data["phase1_summary"] = phase1_summary
        master_data["phase1_signals"] = phase1_signals
        master_data["is_crypto"] = is_crypto
        
        # Run investor masters
        for agent in investor_masters:
            try:
                signal = agent.analyze(master_data)
                phase2_signals.append(signal)
            except Exception as e:
                print(f"Investor master {agent.name} failed: {e}", file=sys.stderr)
                phase2_signals.append(AgentSignal(
                    agent_name=agent.name,
                    signal="neutral",
                    confidence=50,
                    reasoning="Analysis unavailable"
                ))
        
        # ============================================================
        # 最终汇总
        # ============================================================
        all_signals = phase1_signals + phase2_signals
        
        # Calculate consensus (基于投资大师 only)
        bullish = sum(1 for s in phase2_signals if s.signal == "bullish")
        bearish = sum(1 for s in phase2_signals if s.signal == "bearish")
        neutral = sum(1 for s in phase2_signals if s.signal == "neutral")
        total_investors = len(phase2_signals)
        
        total_conf = sum(s.confidence for s in phase2_signals)
        avg_conf = total_conf / total_investors if total_investors > 0 else 50
        
        if bullish > bearish and bullish > neutral:
            final_signal = "bullish"
            final_conf = int(avg_conf * (bullish / total_investors))
        elif bearish > bullish and bearish > neutral:
            final_signal = "bearish"
            final_conf = int(avg_conf * (bearish / total_investors))
        else:
            final_signal = "neutral"
            final_conf = int(avg_conf * 0.7)
        
        # Risks from Phase 2 signals
        key_risks = []
        for s in phase2_signals:
            if s.key_metrics:
                if "red_flags" in s.key_metrics:
                    key_risks.extend(s.key_metrics["red_flags"])
        if not key_risks:
            key_risks = ["Market volatility", "Cryptocurrency risk"] if is_crypto else ["Market volatility", "Sector uncertainty"]
        key_risks = list(set(key_risks))[:5]
        
        # Recommendation
        if final_signal == "bullish" and final_conf > 70:
            recommendation = "Consider 5-10% position size"
        elif final_signal == "bullish":
            recommendation = "Consider 3-5% position size"
        elif final_signal == "neutral":
            recommendation = "Watchlist candidate, no position"
        else:
            recommendation = "Avoid or reduce position"
        
        # Build enhanced_data output
        enhanced_data_dict = self._build_crypto_data_output(crypto_data) if is_crypto else self._build_enhanced_data_output(enhanced_data)
        
        return ConsensusResult(
            ticker=ticker,
            signal=final_signal,
            confidence=final_conf,
            agreement=f"{bullish}/{total_investors} bullish, {bearish}/{total_investors} bearish",
            agent_signals=all_signals,
            key_risks=key_risks,
            recommendation=recommendation,
            analysis_date=datetime.now().isoformat(),
            enhanced_data=enhanced_data_dict
        )
    
    def _is_crypto_ticker(self, ticker: str) -> bool:
        """判断是否是数字货币 ticker"""
        crypto_patterns = ['-USDT', '-BTC', '-ETH', '-USD', 'BTC', 'ETH']
        ticker_upper = ticker.upper()
        return any(pattern in ticker_upper for pattern in crypto_patterns)
    
    def _convert_crypto_to_data_dict(self, crypto_data: Dict) -> Dict:
        """将 OKX 数据转换为统一格式"""
        return {
            "current_price": crypto_data.get("current_price", 0),
            "pe_ratio": 0,  # Crypto 没有 P/E
            "pb_ratio": 0,  # Crypto 没有 P/B
            "beta": crypto_data.get("beta", 1.5),  # Crypto 高 beta
            "roe": 0,  # Crypto 没有 ROE
            "roic": 0,
            "debt_to_equity": 0,
            "operating_margin": 0,
            "current_ratio": 0,
            "sector": "Cryptocurrency",
            "industry": "Digital Assets",
            "market_cap": 0,
            "avg_50": crypto_data.get("MA50", 0) if crypto_data.get("MA50") else crypto_data.get("MA20", 0),
            "avg_200": crypto_data.get("MA200", 0) if crypto_data.get("MA200") else 0,
            "rsi": crypto_data.get("RSI", 50),
            "macd": crypto_data.get("MACD", 0),
            "signal_line": crypto_data.get("MACD_Signal", 0),
            "volume": crypto_data.get("volume", 0),
            "avg_volume": crypto_data.get("volume_ma5", 0),
            "high_52w": crypto_data.get("high_24h", 0),
            "low_52w": crypto_data.get("low_24h", 0),
            # Crypto 特有字段
            "atr": crypto_data.get("ATR", 0),
            "atr_percent": crypto_data.get("atr_percent", 5),
            "trend_direction": crypto_data.get("trend_direction", "neutral"),
            "ma_cross_gold": crypto_data.get("ma_cross_gold", False),
            "ma_cross_death": crypto_data.get("ma_cross_death", False),
            "volatility_20d": crypto_data.get("volatility_20d", 0),
            "change_24h_pct": crypto_data.get("change_24h_pct", 0),
            "volume_ratio": crypto_data.get("volume_ratio", 1),
            # Technical Analyst 需要的字段
            "ma_20": crypto_data.get("MA20", 0),
            "ma_50": crypto_data.get("MA50", 0),
            "high": crypto_data.get("high_price", 0),
            "low": crypto_data.get("low_price", 0),
            "close": crypto_data.get("current_price", 0),
            # Risk Manager 需要的字段
            "beta": crypto_data.get("beta", 1.5),
            # Futures masters 需要的字段
            "breakout_20d_high": crypto_data.get("current_price", 0) > crypto_data.get("resistance_20d", 0) if crypto_data.get("resistance_20d") else False,
            "breakout_20d_low": crypto_data.get("current_price", 0) < crypto_data.get("support_20d", 0) if crypto_data.get("support_20d") else False,
        }
    
    def _convert_stock_to_data_dict(self, enhanced_data) -> Dict:
        """将 Yahoo Finance 数据转换为统一格式"""
        return {
            "current_price": enhanced_data.current_price,
            "pe_ratio": enhanced_data.pe_ratio,
            "pb_ratio": enhanced_data.pb_ratio,
            "beta": enhanced_data.beta,
            "roe": enhanced_data.roe,
            "roic": enhanced_data.roe,
            "debt_to_equity": enhanced_data.debt_to_equity,
            "operating_margin": enhanced_data.operating_margin,
            "current_ratio": enhanced_data.current_ratio,
            "sector": enhanced_data.sector,
            "industry": enhanced_data.industry,
            "market_cap": enhanced_data.market_cap,
            "avg_50": enhanced_data.avg_50,
            "avg_200": enhanced_data.avg_200,
            "rsi": enhanced_data.rsi,
            "macd": getattr(enhanced_data, 'macd', None),
            "signal_line": getattr(enhanced_data, 'signal_line', None),
            "volume": getattr(enhanced_data, 'volume', None),
            "avg_volume": getattr(enhanced_data, 'avg_volume', None),
            "high_52w": getattr(enhanced_data, 'high_52w', None),
            "low_52w": getattr(enhanced_data, 'low_52w', None),
        }
    
    def _create_crypto_enhanced_signal(self, crypto_data: Dict) -> AgentSignal:
        """为 Crypto 创建简化版的增强分析信号"""
        signals = []
        score = 50
        
        # 趋势信号
        trend = crypto_data.get("trend_direction", "neutral")
        if trend == "up":
            score += 20
            signals.append("上升趋势")
        elif trend == "down":
            score -= 20
            signals.append("下降趋势")
        
        # RSI 信号
        rsi = crypto_data.get("RSI", 50)
        if rsi > 70:
            score -= 10
            signals.append("RSI 超买")
        elif rsi < 30:
            score += 10
            signals.append("RSI 超卖")
        
        # 成交量信号
        vol_ratio = crypto_data.get("volume_ratio", 1)
        if vol_ratio > 1.5:
            score += 10
            signals.append("成交量放大")
        
        # MACD 信号
        macd_hist = crypto_data.get("MACD_Hist", 0)
        if macd_hist > 0:
            score += 10
            signals.append("MACD 正向")
        else:
            score -= 10
            signals.append("MACD 负向")
        
        signal = "bullish" if score >= 60 else "bearish" if score <= 40 else "neutral"
        
        return AgentSignal(
            agent_name="Crypto Market Analyst",
            signal=signal,
            confidence=abs(score - 50) + 50,
            reasoning="; ".join(signals) if signals else "Neutral market conditions",
            key_metrics={
                "rsi": rsi,
                "trend": trend,
                "volume_ratio": vol_ratio,
                "change_24h": crypto_data.get("change_24h_pct", 0)
            }
        )
    
    def _build_crypto_data_output(self, crypto_data: Dict) -> Dict:
        """构建 Crypto 数据输出"""
        return {
            "asset_type": "crypto",
            "exchange": "OKX",
            "symbol": crypto_data.get("symbol", ""),
            "current_price": crypto_data.get("current_price", 0),
            "change_24h_pct": crypto_data.get("change_24h_pct", 0),
            "high_24h": crypto_data.get("high_24h", 0),
            "low_24h": crypto_data.get("low_24h", 0),
            "volume_24h": crypto_data.get("volume", 0),
            "RSI": crypto_data.get("RSI", 0),
            "MACD": crypto_data.get("MACD", 0),
            "MACD_Hist": crypto_data.get("MACD_Hist", 0),
            "trend": crypto_data.get("trend_direction", "neutral"),
            "ATR": crypto_data.get("ATR", 0),
            "atr_percent": crypto_data.get("atr_percent", 0),
            "MA20": crypto_data.get("MA20", 0),
            "MA50": crypto_data.get("MA50", 0),
            "volatility_20d": crypto_data.get("volatility_20d", 0),
        }

    def _compile_phase1_summary(self, phase1_signals: List, enhanced_data, is_crypto: bool = False, crypto_data: Dict = None) -> Dict:
        """
        编译 Phase 1 分析结果，供投资大师参考
        
        Phase 1 组成:
        - Technical Analyst: 技术分析 (RSI, MACD, 均线, 成交量)
        - Risk Manager: 风险评估 (Beta, 波动率, 仓位建议)
        - Enhanced Agents: 基本面分析 (5位)
        """
        summary = {
            "technical_overall": "neutral",
            "technical_confidence": 50,
            "technical_reasoning": "",
            "risk_signal": "neutral",
            "risk_confidence": 50,
            "risk_score": 50,  # 0-100, 50=中等风险
            "beta": None,
            "risk_factors": [],  # 风险因素列表
            "position_sizing": "medium",  # 建议仓位: small/medium/large
            "earnings_signal": "neutral",
            "analyst_signal": "neutral",
            "macro_signal": "neutral",
            "dividend_signal": "neutral",
            "financial_health_signal": "neutral",
            "summary_text": "",
        }
        
        # Parse Phase 1 signals
        signal_map = {}
        for sig in phase1_signals:
            signal_map[sig.agent_name.lower()] = sig
        
        # Technical Analyst summary
        if "technical analyst" in signal_map:
            ts = signal_map["technical analyst"]
            summary["technical_overall"] = ts.signal
            summary["technical_confidence"] = ts.confidence
            summary["technical_reasoning"] = ts.reasoning
        
        # Risk Manager summary (核心职责)
        if "risk manager" in signal_map:
            rm = signal_map["risk manager"]
            summary["risk_signal"] = rm.signal
            summary["risk_confidence"] = rm.confidence
            summary["risk_score"] = rm.confidence  # 50-100, 越高风险越大
            
            # 提取风险因素
            if rm.key_metrics and "risks" in rm.key_metrics:
                summary["risk_factors"] = rm.key_metrics["risks"]
            
            # 提取 Beta
            if rm.key_metrics and "beta" in rm.key_metrics:
                summary["beta"] = rm.key_metrics["beta"]
            
            # 仓位建议 (根据风险评分)
            risk_score = summary["risk_score"]
            if risk_score < 40:
                summary["position_sizing"] = "large"  # 低风险可以大仓位
            elif risk_score < 55:
                summary["position_sizing"] = "medium"  # 中等风险
            elif risk_score < 70:
                summary["position_sizing"] = "small"  # 高风险小仓位
            else:
                summary["position_sizing"] = "very_small"  # 极高风险
        
        # Earnings
        if "earnings analyst" in signal_map or "earnings" in signal_map:
            key = "earnings analyst" if "earnings analyst" in signal_map else "earnings"
            summary["earnings_signal"] = signal_map[key].signal
        
        # Analyst consensus
        if "wall street consensus" in signal_map:
            summary["analyst_signal"] = signal_map["wall street consensus"].signal
        
        # Macro
        if "macro strategist" in signal_map:
            summary["macro_signal"] = signal_map["macro strategist"].signal
        
        # Dividend
        if "dividend investor" in signal_map:
            summary["dividend_signal"] = signal_map["dividend investor"].signal
        
        # Financial health
        if "financial health analyst" in signal_map:
            summary["financial_health_signal"] = signal_map["financial health analyst"].signal
        
        # Generate comprehensive summary text
        tech = summary["technical_overall"]
        risk = summary["risk_signal"]
        risk_score = summary["risk_score"]
        beta = summary["beta"]
        earn = summary["earnings_signal"]
        analyst = summary["analyst_signal"]
        macro = summary["macro_signal"]
        fin = summary["financial_health_signal"]
        
        beta_str = f"Beta={beta:.1f}" if beta else "Beta=N/A"
        summary["summary_text"] = (
            f"Tech: {tech} | Risk: {risk}({risk_score}) {beta_str} | "
            f"Earnings: {earn} | Analyst: {analyst} | "
            f"Macro: {macro} | Financial: {fin}"
        )
        
        return summary
    
    def _build_enhanced_data_output(self, enhanced_data) -> Dict:
        """构建增强数据输出字典"""
        return {
            "earnings": {
                "actual_eps": getattr(enhanced_data.earnings, 'actual_eps', None),
                "expected_eps": getattr(enhanced_data.earnings, 'expected_eps', None),
                "surprise_pct": getattr(enhanced_data.earnings, 'surprise_pct', None),
                "beats_last_4q": getattr(enhanced_data.earnings, 'beats_last_4q', None),
            },
            "analyst": {
                "consensus": getattr(enhanced_data.analyst, 'consensus_rating', None),
                "num_analysts": getattr(enhanced_data.analyst, 'num_analysts', None),
                "price_target": getattr(enhanced_data.analyst, 'price_target', None),
                "upside_pct": getattr(enhanced_data.analyst, 'upside_pct', None),
            },
            "dividend": {
                "yield_pct": getattr(enhanced_data.dividend, 'yield_pct', 0) or 0,
                "payout_ratio": getattr(enhanced_data.dividend, 'payout_ratio', None),
                "payout_status": getattr(enhanced_data.dividend, 'payout_status', None),
                "income_rating": getattr(enhanced_data.dividend, 'income_rating', None),
            },
            "macro": {
                "vix": getattr(enhanced_data.macro, 'vix_level', None),
                "vix_status": getattr(enhanced_data.macro, 'vix_status', None),
                "market_regime": getattr(enhanced_data.macro, 'market_regime', None),
                "spy_trend_10d": getattr(enhanced_data.macro, 'spy_trend_10d', None),
            },
            "financials": {
                "operating_margin": getattr(enhanced_data.financials, 'operating_margin', None),
                "gross_margin": getattr(enhanced_data.financials, 'gross_margin', None),
                "debt_to_equity": getattr(enhanced_data.financials, 'debt_to_equity', None),
                "return_on_equity": getattr(enhanced_data.financials, 'return_on_equity', None),
                "return_on_assets": getattr(enhanced_data.financials, 'return_on_assets', None),
                "free_cash_flow": getattr(enhanced_data.financials, 'free_cash_flow', None),
                "revenue_growth_yoy": getattr(enhanced_data.financials, 'revenue_growth_yoy', None),
                "financial_health_score": getattr(enhanced_data.financials, 'financial_health_score', None),
            },
            "sector": enhanced_data.sector,
            "industry": enhanced_data.industry,
        }


def format_output(result: ConsensusResult, detailed: bool = False) -> str:
    """Format analysis result for display"""
    lines = []
    
    # Header
    signal_emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}[result.signal]
    lines.append(f"\n{'='*70}")
    lines.append(f"{signal_emoji} {result.ticker} Analysis - {result.signal.upper()} ({result.confidence}% confidence)")
    lines.append(f"{'='*70}")
    lines.append(f"Agreement: {result.agreement}")
    date_str = result.analysis_date[:10] if result.analysis_date else "N/A"
    lines.append(f"Date: {date_str}")
    lines.append("")
    
    # Enhanced Data Summary
    if result.enhanced_data:
        lines.append("📊 Enhanced Data Summary:")
        lines.append("-" * 40)
        
        # Earnings
        earnings = result.enhanced_data.get("earnings", {})
        if earnings.get("surprise_pct") is not None:
            surprise = earnings["surprise_pct"]
            emoji = "📈" if surprise > 0 else "📉"
            lines.append(f"  {emoji} Earnings Surprise: {surprise:+.1f}%")
        if earnings.get("beats_last_4q") is not None:
            lines.append(f"  📊 Beat Rate: {earnings['beats_last_4q']}/4 quarters")
        
        # Analyst
        analyst = result.enhanced_data.get("analyst", {})
        if analyst.get("num_analysts", 0) > 0:
            lines.append(f"  🎯 Analysts: {analyst['num_analysts']} | Consensus: {analyst.get('consensus', 'N/A')}")
        if analyst.get("upside_pct") is not None:
            upside = analyst["upside_pct"]
            emoji = "🚀" if upside > 10 else "📊" if upside > 0 else "⚠️"
            lines.append(f"  {emoji} Upside to Target: {upside:+.1f}%")
        
        # Dividend
        dividend = result.enhanced_data.get("dividend", {})
        if dividend.get("yield_pct") is not None and dividend.get("yield_pct") > 0:
            lines.append(f"  💰 Dividend: {dividend['yield_pct']:.2f}% ({dividend.get('income_rating', 'N/A')})")
        else:
            lines.append(f"  💰 Dividend: None (no dividend)")
        
        # Macro
        macro = result.enhanced_data.get("macro", {})
        if macro.get("vix"):
            vix_status = macro.get("vix_status", "unknown")
            emoji = {"calm": "😌", "elevated": "😐", "fear": "😰", "panic": "😱"}.get(vix_status, "❓")
            lines.append(f"  {emoji} VIX: {macro['vix']:.1f} ({vix_status})")
        if macro.get("market_regime"):
            lines.append(f"  📈 Market: {macro['market_regime'].upper()}")
        
        # Financial Metrics (NEW)
        financials = result.enhanced_data.get("financials", {})
        if financials:
            lines.append("")
            lines.append("  📈 Financial Health:")
            
            # Health and Innovation Scores
            if financials.get("financial_health_score") is not None:
                score = financials['financial_health_score']
                score_emoji = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
                lines.append(f"    {score_emoji} Health Score: {score}/100")
            
            if financials.get("innovation_score") is not None:
                innov = financials['innovation_score']
                innov_emoji = "🟢" if innov >= 70 else "🟡" if innov >= 50 else "🔴"
                lines.append(f"    {innov_emoji} Innovation Score: {innov}/100")
            
            lines.append("")
            
            # Profitability
            lines.append("    💰 Profitability (TTM - 过去12个月):")
            if financials.get("operating_margin") is not None:
                lines.append(f"      • Operating Margin: {financials['operating_margin']:.1f}%")
            if financials.get("gross_margin") is not None:
                lines.append(f"      • Gross Margin: {financials['gross_margin']:.1f}%")
            if financials.get("return_on_equity") is not None:
                roe = financials['return_on_equity']
                roa = financials.get('return_on_assets')
                if roa and roa > 0 and roe / roa > 5:
                    lines.append(f"      🔴 ROE: {roe:.1f}% (TTM) - 高杠杆驱动，非经营质量！")
                    lines.append(f"      ⚠️  ROA: {roa:.1f}% - 真实盈利能力一般")
                    lines.append(f"      📊 杠杆倍数: {roe/roa:.1f}x (危险高)")
                else:
                    lines.append(f"      • ROE: {roe:.1f}% (TTM)")
            if financials.get("return_on_assets") is not None and (not financials.get("return_on_equity") or financials['return_on_equity'] / financials['return_on_assets'] <= 5):
                lines.append(f"      • ROA: {financials['return_on_assets']:.1f}%")
            
            # Debt & Leverage (with industry context)
            lines.append("    ⚖️  Debt & Leverage:")
            if financials.get("debt_to_equity") is not None:
                de = financials['debt_to_equity']
                sector = result.enhanced_data.get('sector', '')
                industry = result.enhanced_data.get('industry', '')
                
                # Use industry rules for emoji
                try:
                    from industry_rules import evaluate_leverage_in_context
                    leverage_eval = evaluate_leverage_in_context(de, sector, industry)
                    
                    if leverage_eval.get('is_concerning'):
                        debt_emoji = "❌"
                        debt_note = " (过高)"
                    elif leverage_eval.get('note'):
                        debt_emoji = "✅"  # Normal for this industry
                        debt_note = f" ({leverage_eval.get('context', '该行业')}正常)"
                    elif de < 0.5:
                        debt_emoji = "✅"
                        debt_note = ""
                    elif de < 1.0:
                        debt_emoji = "⚠️"
                        debt_note = ""
                    else:
                        debt_emoji = "❌"
                        debt_note = ""
                    
                    lines.append(f"      {debt_emoji} Debt/Equity: {de:.2f}x{debt_note}")
                    
                    if leverage_eval.get('note'):
                        lines.append(f"        ℹ️  {leverage_eval.get('note', '')}")
                except ImportError:
                    debt_emoji = "✅" if de < 0.5 else "⚠️" if de < 1.0 else "❌"
                    lines.append(f"      {debt_emoji} Debt/Equity: {de:.2f}x")
            
            if financials.get("current_ratio") is not None:
                lines.append(f"      • Current Ratio: {financials['current_ratio']:.2f}")
            if financials.get("net_debt") is not None:
                nd = financials['net_debt']
                lines.append(f"      • Net Debt: ${nd:,.0f}M")
            
            # Cash Flow
            lines.append("    💵 Cash Flow (TTM - 过去12个月):")
            if financials.get("free_cash_flow") is not None:
                fcf = financials['free_cash_flow']
                fcf_emoji = "✅" if fcf > 0 else "❌"
                lines.append(f"      {fcf_emoji} Free Cash Flow: ${fcf:,.0f}M (TTM)")
            if financials.get("cash") is not None:
                lines.append(f"      • Cash: ${financials['cash']:,.0f}M (Latest)")
            
            # Innovation Investment
            if financials.get("rd_to_revenue") or financials.get("capex_to_revenue"):
                lines.append("    🔬 Innovation Investment:")
                if financials.get("rd_to_revenue") is not None:
                    lines.append(f"      • R&D: {financials['rd_to_revenue']:.1f}% of revenue")
                if financials.get("rd_expense") is not None:
                    lines.append(f"      • R&D Spend: ${financials['rd_expense']:,.0f}M")
                if financials.get("capex_to_revenue") is not None:
                    lines.append(f"      • CapEx: {financials['capex_to_revenue']:.1f}% of revenue")
            
            # Per Share Metrics
            if financials.get("book_value_per_share") or financials.get("cash_per_share"):
                lines.append("    📊 Per Share:")
                if financials.get("book_value_per_share") is not None:
                    lines.append(f"      • Book Value: ${financials['book_value_per_share']:.2f}")
                if financials.get("cash_per_share") is not None:
                    lines.append(f"      • Cash: ${financials['cash_per_share']:.2f}")
        
        # Data Freshness Warning
        lines.append("")
        lines.append("  ⚠️  数据说明:")
        lines.append("    • ROE、FCF、利润率均为TTM数据(过去12个月)")
        lines.append("    • TTM数据可能跨越不同财年和季度")
        lines.append("    • 如需特定年度数据，请参考公司年报")
        
        # Industry Context Analysis
        try:
            from industry_rules import format_industry_context, get_industry_profile
            industry_text = format_industry_context(result.enhanced_data.get('sector', ''), "")
            if industry_text:
                lines.append(industry_text)
        except ImportError:
            pass
        
        # ROE Quality Warning (with industry context)
        if financials and financials.get('return_on_equity') and financials.get('return_on_assets'):
            roe = financials['return_on_equity']
            roa = financials['return_on_assets']
            leverage_ratio = roe / roa if roa > 0 else 0
            
            # Check if this is a leverage-friendly industry
            is_leverage_friendly = False
            try:
                from industry_rules import get_industry_profile
                profile = get_industry_profile(result.enhanced_data.get('sector', ''), "")
                if profile and profile.leverage_is_good:
                    is_leverage_friendly = True
            except:
                pass
            
            if leverage_ratio > 5:
                lines.append("")
                if is_leverage_friendly:
                    lines.append("  ℹ️  ROE结构分析:")
                    lines.append(f"    • ROE ({roe:.1f}%) / ROA ({roa:.1f}%) = {leverage_ratio:.1f}x")
                    lines.append(f"    • 对于{result.enhanced_data.get('sector', '该行业')}，这是正常的杠杆运用")
                    lines.append("    • 高ROE来自财务杠杆，但在该行业是合理策略")
                else:
                    lines.append("  🚨 重要警告 - ROE质量:")
                    lines.append(f"    • ROE ({roe:.1f}%) 是 ROA ({roa:.1f}%) 的 {leverage_ratio:.1f} 倍")
                    lines.append("    • 说明高ROE主要由债务杠杆驱动")
                    lines.append("    • 这是风险信号，非经营优势！")
        lines.append("")
    
    # Agent details
    if detailed:
        lines.append("📊 Agent Analysis:")
        lines.append("-" * 40)
        for signal in result.agent_signals:
            emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}[signal.signal]
            lines.append(f"{emoji} {signal.agent_name}: {signal.signal} ({signal.confidence}%)")
            lines.append(f"   Reason: {signal.reasoning}")
            lines.append("")
    else:
        lines.append("📊 Agent Signals:")
        for signal in result.agent_signals:
            emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}[signal.signal]
            lines.append(f"  {emoji} {signal.agent_name}: {signal.signal} ({signal.confidence}%)")
        lines.append("")
    
    # Risks (with industry context filtering)
    lines.append("⚠️  Key Risks:")
    
    # Check if this is a leverage-friendly industry
    is_leverage_friendly = False
    leverage_friendly_note = ""
    try:
        from industry_rules import get_industry_profile
        profile = get_industry_profile(result.enhanced_data.get('sector', ''), result.enhanced_data.get('industry', ''))
        if profile and profile.leverage_is_good:
            is_leverage_friendly = True
            leverage_friendly_note = f"Note: High leverage is normal for {profile.name}"
    except:
        pass
    
    filtered_risks = []
    for risk in result.key_risks:
        # Filter out leverage warnings for leverage-friendly industries
        if is_leverage_friendly and ('leverage' in risk.lower() or 'debt' in risk.lower()):
            continue
        filtered_risks.append(risk)
    
    for risk in filtered_risks:
        lines.append(f"  • {risk}")
    
    if is_leverage_friendly and leverage_friendly_note:
        lines.append(f"  ℹ️  {leverage_friendly_note}")
    
    lines.append("")
    
    # Recommendation
    lines.append(f"💡 Recommendation: {result.recommendation}")
    lines.append(f"{'='*70}\n")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI Hedge Fund Stock Analysis - Enhanced Edition")
    parser.add_argument("ticker", help="Stock ticker symbol(s), comma-separated for multiple")
    parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed agent reasoning")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--compare", "-c", action="store_true", help="Compare multiple stocks")
    parser.add_argument("--hot", action="store_true", help="Include trending stocks check")
    parser.add_argument("--rumor", action="store_true", help="Include rumor scanner for this ticker")
    parser.add_argument("--visual", "-v", action="store_true", help="Show financial health visualization")
    parser.add_argument("--dashboard", action="store_true", help="Show full financial dashboard")
    
    args = parser.parse_args()
    
    # Parse tickers
    tickers = [t.strip().upper() for t in args.ticker.split(",")]
    
    # Initialize hedge fund
    hedge_fund = EnhancedAIHedgeFund()
    
    # Run analysis
    if len(tickers) == 1:
        result = hedge_fund.analyze(tickers[0], detailed=args.detailed)
        
        if args.json:
            # Convert to dict for JSON serialization
            result_dict = {
                "ticker": result.ticker,
                "signal": result.signal,
                "confidence": result.confidence,
                "agreement": result.agreement,
                "recommendation": result.recommendation,
                "agent_signals": [
                    {
                        "agent": s.agent_name,
                        "signal": s.signal,
                        "confidence": s.confidence,
                        "reasoning": s.reasoning
                    }
                    for s in result.agent_signals
                ],
                "enhanced_data": result.enhanced_data,
            }
            print(json.dumps(result_dict, indent=2))
        else:
            print(format_output(result, detailed=args.detailed))
            
            # Optional: Financial visualization
            if args.visual or args.dashboard:
                from visualizer import FinancialVisualizer, format_financial_summary
                viz = FinancialVisualizer()
                financials = result.enhanced_data.get("financials", {}) if result.enhanced_data else {}
                
                if financials:
                    if args.dashboard:
                        # Full dashboard
                        print(viz.generate_ascii_health_dashboard(tickers[0], financials))
                        print(viz.generate_radar_summary(tickers[0], financials))
                    else:
                        # Quick visual summary
                        print(viz.generate_ascii_health_dashboard(tickers[0], financials))
            
            # Optional: Hot scanner
            if args.hot:
                from hot_rumor_scanner import HotScanner, format_hot_scanner_results
                scanner = HotScanner()
                hot = scanner.get_hot_stocks()
                print(format_hot_scanner_results(hot))
            
            # Optional: Rumor scanner
            if args.rumor:
                from hot_rumor_scanner import RumorScanner, format_rumor_results
                scanner = RumorScanner()
                rumors = scanner.scan_for_ticker(tickers[0])
                if rumors:
                    print(format_rumor_results({tickers[0]: rumors}))
                else:
                    print(f"\n🔮 No rumors detected for {tickers[0]}\n")
    else:
        # Compare mode
        results = []
        for ticker in tickers:
            result = hedge_fund.analyze(ticker)
            results.append(result)
            print(format_output(result, detailed=False))
        
        # Summary comparison
        print("\n" + "="*70)
        print("📊 COMPARISON SUMMARY")
        print("="*70)
        for r in results:
            emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}[r.signal]
            print(f"{emoji} {r.ticker}: {r.signal.upper()} ({r.confidence}%) - {r.recommendation}")
        
        # Optional: Financial comparison table
        if args.visual or args.dashboard:
            from visualizer import FinancialVisualizer
            viz = FinancialVisualizer()
            
            # Collect financials for all tickers
            all_financials = {}
            for r in results:
                if r.enhanced_data and r.enhanced_data.get("financials"):
                    all_financials[r.ticker] = r.enhanced_data["financials"]
            
            if all_financials:
                print(viz.generate_comparison_table(all_financials))


if __name__ == "__main__":
    main()


# ============================================================
# NEW DISTILLED INVESTOR AGENTS (女娲蒸馏 v2.3)
# ============================================================


class RayDalioAgent(InvestmentAgent):
    """Ray Dalio - All Weather + Risk Parity (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("Ray Dalio", "All Weather Portfolio + Risk Parity")
        self.distilled = RayDalioDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze_portfolio_risk(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning="; ".join(result.get("reasoning", [])),
                key_metrics={
                    "risk_assessment": result.get("risk_assessment", {}),
                    "recommendations": result.get("recommendations", [])
                }
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class BillAckmanAgent(InvestmentAgent):
    """Bill Ackman - High Conviction + Catalyst (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("Bill Ackman", "High Conviction + Catalyst-Driven Activism")
        self.distilled = BillAckmanDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning="; ".join(result.get("reasoning", [])),
                key_metrics=result.get("key_metrics", {})
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class CarlIcahnAgent(InvestmentAgent):
    """Carl Icahn - Activist Investing (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("Carl Icahn", "Activist Investing + Corporate Governance")
        self.distilled = CarlIcahnDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning=f"Activist potential: {result.get('activist_potential', 'unknown')}",
                key_metrics={"catalysts": result.get("catalysts", [])}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class JimSimonsAgent(InvestmentAgent):
    """Jim Simons - Quantitative Trading (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("Jim Simons", "Quantitative Trading + Statistical Arbitrage")
        self.distilled = JimSimonsDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze_market_opportunity(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning=f"Quant approach: {result.get('recommended_approach', 'unknown')}",
                key_metrics={"market_inefficiency": result.get("market_inefficiency_score", 0)}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class StanleyDruckenmillerAgent(InvestmentAgent):
    """Stanley Druckenmiller - Global Macro (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("Stanley Druckenmiller", "Global Macro + Concentrated Bets")
        self.distilled = StanleyDruckenmillerDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning=f"Macro: {result.get('macro_theme', 'unknown')} | {result.get('risk_reward', 'unknown')}",
                key_metrics={"position_recommendation": result.get("position_recommendation", "neutral")}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class KenGriffinAgent(InvestmentAgent):
    """Ken Griffin - Market Neutral + Market Making (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("Ken Griffin", "Market Neutral + Tech-Driven Market Making")
        self.distilled = KenGriffinDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning=f"Strategy: {result.get('strategy_recommendation', 'unknown')}",
                key_metrics=result.get("key_metrics", {})
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class SteveCohenAgent(InvestmentAgent):
    """Steve Cohen - Fundamental Stock Picking (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("Steve Cohen", "Fundamental Stock Picking + Trading Skill")
        self.distilled = SteveCohenDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning=f"Thesis clarity: {result.get('thesis_clarity', 'unknown')}",
                key_metrics=result.get("key_metrics", {})
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class GeorgeSorosAgent(InvestmentAgent):
    """George Soros - Reflexivity Theory (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("George Soros", "Reflexivity + Macro Bets")
        self.distilled = GeorgeSorosDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning=f"Reflexivity score: {result.get('reflexivity_score', 0)} | Trend: {result.get('trend_assessment', 'unknown')}",
                key_metrics={"key_insights": result.get("key_insights", [])}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class MohnishPabraiAgent(InvestmentAgent):
    """Mohnish Pabrai - Deep Value + Margin of Safety (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("Mohnish Pabrai", "Deep Value + Margin of Safety + Imitation")
        self.distilled = MohnishPabraiDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning=f"MOS: {result.get('margin_of_safety', 'unknown')} | {result.get('holding_period_recommendation', 'unknown')}",
                key_metrics=result.get("key_metrics", {})
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class DavidEinhornAgent(InvestmentAgent):
    """David Einhorn - Value-Oriented + Long/Short (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("David Einhorn", "Value-Oriented + Catalyst-Driven")
        self.distilled = DavidEinhornDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning=f"Catalyst: {result.get('catalyst_clarity', 'unknown')}",
                key_metrics=result.get("key_metrics", {})
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class DanielLoebAgent(InvestmentAgent):
    """Daniel Loeb - Activist Investing (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("Daniel Loeb", "Activist Investing + Change Catalyst")
        self.distilled = DanielLoebDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning=f"Activist potential: {result.get('activist_potential', 'unknown')} | Catalyst: {result.get('change_catalyst', 'unknown')}",
                key_metrics={}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class JeffYassAgent(InvestmentAgent):
    """Jeff Yass - Quantitative + Options Mindset (女娲蒸馏版)"""
    
    def __init__(self):
        super().__init__("Jeff Yass", "Quantitative Screening + Tech Focus")
        self.distilled = JeffYassDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning=f"Quant score: {result.get('quant_score', 0)}",
                key_metrics={"options_signals": result.get("options_signals", {})}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")




# ============================================================
# FUTURES TRADING MASTERS (女娲蒸馏 - 新增)
# ============================================================


class RichardDennisAgent(InvestmentAgent):
    """Richard Dennis - Turtle Trading + Trend Following"""
    
    def __init__(self):
        super().__init__("Richard Dennis", "Turtle Trading + Trend Following")
        self.distilled = RichardDennisDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning="; ".join(result.get("reasoning", [])),
                key_metrics={"trend_score": result.get("trend_score", 50), "entry_signals": result.get("entry_signals", [])}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class PaulTudorJonesAgent(InvestmentAgent):
    """Paul Tudor Jones - Macro + Risk Management"""
    
    def __init__(self):
        super().__init__("Paul Tudor Jones", "Macro Analysis + Risk Management")
        self.distilled = PaulTudorJonesDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning="; ".join(result.get("reasoning", [])),
                key_metrics={"macro_signal": result.get("macro_signal", {}), "crash_indicators": result.get("crash_indicators", [])}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class EdSeykotaAgent(InvestmentAgent):
    """Ed Seykota - Trend Following + Computerized Systems"""
    
    def __init__(self):
        super().__init__("Ed Seykota", "Trend Following + Computerized Systems")
        self.distilled = EdSeykotaDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning="; ".join(result.get("reasoning", [])),
                key_metrics={"trend_direction": result.get("trend_direction", "neutral"), "trend_strength": result.get("trend_strength", 50)}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class BruceKovnerAgent(InvestmentAgent):
    """Bruce Kovner - Macro + Technical + Risk Management"""
    
    def __init__(self):
        super().__init__("Bruce Kovner", "Macro + Technical + Risk Management")
        self.distilled = BruceKovnerDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning="; ".join(result.get("reasoning", [])),
                key_metrics={"macro_alignment": result.get("macro_alignment", "neutral"), "entry_quality": result.get("entry_quality", "average")}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class LarryWilliamsAgent(InvestmentAgent):
    """Larry Williams - Overbought/Oversold + Seasonality"""
    
    def __init__(self):
        super().__init__("Larry Williams", "Overbought/Oversold + Seasonality")
        self.distilled = LarryWilliamsDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning="; ".join(result.get("reasoning", [])),
                key_metrics={"williams_r": result.get("williams_r", 0), "overbought_oversold": result.get("overbought_oversold", "neutral")}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class JesseLivermoreAgent(InvestmentAgent):
    """Jesse Livermore - Market Timing + Key Levels"""
    
    def __init__(self):
        super().__init__("Jesse Livermore", "Market Timing + Key Levels")
        self.distilled = JesseLivermoreDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning="; ".join(result.get("reasoning", [])),
                key_metrics={"path_of_least_resistance": result.get("path_of_least_resistance", "neutral"), "market_position": result.get("market_position", "观望")}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


class JimRogersAgent(InvestmentAgent):
    """Jim Rogers - Global Macro + Commodities + Emerging Markets"""
    
    def __init__(self):
        super().__init__("Jim Rogers", "Global Macro + Commodities + Emerging Markets")
        self.distilled = JimRogersDistilled() if ALL_DISTILLED else None
    
    def analyze(self, data: Dict) -> AgentSignal:
        if self.distilled:
            result = self.distilled.analyze(data)
            return AgentSignal(
                agent_name=self.name,
                signal=result["signal"],
                confidence=result["confidence"],
                reasoning="; ".join(result.get("reasoning", [])),
                key_metrics={"macro_regime": result.get("macro_regime", "unknown"), "commodity_signal": result.get("commodity_signal", "neutral")}
            )
        return AgentSignal(self.name, "neutral", 50, "Framework not available")


