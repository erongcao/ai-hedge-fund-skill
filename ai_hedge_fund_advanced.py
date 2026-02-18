#!/usr/bin/env python3
"""
AI Hedge Fund - Advanced Version
Uses OpenClaw sub-agents for parallel analysis by legendary investors
Integrates Alpha Vantage API for high-quality financial data
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Literal, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

@dataclass
class AgentSignal:
    agent_name: str
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int
    reasoning: str
    key_metrics: Optional[Dict] = None

@dataclass
class ConsensusResult:
    ticker: str
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int
    agreement: str
    agent_signals: List[AgentSignal]
    key_risks: List[str]
    recommendation: str
    analysis_date: str
    data_quality: str

class AlphaVantageClient:
    """Alpha Vantage API client"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ALPHA_VANTAGE_API_KEY")
        self.base_url = "https://www.alphavantage.co/query"
        self.cache = {}
    
    def _fetch(self, params: Dict) -> Dict:
        import requests
        cache_key = json.dumps(params, sort_keys=True)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        params["apikey"] = self.api_key
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            data = response.json()
            if "Note" in data and "API call frequency" in data["Note"]:
                print(f"⚠️  API limit: {data['Note']}", file=sys.stderr)
                return {}
            self.cache[cache_key] = data
            return data
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return {}
    
    def get_overview(self, ticker: str) -> Dict:
        return self._fetch({"function": "OVERVIEW", "symbol": ticker})
    
    def get_global_quote(self, ticker: str) -> Dict:
        return self._fetch({"function": "GLOBAL_QUOTE", "symbol": ticker})

class DataFetcher:
    """Unified data fetcher"""
    
    def __init__(self):
        self.alpha = AlphaVantageClient()
        self.use_alpha = bool(os.environ.get("ALPHA_VANTAGE_API_KEY"))
    
    def get_comprehensive_data(self, ticker: str) -> Dict:
        print(f"📊 Fetching data for {ticker}...", file=sys.stderr)
        
        # Try Yahoo Finance first
        yahoo_data = self._get_yahoo_data(ticker)
        
        # Enhance with Alpha Vantage
        if self.use_alpha:
            try:
                overview = self.alpha.get_overview(ticker)
                quote = self.alpha.get_global_quote(ticker)
                
                if overview:
                    yahoo_data.update({
                        "pe_ratio": self._safe_float(overview.get("PERatio")),
                        "pb_ratio": self._safe_float(overview.get("PriceToBookRatio")),
                        "roe": self._safe_float(overview.get("ReturnOnEquityTTM")),
                        "debt_to_equity": self._safe_float(overview.get("DebtToEquityRatio")),
                        "operating_margin": self._safe_float(overview.get("OperatingMarginTTM")),
                        "profit_margin": self._safe_float(overview.get("ProfitMargin")),
                        "beta": self._safe_float(overview.get("Beta")),
                        "forward_pe": self._safe_float(overview.get("ForwardPE")),
                        "peg_ratio": self._safe_float(overview.get("PEGRatio")),
                        "sector": overview.get("Sector"),
                        "industry": overview.get("Industry"),
                        "description": overview.get("Description", "")[:1000],
                    })
                
                if quote and "Global Quote" in quote:
                    q = quote["Global Quote"]
                    yahoo_data["current_price"] = self._safe_float(q.get("05. price"))
                
                yahoo_data["data_source"] = "Alpha Vantage + Yahoo Finance"
            except Exception as e:
                print(f"Alpha Vantage error: {e}", file=sys.stderr)
                yahoo_data["data_source"] = "Yahoo Finance"
        else:
            yahoo_data["data_source"] = "Yahoo Finance"
        
        yahoo_data["fetch_date"] = datetime.now().isoformat()
        return yahoo_data
    
    def _get_yahoo_data(self, ticker: str) -> Dict:
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1y")
            
            price = hist['Close'].iloc[-1] if not hist.empty else None
            avg50 = hist['Close'].rolling(50).mean().iloc[-1] if len(hist) >= 50 else None
            avg200 = hist['Close'].rolling(200).mean().iloc[-1] if len(hist) >= 200 else None
            
            return {
                "ticker": ticker,
                "current_price": price,
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "pb_ratio": info.get("priceToBook"),
                "roe": info.get("returnOnEquity"),
                "debt_to_equity": info.get("debtToEquity"),
                "operating_margin": info.get("operatingMargins"),
                "current_ratio": info.get("currentRatio"),
                "beta": info.get("beta"),
                "avg_50": avg50,
                "avg_200": avg200,
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "business_summary": info.get("longBusinessSummary", "")[:1000],
            }
        except Exception as e:
            print(f"Yahoo error: {e}", file=sys.stderr)
            return {"ticker": ticker}
    
    def _safe_float(self, value) -> Optional[float]:
        if value is None or value == "None" or value == "":
            return None
        try:
            return float(value)
        except:
            return None

class SubAgentRunner:
    """Run agents as OpenClaw sub-agents"""
    
    def __init__(self, model: str = "moonshot/kimi-k2.5"):
        self.model = model
    
    def spawn_agent(self, agent_name: str, philosophy: str, ticker: str, data: Dict) -> AgentSignal:
        prompt = self._build_prompt(agent_name, philosophy, ticker, data)
        
        try:
            result = self._call_openclaw(agent_name, prompt)
            return self._parse_response(agent_name, result)
        except Exception as e:
            print(f"Agent {agent_name} failed: {e}", file=sys.stderr)
            return AgentSignal(agent_name, "neutral", 50, f"Failed: {e}", {})
    
    def _build_prompt(self, agent_name: str, philosophy: str, ticker: str, data: Dict) -> str:
        financials = self._format_data(data)
        return f"""You are {agent_name}, legendary investor.

PHILOSOPHY:
{philosophy}

ANALYZE: {ticker}

DATA:
{financials}

Return ONLY JSON:
{{"signal": "bullish"|"bearish"|"neutral", "confidence": 0-100, "reasoning": "explanation", "keyMetrics": {{}}}}
"""
    
    def _format_data(self, data: Dict) -> str:
        lines = []
        if data.get("current_price"):
            lines.append(f"Price: ${data['current_price']:.2f}")
        if data.get("pe_ratio"):
            lines.append(f"P/E: {data['pe_ratio']:.2f}")
        if data.get("pb_ratio"):
            lines.append(f"P/B: {data['pb_ratio']:.2f}")
        if data.get("roe"):
            lines.append(f"ROE: {data['roe']:.1%}")
        if data.get("debt_to_equity") is not None:
            lines.append(f"D/E: {data['debt_to_equity']:.2f}")
        if data.get("operating_margin"):
            lines.append(f"Op Margin: {data['operating_margin']:.1%}")
        if data.get("beta"):
            lines.append(f"Beta: {data['beta']:.2f}")
        if data.get("sector"):
            lines.append(f"Sector: {data['sector']}")
        desc = data.get("description") or data.get("business_summary")
        if desc:
            lines.append(f"Business: {desc[:200]}...")
        return "\n".join(lines)
    
    def _call_openclaw(self, agent_name: str, prompt: str) -> str:
        """Call OpenClaw via CLI"""
        # Use openclaw CLI to spawn
        cmd = [
            "openclaw", "sessions", "spawn",
            "--task", prompt,
            "--model", self.model,
            "--timeout-seconds", "120",
            "--label", f"hf-{agent_name.lower().replace(' ', '-')[:20]}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=130)
        
        if result.returncode != 0:
            raise RuntimeError(f"OpenClaw error: {result.stderr}")
        
        return result.stdout
    
    def _parse_response(self, agent_name: str, response: str) -> AgentSignal:
        try:
            start = response.find('{')
            end = response.rfind('}')
            if start != -1 and end != -1:
                data = json.loads(response[start:end+1])
                return AgentSignal(
                    agent_name=agent_name,
                    signal=data.get("signal", "neutral"),
                    confidence=data.get("confidence", 50),
                    reasoning=data.get("reasoning", "No reasoning"),
                    key_metrics=data.get("keyMetrics", {})
                )
        except Exception as e:
            print(f"Parse error: {e}", file=sys.stderr)
        
        return AgentSignal(agent_name, "neutral", 50, "Parse failed", {})

# Investment agent definitions
INVESTMENT_AGENTS = [
    {
        "name": "Warren Buffett",
        "philosophy": """Value investing. Key criteria: ROE>15%, Debt/Equity<0.5, Operating Margin>15%, durable moat, margin of safety. Avoid high debt, cyclicals without moats. Quote: "Wonderful companies at fair prices.""",
        "weight": 1.3
    },
    {
        "name": "Charlie Munger", 
        "philosophy": """Rational investing. Focus: Circle of competence, mental models, long-term thinking, quality over price, rational capital allocation. Quote: "Big money is in the waiting.""",
        "weight": 1.2
    },
    {
        "name": "Ben Graham",
        "philosophy": """Deep value. Key: Margin of safety (buy at 2/3 value), P/E<15, P/B<1.5, Current Ratio>2, no earnings deficits. Quote: "Market is voting machine short-term, weighing machine long-term.""",
        "weight": 1.1
    },
    {
        "name": "Michael Burry",
        "philosophy": """Contrarian deep value. Look for: Hidden value, assets below replacement cost, strong balance sheet, catalysts, contrarian views. Quote: "Better certain and make less than hopeful and lose.""",
        "weight": 0.9
    },
    {
        "name": "Cathie Wood",
        "philosophy": """Growth/Innovation. Focus: Disruptive innovation, platform businesses, exponential growth, high gross margins, large TAM. Accept high P/E for true innovators.""",
        "weight": 0.9
    },
    {
        "name": "Peter Lynch",
        "philosophy": """Growth at reasonable price. Key: Understandable business, ten-bagger potential, PEG<1, insider buying. Quote: "Invest in what you know.""",
        "weight": 1.0
    },
    {
        "name": "Technical Analyst",
        "philosophy": """Price action. Key: Trend (50/200 MA), Golden/Death Cross, RSI levels, volume confirmation, support/resistance. Bullish: Price>50MA>200MA, RSI 40-60.""",
        "weight": 0.7
    },
    {
        "name": "Risk Manager",
        "philosophy": """Risk control. Key: Beta analysis, position sizing, max drawdown, liquidity, tail risks. High beta>1.5: smaller positions. Mandate: Never lose money permanently.""",
        "weight": 1.0
    }
]

class AIHedgeFundAdvanced:
    """Advanced AI Hedge Fund with parallel sub-agents"""
    
    def __init__(self, use_subagents: bool = True, model: str = "moonshot/kimi-k2.5"):
        self.data_fetcher = DataFetcher()
        self.use_subagents = use_subagents
        self.model = model
        self.sub_agent_runner = SubAgentRunner(model=model) if use_subagents else None
    
    def analyze(self, ticker: str) -> ConsensusResult:
        print(f"\n🔍 Analyzing {ticker}...", file=sys.stderr)
        print(f"   Model: {self.model}", file=sys.stderr)
        
        # Fetch data
        data = self.data_fetcher.get_comprehensive_data(ticker)
        data_quality = data.get("data_source", "Unknown")
        
        if not data.get("current_price"):
            raise ValueError(f"No data for {ticker}")
        
        # Run agents
        if self.use_subagents and self.sub_agent_runner:
            signals = self._run_subagents(ticker, data)
        else:
            signals = self._run_rules_fallback(ticker, data)
        
        return self._generate_consensus(ticker, signals, data_quality)
    
    def _run_subagents(self, ticker: str, data: Dict) -> List[AgentSignal]:
        signals = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(
                    self.sub_agent_runner.spawn_agent,
                    agent["name"],
                    agent["philosophy"],
                    ticker,
                    data
                ): agent
                for agent in INVESTMENT_AGENTS
            }
            
            for future in as_completed(futures):
                agent = futures[future]
                try:
                    signal = future.result(timeout=130)
                    signals.append(signal)
                    emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}[signal.signal]
                    print(f"   {emoji} {agent['name']}: {signal.signal} ({signal.confidence}%)", file=sys.stderr)
                except Exception as e:
                    print(f"   ❌ {agent['name']}: {e}", file=sys.stderr)
                    signals.append(AgentSignal(agent["name"], "neutral", 50, f"Error: {e}", {}))
        
        return signals
    
    def _run_rules_fallback(self, ticker: str, data: Dict) -> List[AgentSignal]:
        print("   Using rules-based fallback", file=sys.stderr)
        sys.path.insert(0, str(Path(__file__).parent))
        from ai_hedge_fund import WarrenBuffettAgent, BenGrahamAgent, TechnicalAnalyst, RiskManager, CathieWoodAgent
        
        agents = [WarrenBuffettAgent(), BenGrahamAgent(), TechnicalAnalyst(), RiskManager(), CathieWoodAgent()]
        return [agent.analyze(data) for agent in agents]
    
    def _generate_consensus(self, ticker: str, signals: List[AgentSignal], data_quality: str) -> ConsensusResult:
        # Weighted scoring
        weighted_bullish = weighted_bearish = total_weight = 0
        
        for signal in signals:
            agent_config = next((a for a in INVESTMENT_AGENTS if a["name"] == signal.agent_name), {"weight": 1.0})
            weight = agent_config.get("weight", 1.0)
            conf = signal.confidence / 100
            
            if signal.signal == "bullish":
                weighted_bullish += weight * conf
            elif signal.signal == "bearish":
                weighted_bearish += weight * conf
            
            total_weight += weight
        
        bullish_score = weighted_bullish / total_weight if total_weight > 0 else 0
        bearish_score = weighted_bearish / total_weight if total_weight > 0 else 0
        
        if bullish_score > bearish_score and bullish_score > 0.35:
            consensus_signal = "bullish"
            consensus_confidence = min(95, int(bullish_score * 100))
        elif bearish_score > bullish_score and bearish_score > 0.35:
            consensus_signal = "bearish"
            consensus_confidence = min(95, int(bearish_score * 100))
        else:
            consensus_signal = "neutral"
            consensus_confidence = int((1 - abs(bullish_score - bearish_score)) * 50 + 25)
        
        bullish_count = sum(1 for s in signals if s.signal == "bullish")
        bearish_count = sum(1 for s in signals if s.signal == "bearish")
        
        # Collect risks
        risks = []
        for signal in signals:
            if signal.signal in ["bearish", "neutral"] and signal.reasoning:
                risks.append(f"{signal.agent_name}: {signal.reasoning[:50]}...")
        if not risks:
            risks = ["No major risks identified"]
        
        # Recommendation
        if consensus_signal == "bullish" and consensus_confidence > 75:
            recommendation = "Strong buy. Consider 8-12% position."
        elif consensus_signal == "bullish":
            recommendation = "Buy. Consider 5-8% position."
        elif consensus_signal == "neutral":
            recommendation = "Watchlist. Wait for better entry."
        else:
            recommendation = "Avoid or reduce position."
        
        return ConsensusResult(
            ticker=ticker,
            signal=consensus_signal,
            confidence=consensus_confidence,
            agreement=f"{bullish_count}/{len(signals)} bullish, {bearish_count}/{len(signals)} bearish",
            agent_signals=signals,
            key_risks=risks[:5],
            recommendation=recommendation,
            analysis_date=datetime.now().isoformat(),
            data_quality=data_quality
        )

def format_output(result: ConsensusResult, detailed: bool = False) -> str:
    signal_emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}[result.signal]
    lines = [
        f"\n{'='*70}",
        f"{signal_emoji} {result.ticker} Analysis - {result.signal.upper()} ({result.confidence}% confidence)",
        f"{'='*70}",
        f"Agreement: {result.agreement}",
        f"Data: {result.data_quality}",
        f"Date: {result.analysis_date[:10]}",
        ""
    ]
    
    lines.append("📊 Agent Analysis:")
    lines.append("-" * 50)
    for signal in result.agent_signals:
        emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}[signal.signal]
        lines.append(f"{emoji} {signal.agent_name:20} {signal.signal.upper():8} {signal.confidence}%")
        if detailed:
            lines.append(f"   {signal.reasoning}")
            lines.append("")
    
    lines.extend([
        "",
        "⚠️  Key Concerns:",
        *[f"  • {risk}" for risk in result.key_risks],
        "",
        f"💡 {result.recommendation}",
        f"{'='*70}\n"
    ])
    
    return "\n".join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Hedge Fund - Advanced")
    parser.add_argument("ticker", help="Stock ticker(s), comma-separated")
    parser.add_argument("--detailed", "-d", action="store_true")
    parser.add_argument("--json", "-j", action="store_true")
    parser.add_argument("--rules", "-r", action="store_true", help="Use rules-based fallback")
    parser.add_argument("--model", "-m", default="moonshot/kimi-k2.5")
    args = parser.parse_args()
    
    tickers = [t.strip().upper() for t in args.ticker.split(",")]
    hedge_fund = AIHedgeFundAdvanced(use_subagents=not args.rules, model=args.model)
    
    for ticker in tickers:
        try:
            result = hedge_fund.analyze(ticker)
            
            if args.json:
                result_dict = {
                    "ticker": result.ticker,
                    "signal": result.signal,
                    "confidence": result.confidence,
                    "agreement": result.agreement,
                    "recommendation": result.recommendation,
                    "data_quality": result.data_quality,
                    "agents": [
                        {"name": s.agent_name, "signal": s.signal, "confidence": s.confidence, "reasoning": s.reasoning}
                        for s in result.agent_signals
                    ]
                }
                print(json.dumps(result_dict, indent=2))
            else:
                print(format_output(result, detailed=args.detailed))
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
