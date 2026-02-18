# 🤖 AI Hedge Fund Skill

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw/openclaw)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> An AI-powered hedge fund team that simulates legendary investors (Buffett, Munger, Graham, etc.) to analyze stocks and provide investment recommendations using multi-agent consensus.

[中文](#中文介绍) | [English](#introduction)

---

## 📸 Screenshot

```
🔍 Analyzing AAPL...
   Model: moonshot/kimi-k2.5

   📈 Warren Buffett: bullish (78%) - Strong ROE, low debt, wonderful company
   📈 Charlie Munger: bullish (82%) - Rational capital allocation, durable moat
   📈 Ben Graham: neutral (55%) - P/E slightly high but acceptable margin of safety
   📈 Michael Burry: bullish (70%) - Hidden value in services revenue
   📈 Cathie Wood: bullish (85%) - Platform business with innovation
   📈 Technical Analyst: bullish (80%) - Golden cross, strong momentum
   ➡️ Risk Manager: neutral (60%) - Elevated valuation, market concentration

📈 CONSENSUS: BULLISH (73% confidence)
Agreement: 6/7 bullish, 0/7 bearish
Recommendation: Strong buy. Consider 8-12% position.
```

---

<a name="introduction"></a>
## 🌟 Introduction

This OpenClaw skill creates a team of AI agents, each embodying the investment philosophy of famous investors. By combining multiple perspectives, it provides a comprehensive analysis of stocks and helps construct optimized portfolios.

### ✨ Key Features

- **🧠 8 Legendary Investor Agents**
  - Warren Buffett - Value investing
  - Charlie Munger - Rational investing
  - Ben Graham - Deep value
  - Michael Burry - Contrarian value
  - Cathie Wood - Growth/Innovation
  - Peter Lynch - GARP investing
  - Technical Analyst - Price action
  - Risk Manager - Risk control

- **📊 Portfolio Construction**
  - Modern Portfolio Theory (MPT) optimization
  - Mean-variance optimization
  - Risk parity weighting
  - Sector diversification analysis

- **📈 Strategy Backtesting**
  - Historical performance validation
  - Multiple strategies (AI consensus, momentum, value)
  - Benchmark comparison (S&P 500)

- **🔄 Portfolio Monitoring**
  - Automatic drift detection
  - Rebalancing alerts
  - Health score calculation

- **💰 Tax Optimization**
  - Tax-loss harvesting opportunities
  - Wash sale rule detection
  - Year-end tax strategy

- **🌱 ESG Screening**
  - Environmental, Social, Governance scores
  - Controversy detection
  - Portfolio ESG analysis

- **🌍 Global Markets**
  - 15+ international exchanges
  - US, Hong Kong, China A-shares, Japan, Europe, India, etc.
  - Currency conversion

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/erongcao/ai-hedge-fund-skill.git
cd ai-hedge-fund-skill

# Install dependencies
pip3 install yfinance pandas numpy

# Configure API key (optional but recommended)
echo "ALPHA_VANTAGE_API_KEY=your_key_here" > .env
```

### Basic Usage

```bash
# Analyze a single stock
./ai-hedge-fund-cli analyze AAPL

# Detailed analysis
./ai-hedge-fund-cli analyze AAPL --detailed

# Compare multiple stocks
./ai-hedge-fund-cli analyze AAPL,MSFT,GOOGL,TSLA

# JSON output for automation
./ai-hedge-fund-cli analyze TSLA --json
```

### Portfolio Construction

```bash
# Build optimized portfolio
./ai-hedge-fund-cli portfolio AAPL,MSFT,GOOGL,JPM,JNJ --risk moderate

# Conservative portfolio
./ai-hedge-fund-cli portfolio AAPL,MSFT,GOOGL --risk conservative

# Aggressive growth portfolio
./ai-hedge-fund-cli portfolio NVDA,TSLA,COIN --risk aggressive
```

### Strategy Backtesting

```bash
# Backtest AI consensus strategy
./ai-hedge-fund-cli backtest AAPL,MSFT --start 2023-01-01 --end 2024-01-01

# Test momentum strategy
./ai-hedge-fund-cli backtest AAPL,MSFT,GOOGL --start 2023-01-01 --end 2024-01-01 --strategy momentum

# Monthly rebalancing
./ai-hedge-fund-cli backtest AAPL,MSFT --start 2023-01-01 --end 2024-01-01 --rebalance monthly
```

### Global Markets

```bash
# List supported markets
./ai-hedge-fund-cli global list-markets

# Analyze Hong Kong stock (Tencent)
./ai-hedge-fund-cli global analyze --ticker 0700.HK

# Analyze China A-share (Kweichow Moutai)
./ai-hedge-fund-cli global analyze --ticker 600519.SS

# Analyze Japanese stock (Toyota)
./ai-hedge-fund-cli global analyze --ticker 7203.T

# Currency conversion
./ai-hedge-fund-cli global convert --amount 10000 --from-currency CNY
```

---

## 📚 Supported Markets

| Market | Code | Example Ticker | Currency |
|--------|------|----------------|----------|
| United States | US | AAPL, MSFT, TSLA | USD |
| Hong Kong | HK | 0700.HK, 9988.HK | HKD |
| Shanghai | SS | 600519.SS, 000001.SS | CNY |
| Shenzhen | SZ | 000858.SZ, 002594.SZ | CNY |
| Tokyo | T | 7203.T, 9984.T | JPY |
| London | L | SHEL.L, ULVR.L | GBP |
| Frankfurt | DE | SAP.DE, VOW.DE | EUR |
| Paris | PA | TTE.PA, OR.PA | EUR |
| Toronto | TO | RY.TO, ENB.TO | CAD |
| Australia | AU | CBA.AX, BHP.AX | AUD |
| India NSE | NS | RELIANCE.NS, TCS.NS | INR |
| Korea | KS | 005930.KS, 000660.KS | KRW |
| Singapore | SI | D05.SI, O39.SI | SGD |

---

## 🏗️ Architecture

```
User Request
    │
    ▼
┌─────────────────────────────────────┐
│  Unified CLI (ai-hedge-fund-cli)    │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┬─────────┬─────────┐
    │         │         │         │         │
    ▼         ▼         ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Analyze│ │Portfolio│ │Backtest│ │Tax    │ │Global │
│       │ │        │ │       │ │       │ │       │
└───┬───┘ └────┬────┘ └───┬───┘ └───┬───┘ └───┬───┘
    │          │          │         │         │
    └──────────┴────┬─────┴─────────┴─────────┘
                    │
           ┌────────▼────────┐
           │ 8 AI Agents     │
           │ - Buffett       │
           │ - Munger        │
           │ - Graham        │
           │ - Burry         │
           │ - Cathie Wood   │
           │ - Peter Lynch   │
           │ - Technical     │
           │ - Risk Manager  │
           └────────┬────────┘
                    │
           ┌────────▼────────┐
           │  Data Sources   │
           │ - Yahoo Finance │
           │ - Alpha Vantage │
           └─────────────────┘
```

---

## 🛠️ Advanced Features

### Portfolio Rebalancing Monitor

```bash
# Check if portfolio needs rebalancing
./ai-hedge-fund-cli rebalance AAPL:0.3,MSFT:0.2,GOOGL:0.5

# With last rebalance date
./ai-hedge-fund-cli rebalance AAPL:0.3,MSFT:0.2,GOOGL:0.5 --last-rebalanced 2024-01-01
```

### Tax Optimization

```bash
# Analyze tax position
./ai-hedge-fund-cli tax --lots '[
  {"ticker":"AAPL","shares":100,"purchase_date":"2024-01-01","purchase_price":150},
  {"ticker":"MSFT","shares":50,"purchase_date":"2023-06-01","purchase_price":300}
]'

# Year-end tax strategy
./ai-hedge-fund-cli tax --lots lots.json --year-end --target-gains 10000
```

### ESG Screening

```bash
# Screen individual stocks
./ai-hedge-fund-cli esg AAPL,MSFT,XOM,TSLA

# Portfolio ESG analysis
./ai-hedge-fund-cli esg AAPL,MSFT,GOOGL --portfolio --minimum-score 6.0
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the skill directory:

```bash
# Alpha Vantage API Key (free tier available)
ALPHA_VANTAGE_API_KEY=your_key_here

# Optional: Financial Datasets API
FINANCIAL_DATASETS_API_KEY=your_key_here

# Model Configuration
DEFAULT_MODEL=moonshot/kimi-k2.5
```

### Risk Profiles

| Profile | Description | Target Volatility |
|---------|-------------|-------------------|
| Conservative | Capital preservation, steady income | < 15% |
| Moderate | Balanced growth and stability | 15-25% |
| Aggressive | Maximum growth, high volatility | > 25% |

---

## 📖 Documentation

- **[SKILL.md](SKILL.md)** - Complete feature documentation
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[ADVANCED.md](ADVANCED.md)** - Advanced architecture and sub-agent design

---

## 🧪 Example Output

### Stock Analysis

```
================================================================================
🟢 AAPL Analysis - BULLISH (73% confidence)
================================================================================
Agreement: 6/8 bullish, 0/8 bearish

📊 Agent Analysis:
  📈 Warren Buffett: bullish (78%) - Strong ROE, low debt, wonderful company
  📈 Charlie Munger: bullish (82%) - Rational capital allocation, durable moat
  📈 Ben Graham: neutral (55%) - P/E slightly high but acceptable
  📈 Michael Burry: bullish (70%) - Hidden value in services
  📈 Cathie Wood: bullish (85%) - Platform business, innovation leader
  📈 Peter Lynch: bullish (75%) - Understandable business, ten-bagger potential
  📈 Technical Analyst: bullish (80%) - Golden cross, strong momentum
  ➡️ Risk Manager: neutral (60%) - Elevated valuation, market concentration

⚠️  Key Risks:
  • Elevated valuation
  • Market concentration

💡 Recommendation: Strong buy. Consider 8-12% position.
================================================================================
```

### Portfolio Construction

```
================================================================================
📊 Optimized Moderate Portfolio
================================================================================

💼 Recommended Allocation:
------------------------------------------------------------
Ticker     Weight     Signal     Exp Return   Volatility  
------------------------------------------------------------
MSFT          25.0%   BULLISH       8.5%         22.1%
NVDA          20.0%   BULLISH      15.2%         35.8%
JPM           18.0%   BULLISH       7.8%         19.5%
AAPL          15.0%   NEUTRAL       5.5%         24.3%
GOOGL         12.0%   NEUTRAL       6.2%         28.1%

📈 Portfolio Metrics:
  Expected Annual Return:     12.8%
  Expected Volatility:        22.5%
  Sharpe Ratio:                0.39
  Portfolio Beta:              1.05
  Est. Max Drawdown:         -56.3%
  Diversification Score:       78/100
================================================================================
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/ai-hedge-fund-skill.git
cd ai-hedge-fund-skill

# Install development dependencies
pip3 install -r requirements-dev.txt

# Run tests
python3 -m pytest tests/
```

### Adding New Agents

To add a new investment agent:

1. Create agent class in `ai_hedge_fund_advanced.py`
2. Define investment philosophy and criteria
3. Add to `INVESTMENT_AGENTS` list
4. Update documentation

---

## ⚠️ Disclaimer

**This tool is for educational and research purposes only.**

- Not intended for real trading or investment
- No investment advice or guarantees provided
- Creator assumes no liability for financial losses
- Consult a qualified financial advisor for investment decisions
- Past performance does not indicate future results

---

<a name="中文介绍"></a>
## 中文介绍

AI Hedge Fund Skill 是一个基于 OpenClaw 的投资分析工具，模拟巴菲特、芒格、格雷厄姆等投资大师的风格，通过多智能体共识提供股票分析和投资组合建议。

### 主要功能

- **8位投资大师智能体** - 每位都有独特的投资哲学
- **投资组合构建** - 现代投资组合理论(MPT)优化
- **策略回测** - 历史数据验证策略效果
- **再平衡监控** - 自动检测组合偏离并提醒
- **税务优化** - 税损收割和年末策略
- **ESG筛选** - 环境社会治理评分
- **全球市场** - 支持港股、A股、美股等15+交易所

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/erongcao/ai-hedge-fund-skill.git
cd ai-hedge-fund-skill

# 安装依赖
pip3 install yfinance pandas numpy

# 分析股票
./ai-hedge-fund-cli analyze AAPL

# 构建投资组合
./ai-hedge-fund-cli portfolio AAPL,MSFT,GOOGL --risk moderate

# 分析港股
./ai-hedge-fund-cli global analyze --ticker 0700.HK
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund)
- Built for [OpenClaw](https://github.com/openclaw/openclaw)
- Uses [yfinance](https://github.com/ranaroussi/yfinance) for market data
- Powered by [kimi-k2.5](https://www.moonshot.cn/) for AI analysis

---

## 📬 Contact

- GitHub: [@erongcao](https://github.com/erongcao)
- Email: cao_erong@163.com

---

<p align="center">
  <sub>Built with ❤️ by OpenClaw Community</sub>
</p>
