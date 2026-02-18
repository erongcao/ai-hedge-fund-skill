# AI Hedge Fund Skill - 快速上手指南

## 当前状态

✅ **基础版本已完成** (`ai_hedge_fund.py`)
- 5 个投资风格 agent（巴菲特、格雷厄姆、技术分析师、风险管理、Cathie Wood）
- 使用 Yahoo Finance 免费数据
- 规则引擎分析（不需要 API key）
- 已测试可用

⏳ **高级版本** (`ADVANCED.md`)
- 使用 OpenClaw sub-agent 并行执行
- 每个 agent 用 kimi-k2.5 进行推理
- 8+ 投资大师风格
- 需要实现（见下方说明）

---

## 立即使用（基础版本）

### 1. 分析单只股票

```bash
cd ~/.openclaw/workspace/skills/ai-hedge-fund
./ai-hedge-fund AAPL
```

输出示例：
```
============================================================
🟢 AAPL Analysis - BULLISH (68% confidence)
============================================================
Agreement: 3/5 bullish, 1/5 bearish

📊 Agent Signals:
  📈 Warren Buffett: bullish (70%)
  📉 Ben Graham: bearish (10%)
  📈 Technical Analyst: bullish (90%)
  ➡️ Risk Manager: neutral (50%)
  📈 Cathie Wood: bullish (70%)

⚠️  Key Risks:
  • High beta (1.1)
  • Volatile sector: Technology

💡 Recommendation: Consider 3-5% position size
```

### 2. 详细分析

```bash
./ai-hedge-fund TSLA --detailed
```

### 3. 比较多只股票

```bash
./ai-hedge-fund AAPL,MSFT,GOOGL --compare
```

### 4. JSON 输出（用于自动化）

```bash
./ai-hedge-fund NVDA --json > nvda_analysis.json
```

---

## 作为 OpenClaw Skill 使用

### 选项 A：直接调用 Python 脚本

```typescript
// 在 OpenClaw 会话中
const result = await exec({
  command: "cd ~/.openclaw/workspace/skills/ai-hedge-fund && python3 ai_hedge_fund.py AAPL --json"
});

const analysis = JSON.parse(result.stdout);
```

### 选项 B：集成到 WORKSPACE

1. 添加到 `TOOLS.md`：

```markdown
### AI Hedge Fund

**路径**: `~/.openclaw/workspace/skills/ai-hedge-fund/ai-hedge-fund`

**用法**:
```bash
ai-hedge-fund <TICKER> [options]
```

**示例**:
```bash
ai-hedge-fund AAPL --detailed
ai-hedge-fund AAPL,MSFT,GOOGL --compare
ai-hedge-fund TSLA --json
```
```

### 选项 C：创建专用 Tool

```typescript
// 在 OpenClaw config 中添加自定义 tool
{
  "name": "analyze_stock",
  "description": "Analyze a stock using AI hedge fund team",
  "command": "~/.openclaw/workspace/skills/ai-hedge-fund/ai-hedge-fund",
  "args": ["{ticker}", "--json"]
}
```

---

## 升级到高级版本（可选）

如果你想要真正的 AI 驱动分析（每个 agent 用 kimi-k2.5 推理），需要：

### 步骤 1：安装依赖

```bash
pip3 install yfinance pandas numpy
```

### 步骤 2：实现 Sub-Agent 版本

参考 `ADVANCED.md` 中的架构，创建一个 TypeScript 版本：

```typescript
// ai-hedge-fund-advanced.ts
// 使用 sessions_spawn 并行运行每个 agent
```

或者使用 Python + OpenClaw API：

```python
# ai_hedge_fund_advanced.py
# 调用 OpenClaw 的 sessions_spawn
```

### 步骤 3：配置模型

```bash
# 确保使用 kimi-k2.5
export DEFAULT_MODEL=moonshot/kimi-k2.5
```

---

## 数据源说明

### 当前使用：Yahoo Finance（免费）

**优点**:
- 完全免费，无需 API key
- 实时股价
- 基础财务数据

**限制**:
- 某些数据可能延迟
- 高频调用可能受限
- 非官方 API

### 可选升级：Alpha Vantage

1. 获取免费 API key: https://www.alphavantage.co/support/#api-key
2. 添加到 `.env` 文件：

```bash
echo "ALPHA_VANTAGE_API_KEY=your_key_here" > ~/.openclaw/workspace/skills/ai-hedge-fund/.env
```

3. 修改 `ai_hedge_fund.py` 使用 Alpha Vantage

---

## 自定义 Agent

### 添加新的投资风格

编辑 `ai_hedge_fund.py`，添加新类：

```python
class YourCustomAgent(InvestmentAgent):
    def __init__(self):
        super().__init__(
            "Your Name",
            "Your investment philosophy"
        )
    
    def analyze(self, data: Dict) -> AgentSignal:
        # Your analysis logic
        score = 0
        # ... calculate score based on your criteria
        
        return AgentSignal(
            agent_name=self.name,
            signal="bullish" if score > 70 else "neutral",
            confidence=score,
            reasoning="Your reasoning"
        )
```

然后在 `AIHedgeFund.__init__` 中添加：

```python
self.agents = [
    # ... existing agents
    YourCustomAgent(),
]
```

---

## 常见问题

### Q: 为什么某些股票没有数据？

A: 确保使用正确的 ticker 格式：
- ✅ AAPL, MSFT, GOOGL, TSLA, NVDA
- ✅ BRK-B (伯克希尔，注意是连字符)
- ❌ BRK.B (不要用点)

### Q: 分析速度太慢？

A: 第一次运行会获取数据，后续使用缓存。或者使用 `--quick` 模式（需要实现）。

### Q: 如何添加更多 agents？

A: 参考 ADVANCED.md 实现并行 sub-agent 版本，可以扩展到 12+ 个投资大师风格。

### Q: 能用于实际交易吗？

A: ⚠️ **不能**。这只是教育工具。AI 模拟不等于专业投资建议。

---

## 下一步建议

1. **测试基础版本** - 运行几个股票看看效果
2. **调整权重** - 根据你的偏好修改 agent 权重
3. **添加数据源** - 集成 Alpha Vantage 获取更完整数据
4. **实现高级版本** - 用 sub-agent 实现真正的 AI 推理
5. **回测功能** - 验证策略在历史数据上的表现

---

## 文件结构

```
~/.openclaw/workspace/skills/ai-hedge-fund/
├── SKILL.md                    # 完整 skill 文档
├── ai_hedge_fund.py           # 主程序（基础版本）
├── ai-hedge-fund              # Shell wrapper
├── ADVANCED.md                # 高级版本设计文档
├── QUICKSTART.md              # 本文件
└── .env                       # API keys（可选）
```

---

**需要帮助？** 运行 `./ai-hedge-fund --help` 查看所有选项。
