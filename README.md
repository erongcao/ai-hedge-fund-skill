# AI Hedge Fund Skill V2 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DeFi](https://img.shields.io/badge/DeFi-Ready-green.svg)]()

> **女娲方法论完整版** | 22位投资大师思维框架蒸馏 | 链上链下一体化分析

AI Hedge Fund Skill 是一个基于**投资大师思维框架**的智能投资分析工具。它集成了22位传奇投资者（Buffett、Dalio、Soros、Simons等）的思维模型，通过AI模拟他们的决策过程，生成投资共识报告。

---

## 🎉 V2 重大升级

### 核心升级内容

| 模块 | V1 | V2 女娲版 | 状态 |
|------|-----|-----------|------|
| **大师框架** | 22位基础版本 | 22位完整女娲标准版 | ✅ |
| **能力圈检测** | ❌ 无 | ✅ Circle of Competence | ✅ |
| **实时数据** | ❌ 手动获取 | ✅ WebSocket实时接入 | ✅ |
| **交互CLI** | ❌ 无 | ✅ 一键分析命令 | ✅ |
| **回测引擎** | ❌ 无 | 🚧 历史验证系统 | 🚧 开发中 |
| **自适应权重** | ❌ 固定权重 | 🚧 市场环境动态调整 | 🚧 开发中 |
| **自动更新** | ❌ 静态 | 🚧 大师动态监控 | 🚧 开发中 |
| **投资委员会** | ❌ 无 | ✅ 元技能组合 | ✅ |

### 22位大师完整列表

| 类别 | 大师 | 文件大小 | 质量等级 |
|------|------|---------|----------|
| **标杆级** | Warren Buffett | 56KB | ⭐⭐⭐⭐⭐ |
| **完整级** | Ray Dalio, Ben Graham, Richard Dennis, Jim Simons, George Soros | 30-57KB | ⭐⭐⭐⭐⭐ |
| **标准级** | Cathie Wood, Paul Tudor Jones, Ed Seykota, Bruce Kovner | 6-7KB | ⭐⭐⭐⭐ |
| **基础级** | Stanley Druckenmiller, Carl Icahn, Steve Cohen, Ken Griffin, Mohnish Pabrai, David Einhorn, Daniel Loeb, Jeff Yass, Jesse Livermore, Jim Rogers, Larry Williams | 1-2KB | ⭐⭐⭐ |

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/erongcao/ai-hedge-fund-skill.git
cd ai-hedge-fund-skill

# 安装依赖
pip install -r requirements.txt
```

### 基本用法

```bash
# 分析股票 (使用投资委员会)
python3 hedge_cli.py fund NVDA --masters buffett,wood,dalio

# 分析加密货币
python3 hedge_cli.py fund BTC-USDT --timeframe 4H

# 回测大师策略
python3 hedge_cli.py backtest buffett --start 2020-01 --end 2024-12

# 对比所有大师
python3 hedge_cli.py compare --masters all --period 1Y

# 实时监控
python3 hedge_cli.py watch NVDA,BTC-USDT,ETH-USDT
```

### Python调用

```python
from investment_committee import InvestmentCommittee
from circle_of_competence import get_circle_of_competence

# 创建投资委员会
committee = InvestmentCommittee()

# 分析NVDA
report = committee.analyze("NVDA", masters=["buffett", "wood", "dalio"])
print(f"共识: {report.consensus}")
print(f"建议: {report.recommendation}")

# 检查能力圈
coc = get_circle_of_competence("Warren Buffett")
level, reason, confidence = coc.check({"sector": "Technology"})
```

---

## 📊 核心功能

### 1. 投资委员会模式 (Meta-Skill Composition)

聚合多位大师观点，生成共识报告：

```python
from investment_committee import InvestmentCommittee

committee = InvestmentCommittee()
report = committee.analyze("TSLA", masters=["buffett", "wood", "dalio"])

# 输出：
# 共识: 分歧
# 看多: 2 (Wood, Dalio)
# 看空: 1 (Buffett)
# 建议: 观点分歧，建议观望
```

### 2. 能力圈边界检测 (Circle of Competence)

每位大师都有明确的能力圈边界：

```python
from circle_of_competence import get_circle_of_competence, get_experts_for_sector

# 检查Buffett是否擅长科技股
coc = get_circle_of_competence("Warren Buffett")
level, reason, adj = coc.check({"sector": "Technology"})
# → OUTSIDE (明确回避，除非有护城河)

# 查找科技领域专家
experts = get_experts_for_sector("Technology")
# → ['Cathie Wood', 'Ken Griffin', 'Steve Cohen']
```

### 3. 实时数据接入

WebSocket实时行情，自动缓存：

```python
from realtime_data_feed import create_data_feed

feed = create_data_feed()
feed.start(["NVDA-USDT-SWAP", "BTC-USDT"])

# 获取最新价格
price = feed.get_price("NVDA-USDT-SWAP")
```

### 4. 历史回测引擎

验证大师策略在历史数据上的表现：

```python
from backtest_engine import run_backtest, compare_masters

# 单大师回测
result = run_backtest("buffett", "AAPL", "2020-01", "2024-12")

# 多大师对比
compare_masters(
    ["buffett", "wood", "dalio", "druckenmiller"],
    "NVDA",
    "2020-01",
    "2024-12"
)
```

### 5. 自适应权重系统

根据市场环境动态调整大师权重：

```python
from adaptive_weights import AdaptiveWeightSystem, MarketIndicators

aws = AdaptiveWeightSystem()

# 牛市配置
weights = aws.get_weights(MarketRegime.BULL_GROWTH)
# → Wood: 25%, Druckenmiller: 20%, Dalio: 15%, Buffett: 8%...

# 熊市配置
weights = aws.get_weights(MarketRegime.BEAR_DEFLATION)
# → Buffett: 35%, Graham: 30%, Dalio: 20%, Wood: 5%...
```

### 6. 自动更新机制

监控大师动态，自动更新思维框架：

```bash
# 每日检查更新
python3 auto_updater.py --check

# 查看待审核更新
python3 auto_updater.py --list-pending

# 批准更新
python3 auto_updater.py --approve <update_id>
```

---

## 🧠 女娲方法论标准

每位大师V2版本都包含完整的女娲标准要素：

| 要素 | 说明 |
|------|------|
| **身份卡** | 大师背景、称号、巅峰成就 |
| **心智模型** | 带三重验证的核心思维模型 |
| **决策启发式** | if-then规则 + 反事实用例 |
| **表达DNA** | 句式、词汇、节奏、引用习惯 |
| **反模式** | 绝对不会做的事 |
| **内在张力** | 价值观冲突 |
| **智识谱系** | 影响来源和被影响 |
| **诚实边界** | 明确什么做不到 |
| **能力圈** | Circle of Competence |
| **Agentic Protocol** | 回答工作流 |

---

## 📁 项目结构

```
ai-hedge-fund-skill/
├── *_distilled_v2.py          # 22位大师V2版本
├── circle_of_competence.py     # 能力圈框架
├── investment_committee.py     # 投资委员会/元技能组合
├── realtime_data_feed.py       # 实时数据接入
├── hedge_cli.py                # 交互式CLI
├── backtest_engine.py          # 历史回测引擎
├── adaptive_weights.py         # 自适应权重系统
├── auto_updater.py             # 自动更新机制
├── ai_hedge_fund.py            # 主程序
├── README.md                   # 本文件
├── NUWA_V2_COMPLETION_REPORT.md # V2完成报告
└── requirements.txt            # 依赖列表
```

---

## 💡 使用示例

### 分析实战案例

查看完整分析报告示例：
- [NVDA分析报告](NVDA_ANALYSIS_REPORT_2026-04-12.md)

### 大师思维对比

```python
# 让Buffett和Wood辩论TSLA
from investment_committee import InvestmentCommittee

committee = InvestmentCommittee()
debate = committee.debate("TSLA", "估值是否合理", "buffett", "wood")

print(debate['debate_summary'])
# Buffett观点: 估值过高，缺乏安全边际
# Wood观点: AI自动驾驶潜力巨大，长期看好
```

---

## ⚠️ 风险提示

1. **本工具仅供学习和研究，不构成投资建议**
2. **加密货币市场波动剧烈，请严格控制风险**
3. **大师思维框架基于历史数据，无法预测未来**
4. **任何DeFi协议都有智能合约风险，请自行评估**

---

## 🛠️ 开发计划

- [x] 22位大师V2版本
- [x] 能力圈框架
- [x] 投资委员会模式
- [x] 实时数据接入
- [x] 交互式CLI
- [x] 历史回测引擎
- [x] 自适应权重系统
- [x] 自动更新机制
- [ ] 扩展到50位大师
- [ ] A股/港股支持
- [ ] Web可视化面板
- [ ] 机器学习增强

---

## 🤝 贡献

欢迎提交Issue和PR！

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- 22位投资大师的智慧
- 女娲Skill造人术方法论
- OpenClaw框架支持

---

**免责声明**: 本工具仅供学习参考，不构成投资建议。投资有风险，入市需谨慎。
