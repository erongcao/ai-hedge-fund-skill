---
name: ai-hedge-fund-advanced
description: Advanced AI Hedge Fund using OpenClaw sub-agents for parallel analysis by legendary investors (Buffett, Munger, Graham, etc.)
---

# AI Hedge Fund - Advanced Version (Using OpenClaw Sub-Agents)

This version uses OpenClaw's `sessions_spawn` to run each investment agent in parallel as sub-agents, with each agent using kimi-k2.5 for reasoning.

## Architecture

```
User Request: "Analyze AAPL"
    │
    ▼
┌─────────────────────────────────────┐
│  Main Agent (Orchestrator)          │
│  - Fetch financial data             │
│  - Spawn sub-agents in parallel     │
│  - Collect results                  │
│  - Generate consensus               │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┬─────────┬─────────┐
    │         │         │         │         │
    ▼         ▼         ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Buffett│ │Munger │ │Graham │ │Tech   │ │Risk   │ ← Sub-agents
│Agent  │ │Agent  │ │Agent  │ │Analyst│ │Mgr    │   (parallel)
└───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
    │         │         │         │         │
    └─────────┴────┬────┴─────────┴─────────┘
                   │
            ┌──────▼──────┐
            │  Consensus  │
            │   Engine    │
            └──────┬──────┘
                   │
            ┌──────▼──────┐
            │  Portfolio  │
            │   Manager   │ ← Final recommendation
            └─────────────┘
```

## Implementation

### 1. Main Orchestrator (TypeScript/OpenClaw)

```typescript
// ai-hedge-fund.ts - Main orchestrator
import { sessions_spawn } from "@openclaw/sessions";

interface AnalysisResult {
  agent: string;
  signal: "bullish" | "bearish" | "neutral";
  confidence: number;
  reasoning: string;
  keyMetrics?: Record<string, any>;
}

const INVESTMENT_AGENTS = [
  {
    name: "Warren Buffett",
    style: "Value investing. Focus on:
      - ROE > 15%
      - Low debt (D/E < 0.5)
      - Operating margins > 15%
      - Durable competitive moat
      - Margin of safety
      - Wonderful companies at fair prices",
    weight: 1.2  // Higher weight for Buffett
  },
  {
    name: "Charlie Munger",
    style: "Rational investing. Focus on:
      - Circle of competence
      - Mental models
      - Long-term thinking
      - Shareholder-friendly management
      - Quality over price",
    weight: 1.1
  },
  {
    name: "Ben Graham",
    style: "Deep value. Focus on:
      - Margin of safety (buy at 66% of value)
      - P/E < 15
      - P/B < 1.5
      - Current ratio > 2
      - No earnings deficits",
    weight: 1.0
  },
  {
    name: "Michael Burry",
    style: "Contrarian deep value. Focus on:
      - Hidden value others miss
      - Balance sheet strength
      - Distressed assets
      - Going against consensus",
    weight: 0.9
  },
  {
    name: "Cathie Wood",
    style: "Growth/Innovation. Focus on:
      - Disruptive innovation
      - Exponential growth potential
      - Platform businesses
      - Long-term winners in tech/biotech",
    weight: 0.9
  },
  {
    name: "Peter Lynch",
    style: "Practical growth. Focus on:
      - Ten-bagger potential
      - Everyday businesses
      - Understandable products
      - Reasonable PEG ratio",
    weight: 1.0
  },
  {
    name: "Technical Analyst",
    style: "Price action. Focus on:
      - Trend (50/200 day MA)
      - RSI momentum
      - Support/resistance
      - Volume patterns
      - Chart patterns",
    weight: 0.7
  },
  {
    name: "Risk Manager",
    style: "Risk control. Focus on:
      - Volatility (beta)
      - Position sizing
      - Correlation
      - Maximum drawdown
      - Tail risks",
    weight: 1.0
  }
];

async function analyzeStock(ticker: string): Promise<AnalysisResult[]> {
  // 1. Fetch financial data (once)
  const financialData = await fetchFinancialData(ticker);
  
  // 2. Spawn sub-agents in parallel
  const agentPromises = INVESTMENT_AGENTS.map(agent => 
    sessions_spawn({
      task: generateAgentPrompt(agent, ticker, financialData),
      model: "moonshot/kimi-k2.5",
      timeoutSeconds: 120,
      label: `agent-${agent.name.toLowerCase().replace(/\\s+/g, '-')}`
    })
  );
  
  // 3. Collect all results
  const results = await Promise.all(agentPromises);
  
  // 4. Parse and validate results
  return results.map((result, index) => ({
    agent: INVESTMENT_AGENTS[index].name,
    ...parseAgentResponse(result),
    weight: INVESTMENT_AGENTS[index].weight
  }));
}

function generateAgentPrompt(agent: any, ticker: string, data: any): string {
  return `
You are ${agent.name}, the legendary investor.

Your Investment Philosophy:
${agent.style}

STOCK TO ANALYZE: ${ticker}

Financial Data:
${JSON.stringify(data, null, 2)}

Analyze this stock according to YOUR specific investment philosophy.
Return ONLY a JSON object in this exact format:

{
  "signal": "bullish" | "bearish" | "neutral",
  "confidence": number (0-100),
  "reasoning": "2-3 sentences explaining your decision based on your philosophy",
  "keyMetrics": {
    "metric1": value,
    "metric2": value
  }
}

Important:
- Think like ${agent.name} would think
- Use YOUR specific criteria, not generic analysis
- Be decisive - avoid neutral unless truly unclear
- Provide specific numbers in your reasoning
`;
}

function parseAgentResponse(response: string): Omit<AnalysisResult, 'agent'> {
  try {
    // Extract JSON from response
    const jsonMatch = response.match(/\\{[\\s\\S]*\\}/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[0]);
    }
  } catch (e) {
    console.error("Failed to parse agent response:", e);
  }
  
  // Fallback
  return {
    signal: "neutral",
    confidence: 50,
    reasoning: "Could not parse response",
    keyMetrics: {}
  };
}

async function generateConsensus(results: AnalysisResult[]): Promise<{
  signal: string;
  confidence: number;
  agreement: string;
  recommendation: string;
}> {
  // Weighted voting
  let weightedBullish = 0;
  let weightedBearish = 0;
  let totalWeight = 0;
  
  for (const result of results) {
    const weight = result.weight || 1;
    const confidenceWeight = result.confidence / 100;
    
    if (result.signal === "bullish") {
      weightedBullish += weight * confidenceWeight;
    } else if (result.signal === "bearish") {
      weightedBearish += weight * confidenceWeight;
    }
    totalWeight += weight;
  }
  
  const bullishScore = weightedBullish / totalWeight;
  const bearishScore = weightedBearish / totalWeight;
  
  let signal: string;
  let confidence: number;
  
  if (bullishScore > bearishScore && bullishScore > 0.4) {
    signal = "bullish";
    confidence = Math.round(bullishScore * 100);
  } else if (bearishScore > bullishScore && bearishScore > 0.4) {
    signal = "bearish";
    confidence = Math.round(bearishScore * 100);
  } else {
    signal = "neutral";
    confidence = Math.round((1 - Math.abs(bullishScore - bearishScore)) * 50 + 25);
  }
  
  const bullishCount = results.filter(r => r.signal === "bullish").length;
  const bearishCount = results.filter(r => r.signal === "bearish").length;
  
  return {
    signal,
    confidence,
    agreement: `${bullishCount}/${results.length} bullish, ${bearishCount}/${results.length} bearish`,
    recommendation: generateRecommendation(signal, confidence, results)
  };
}

function generateRecommendation(
  signal: string, 
  confidence: number, 
  results: AnalysisResult[]
): string {
  const risks = results
    .filter(r => r.signal === "bearish" || r.signal === "neutral")
    .map(r => r.reasoning)
    .slice(0, 3);
  
  if (signal === "bullish" && confidence > 75) {
    return `Strong buy candidate. Consider 8-12% position. Risks: ${risks.join("; ") || "Market volatility"}`;
  } else if (signal === "bullish") {
    return `Buy candidate. Consider 5-8% position. Risks: ${risks.join("; ") || "Standard market risks"}`;
  } else if (signal === "neutral") {
    return `Watchlist candidate. Wait for better entry or clearer thesis.`;
  } else {
    return `Avoid or reduce position. Consider selling if owned.`;
  }
}

// Main execution
export async function main(ticker: string) {
  console.log(`🔍 Analyzing ${ticker} with AI Hedge Fund Team...\\n`);
  
  const results = await analyzeStock(ticker);
  const consensus = await generateConsensus(results);
  
  // Display results
  console.log("📊 AGENT ANALYSIS:");
  console.log("-".repeat(60));
  for (const result of results) {
    const emoji = { bullish: "📈", bearish: "📉", neutral: "➡️" }[result.signal];
    console.log(`${emoji} ${result.agent.padEnd(20)} ${result.signal.toUpperCase().padEnd(8)} ${result.confidence}%`);
    console.log(`   ${result.reasoning}\\n`);
  }
  
  console.log("📈 CONSENSUS:");
  console.log("-".repeat(60));
  const signalEmoji = { bullish: "🟢", bearish: "🔴", neutral: "🟡" }[consensus.signal];
  console.log(`${signalEmoji} Signal: ${consensus.signal.toUpperCase()} (${consensus.confidence}% confidence)`);
  console.log(`🤝 Agreement: ${consensus.agreement}`);
  console.log(`💡 ${consensus.recommendation}\\n`);
  
  return { results, consensus };
}
```

### 2. Data Fetcher Module

```typescript
// data-fetcher.ts
import yfinance from "yfinance";  // or use yfinance Python bridge

interface FinancialData {
  ticker: string;
  currentPrice: number;
  marketCap: number;
  peRatio: number;
  pbRatio: number;
  roe: number;
  debtToEquity: number;
  operatingMargin: number;
  currentRatio: number;
  dividendYield: number;
  beta: number;
  avg50: number;
  avg200: number;
  rsi: number;
  revenue: number;
  netIncome: number;
  freeCashFlow: number;
  sector: string;
  industry: string;
  description: string;
}

export async function fetchFinancialData(ticker: string): Promise<FinancialData> {
  // Option 1: Use yfinance Python bridge
  // Option 2: Use Alpha Vantage API (free tier)
  // Option 3: Use Yahoo Finance API (unofficial)
  
  const response = await fetch(`https://query1.finance.yahoo.com/v8/finance/chart/${ticker}`);
  // ... parse and structure data
  
  return structuredData;
}
```

### 3. Package.json

```json
{
  "name": "ai-hedge-fund-skill",
  "version": "2.0.0",
  "description": "AI Hedge Fund with parallel sub-agents",
  "main": "ai-hedge-fund.ts",
  "scripts": {
    "analyze": "tsx ai-hedge-fund.ts"
  },
  "dependencies": {
    "@openclaw/sdk": "^1.0.0"
  }
}
```

## Usage

```bash
# Basic analysis
ai-hedge-fund-advanced AAPL

# Compare multiple
ai-hedge-fund-advanced AAPL,MSFT,GOOGL --compare

# With custom weights
ai-hedge-fund-advanced TSLA --weights="growth:1.5,value:0.8"

# Output JSON for further processing
ai-hedge-fund-advanced NVDA --json
```

## Data Sources

### Free Options (Recommended)

1. **Yahoo Finance (yfinance)**
   - Real-time prices
   - Historical data
   - Basic financials
   - No API key needed

2. **SEC EDGAR**
   - Official filings
   - Free but requires parsing

3. **Alpha Vantage**
   - 500 calls/day free
   - Good for fundamentals
   - Requires API key

### Paid Options

1. **Financial Datasets AI**
   - AAPL/GOOGL/MSFT/NVDA/TSLA free
   - Others paid
   - High quality data

2. **Polygon.io**
   - Professional-grade
   - Reasonable pricing

## Configuration

```bash
# ~/.openclaw/skills/ai-hedge-fund-advanced/.env

# Data source
PRIMARY_DATA_SOURCE=yahoo  # yahoo | alpha_vantage | financial_datasets
ALPHA_VANTAGE_API_KEY=...
FINANCIAL_DATASETS_API_KEY=...

# LLM configuration
AGENT_MODEL=moonshot/kimi-k2.5
AGENT_TIMEOUT=120
MAX_PARALLEL_AGENTS=8

# Analysis settings
INCLUDE_TECHNICAL=true
INCLUDE_SENTIMENT=true
RISK_FREE_RATE=0.04
MARKET_BENCHMARK=SPY
```

## Performance Optimization

### Caching Strategy

```typescript
// Cache financial data for 1 hour
const cacheKey = `financial_${ticker}_${date}`;
const cached = await cache.get(cacheKey);
if (cached) return cached;

const data = await fetchFinancialData(ticker);
await cache.set(cacheKey, data, 3600);
```

### Parallel Execution

```typescript
// Run data fetch and some agents in parallel
const [financialData, marketData] = await Promise.all([
  fetchFinancialData(ticker),
  fetchMarketContext()
]);

// Then spawn all agents in parallel
const results = await Promise.all(
  agents.map(agent => spawnAgent(agent, financialData))
);
```

## Extending with New Agents

```typescript
// Add custom agent
const customAgent = {
  name: "Your Custom Agent",
  style: `Your specific investment philosophy here
    - Criterion 1
    - Criterion 2
    - Criterion 3`,
  weight: 1.0
};

INVESTMENT_AGENTS.push(customAgent);
```

## Future Enhancements

1. **Backtesting Module**
   - Run agents on historical data
   - Validate strategies
   - Compare performance

2. **Portfolio Construction**
   - Correlation analysis
   - Risk parity allocation
   - Rebalancing suggestions

3. **Sentiment Integration**
   - News analysis
   - Social media sentiment
   - Earnings call sentiment

4. **Real-time Monitoring**
   - Price alerts
   - Agent signal changes
   - Automatic rebalancing

## Disclaimer

⚠️ **For educational purposes only. Not investment advice.**

- AI agents simulate investor styles but may not perfectly replicate decisions
- Past performance does not predict future results
- Always consult a qualified financial advisor
- Test strategies with paper trading before real money

---

**Version**: 2.0.0 (Advanced)  
**Requires**: OpenClaw with sub-agent support  
**Recommended Model**: moonshot/kimi-k2.5
