---
name: ai-hedge-fund
description: An AI-powered hedge fund team that simulates legendary investors (Buffett, Munger, Graham, etc.) to analyze stocks and provide investment recommendations using multi-agent consensus.
homepage: https://github.com/virattt/ai-hedge-fund
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["python3", "pip3"] },
        "install":
          [
            {
              "id": "yfinance",
              "kind": "pip",
              "package": "yfinance",
              "bins": [],
              "label": "Install yfinance (Yahoo Finance)",
            },
            {
              "id": "pandas",
              "kind": "pip",
              "package": "pandas",
              "bins": [],
              "label": "Install pandas",
            },
            {
              "id": "numpy",
              "kind": "pip",
              "package": "numpy",
              "bins": [],
              "label": "Install numpy",
            },
          ],
      },
  }
---

# AI Hedge Fund Skill

An AI-powered hedge fund team that simulates legendary investors to analyze stocks and provide investment recommendations.

## Overview

This skill creates a team of AI agents, each embodying the investment philosophy of famous investors:

### Classic Investment Agents (5)
- **Warren Buffett** - Value investing, wonderful companies at fair prices
- **Ben Graham** - Margin of safety, hidden gems
- **Technical Analyst** - Chart patterns and indicators
- **Risk Manager** - Risk metrics and position sizing
- **Cathie Wood** - Innovation and disruption

### Enhanced Analysis Agents (4) - NEW in v2.1
- **Earnings Analyst** - EPS surprises, beat rates, earnings quality
- **Wall Street Consensus** - Analyst ratings, price targets, upside
- **Macro Strategist** - VIX, market regime, SPY/QQQ trends
- **Dividend Investor** - Yield, payout safety, dividend growth

**Total: 9 agents analyzing each stock for comprehensive coverage**

## Quick Start

```bash
# Unified CLI - All features in one command
ai-hedge-fund analyze AAPL
ai-hedge-fund portfolio AAPL,MSFT,GOOGL --risk moderate
ai-hedge-fund backtest AAPL,MSFT --start 2023-01-01 --end 2024-01-01
ai-hedge-fund global analyze --ticker 0700.HK

# Or use individual commands
./ai-hedge-fund AAPL                    # Basic analysis
./portfolio-build AAPL,MSFT,GOOGL       # Portfolio construction
./backtester AAPL,MSFT --start 2023-01-01 --end 2024-01-01  # Backtest
```

## Data Sources

### Free Tier (No API Key Required)
- **Yahoo Finance** - Real-time prices, basic financials (via yfinance)
- AAPL, GOOGL, MSFT, NVDA, TSLA have extended free data

### Optional API Keys (for enhanced data)
```bash
# Add to ~/.openclaw/skills/ai-hedge-fund/.env
FINANCIAL_DATASETS_API_KEY=your_key  # Detailed financial metrics
ALPHA_VANTAGE_API_KEY=your_key       # Alternative data source
```

## Architecture

```
User Request
    │
    ▼
┌─────────────────┐
│  Data Fetcher   │ ← Yahoo Finance / API
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┬────────┐
    ▼         ▼        ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Buffett│ │ Munger│ │Graham │ │Burry  │ │Cathie │ ← Parallel sub-agents
└───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
    │         │         │         │         │
    └─────────┴────┬────┴─────────┴─────────┘
                   │
          ┌────────▼────────┐
          │  Risk Manager   │
          └────────┬────────┘
                   │
          ┌────────▼────────┐
          │Portfolio Manager│ ← Final recommendation
          └─────────────────┘
```

## Agent Details

### Warren Buffett Agent
**Philosophy**: "It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price."

**Analysis Criteria**:
- Return on Equity (ROE) > 15%
- Debt to Equity < 0.5
- Operating Margin > 15%
- Consistent earnings growth
- Durable competitive moat
- Margin of safety calculation

**Signal**: bullish/bearish/neutral with confidence (0-100)

### Charlie Munger Agent
**Philosophy**: "The big money is not in the buying and selling, but in the waiting."

**Analysis Criteria**:
- Mental model checklist
- Rational capital allocation
- Shareholder-friendly management
- Circle of competence
- Long-term thinking

### Ben Graham Agent
**Philosophy**: "In the short run, the market is a voting machine but in the long run, it is a weighing machine."

**Analysis Criteria**:
- Margin of safety (price < intrinsic value * 0.66)
- P/E ratio < 15
- P/B ratio < 1.5
- Current ratio > 2
- No earnings deficit in past 10 years

### Technical Analyst
**Analysis**:
- Moving averages (20, 50, 200 day)
- RSI (Relative Strength Index)
- MACD
- Support/resistance levels
- Volume analysis

### Risk Manager
**Metrics**:
- Volatility (standard deviation)
- Beta vs S&P 500
- Maximum drawdown
- Sharpe ratio
- Position size recommendations

## Enhanced Analysis (NEW in v2.1)

Based on features learned from stock-analysis skill, we've added 4 new agents:

### Earnings Analyst
**Focus**: Earnings surprises and quality
- EPS surprise analysis (actual vs expected)
- Historical beat rate (last 4 quarters)
- Earnings growth trends
- **Example**: "Beat by +5.2%, 3/4 quarters exceeded estimates"

### Wall Street Consensus
**Focus**: Professional analyst opinions
- Consensus rating (strong_buy/buy/hold/sell/strong_sell)
- Number of covering analysts
- Price target vs current price
- Upside/downside potential
- **Example**: "19 analysts, consensus HOLD, +1.2% upside to target"

### Macro Strategist
**Focus**: Market environment context
- VIX level (fear index)
- Market regime (bull/bear/choppy)
- SPY/QQQ 10-day trends
- Risk-off/risk-on indicators
- **Example**: "VIX 19.6 (elevated), choppy market, SPY flat"

### Dividend Investor
**Focus**: Income and dividend safety
- Dividend yield analysis
- Payout ratio safety assessment
- Dividend growth history
- Income rating (excellent/good/moderate/poor)
- **Example**: "2.8% yield, safe payout at 45%, dividend aristocrat"

## Usage Examples

### Basic Analysis
```python
# Single stock
result = ai_hedge_fund.analyze("AAPL")
# Returns: {"signal": "bullish", "confidence": 75, "reasoning": "..."}

# Multiple stocks
results = ai_hedge_fund.analyze(["AAPL", "MSFT", "GOOGL"])
```

### Detailed Report
```json
{
  "ticker": "AAPL",
  "analysis_date": "2025-02-18",
  "agents": {
    "warren_buffett": {
      "signal": "bullish",
      "confidence": 85,
      "reasoning": "Strong ROE of 160%, excellent brand moat, consistent dividend growth"
    },
    "charlie_munger": {
      "signal": "bullish",
      "confidence": 80,
      "reasoning": "Rational capital allocation via buybacks, strong pricing power"
    },
    "ben_graham": {
      "signal": "neutral",
      "confidence": 50,
      "reasoning": "High P/E of 28 exceeds margin of safety threshold"
    },
    "technical": {
      "signal": "bullish",
      "confidence": 70,
      "reasoning": "Price above 200-day MA, RSI at 55 indicates healthy momentum"
    },
    "risk_manager": {
      "signal": "neutral",
      "confidence": 60,
      "reasoning": "Beta 1.2 indicates market correlation, moderate volatility"
    }
  },
  "consensus": {
    "signal": "bullish",
    "confidence": 73,
    "agreement": "4/5 agents bullish",
    "key_risks": ["High valuation", "Market correlation"],
    "recommendation": "Consider position size of 5-8% max"
  }
}
```

## Configuration

### Environment Variables
```bash
# ~/.openclaw/skills/ai-hedge-fund/.env

# LLM Configuration (uses OpenClaw default if not set)
OPENAI_API_KEY=sk-...  # Optional, falls back to kimi-k2.5

# Data Sources
FINANCIAL_DATASETS_API_KEY=...  # Optional, enhances data quality
ALPHA_VANTAGE_API_KEY=...       # Optional, alternative source

# Analysis Settings
MAX_AGENTS=12           # Number of agents to run
PARALLEL_MODE=true      # Run agents in parallel
CACHE_DURATION=3600     # Cache data for 1 hour
```

### Custom Agents

Add your own investment style by creating a new agent file:

```python
# ~/.openclaw/skills/ai-hedge-fund/agents/custom_agent.py

from typing import Literal

class CustomAgentSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: int = Field(description="Confidence 0-100")
    reasoning: str = Field(description="Reasoning for the decision")

def custom_agent(state: AgentState, ticker: str) -> CustomAgentSignal:
    """Your custom analysis logic"""
    # Fetch data
    data = fetch_financial_data(ticker)
    
    # Analyze
    score = analyze_custom_metrics(data)
    
    # Return signal
    return CustomAgentSignal(
        signal="bullish" if score > 70 else "neutral",
        confidence=score,
        reasoning="Your reasoning here"
    )
```

## Limitations & Disclaimers

**⚠️ IMPORTANT**: This tool is for **educational and research purposes only**.

- **Not investment advice**: These are AI simulations, not professional financial advice
- **No guarantee**: Past performance analyzed by AI does not predict future results
- **Data limitations**: Free data sources may have delays or inaccuracies
- **Risk**: Always consult a qualified financial advisor before making investment decisions

## Technical Details

### Multi-Agent Coordination
Uses OpenClaw's `sessions_spawn` to run agents in parallel:

```typescript
// Parallel agent execution
const agentResults = await Promise.all(
  agents.map(agent => 
    sessions_spawn({
      task: `Analyze ${ticker} as ${agent.name}`,
      agentId: 'investment-analyst',
      timeoutSeconds: 60
    })
  )
);
```

### Data Caching
- Financial data cached for 1 hour to reduce API calls
- Agent results cached for same ticker within 30 minutes

### Error Handling
- Graceful fallback if data source unavailable
- Individual agent failures don't block other agents
- Missing data reported in reasoning

## Troubleshooting

### "No data for ticker"
- Check ticker symbol is correct (e.g., "BRK-B" not "BRK.B")
- Try popular tickers first (AAPL, MSFT, GOOGL)
- Some tickers may not be available in free tier

### "API rate limit"
- Wait a few minutes and retry
- Results are cached, so retry is fast
- Consider adding API key for higher limits

### Slow analysis
- First run fetches and caches data
- Subsequent runs use cached data (much faster)
- Use `--quick` flag for essential agents only

## Feature Modules

### 1. Portfolio Construction (`portfolio_constructor.py`)
Modern Portfolio Theory (MPT) optimization:
- Mean-variance optimization
- Risk parity weighting
- Sector diversification analysis
- Sharpe ratio maximization
- Three risk profiles: conservative, moderate, aggressive

```bash
ai-hedge-fund portfolio AAPL,MSFT,GOOGL,JPM,JNJ --risk moderate
```

### 2. Backtesting (`backtester.py`)
Backtest strategies on historical data:
- Multiple strategies: ai_consensus, equal_weight, momentum, value
- Rebalancing schedules: weekly, monthly, quarterly
- Performance metrics: Sharpe, max drawdown, alpha, beta
- Benchmark comparison (S&P 500)
- Trade history tracking

```bash
ai-hedge-fund backtest AAPL,MSFT,GOOGL --start 2023-01-01 --end 2024-01-01 --strategy ai_consensus
```

### 3. Rebalancing Monitor (`rebalance_monitor.py`)
Monitor portfolio drift and generate alerts:
- Weight drift detection
- Signal-based target weights
- Urgency classification (HIGH/MEDIUM/LOW)
- Health score calculation
- Rebalancing schedule generation

```bash
ai-hedge-fund rebalance AAPL:0.3,MSFT:0.2,GOOGL:0.5 --last-rebalanced 2024-01-01
```

### 4. Tax Optimization (`tax_optimizer.py`)
Tax-loss harvesting and optimization:
- Unrealized gain/loss tracking
- Tax-loss harvesting opportunities
- Wash sale rule detection
- Replacement security suggestions
- Year-end tax strategy

```bash
ai-hedge-fund tax --lots '[{"ticker":"AAPL","shares":100,"purchase_date":"2024-01-01","purchase_price":150}]' --year-end
```

### 5. ESG Screening (`esg_screener.py`)
Environmental, Social, Governance screening:
- ESG score calculation (0-10 scale)
- Controversy detection
- Sector comparison
- Exclusion criteria checking
- Portfolio ESG scoring

```bash
ai-hedge-fund esg AAPL,MSFT,XOM,TSLA --portfolio --minimum-score 6.0
```

### 6. Global Markets (`global_markets.py`)
International stock market support:
- Market detection from ticker format
- 15+ global exchanges
- Currency conversion
- Market hours and timezones
- Index tracking

```bash
# List supported markets
ai-hedge-fund global list-markets

# Analyze Hong Kong stock
ai-hedge-fund global analyze --ticker 0700.HK

# Analyze China A-share
ai-hedge-fund global analyze --ticker 600519.SS

# Convert currency
ai-hedge-fund global convert --amount 10000 --from-currency CNY
```

#### Supported Markets
| Market | Code | Example Ticker |
|--------|------|----------------|
| US Stocks | US | AAPL, MSFT |
| Hong Kong | HK | 0700.HK, 9988.HK |
| Shanghai | SS | 600519.SS |
| Shenzhen | SZ | 000858.SZ |
| Tokyo | T | 7203.T |
| London | L | SHEL.L |
| Frankfurt | DE | SAP.DE |
| India NSE | NS | RELIANCE.NS |
| Australia | AU | CBA.AX |
| Korea | KS | 005930.KS |
| Singapore | SI | D05.SI |

## File Structure

```
ai-hedge-fund/
├── SKILL.md                      # This documentation
├── QUICKSTART.md                 # Quick start guide
├── ADVANCED.md                   # Advanced architecture
├── ai_hedge_fund.py             # Basic rule-based analysis
├── ai_hedge_fund_advanced.py    # AI-powered sub-agent analysis
├── portfolio_constructor.py     # Portfolio optimization
├── backtester.py                # Strategy backtesting
├── rebalance_monitor.py         # Rebalancing alerts
├── tax_optimizer.py             # Tax-loss harvesting
├── esg_screener.py              # ESG screening
├── global_markets.py            # Global market support
├── ai-hedge-fund-cli            # Unified CLI
├── ai-hedge-fund                # Basic CLI wrapper
├── ai-hedge-fund-advanced       # Advanced CLI wrapper
├── portfolio-build              # Portfolio CLI wrapper
└── .env                         # API keys
```

## Related Resources

- [Original Project](https://github.com/virattt/ai-hedge-fund)
- [Value Investing](https://www.investopedia.com/terms/v/valueinvesting.asp)
- [Technical Analysis](https://www.investopedia.com/terms/t/technicalanalysis.asp)
- [Modern Portfolio Theory](https://www.investopedia.com/terms/m/modernportfoliotheory.asp)
- [ESG Investing](https://www.investopedia.com/terms/e/environmental-social-and-governance-esg-criteria.asp)

---

**Version**: 2.0.0  
**Author**: OpenClaw Community  
**License**: MIT
