# AI Hedge Fund Enhancement Plan

## 从 stock-analysis 学习的功能

### 1. 📊 财报分析模块 (EarningsSurprise)
- EPS beat/miss 分析
- 历史财报表现统计
- 市场对财报反应模式

### 2. 🎯 分析师共识模块 (AnalystSentiment)
- 多位分析师评级汇总
- 目标价 vs 现价
- 上涨空间计算

### 3. 🌍 宏观环境模块 (MarketContext)
- VIX 恐慌指数
- SPY/QQQ 趋势
- 避险资产流动 (黄金、国债、美元)
- 市场环境判断 (bull/bear/choppy)

### 4. 💰 股息分析模块 (DividendAnalysis)
- 股息率
- 派息比率 (安全性)
- 股息增长历史
- 连续加息年数

### 5. 📈 历史模式模块 (HistoricalPatterns)
- 财报超预期频率
- 平均市场反应
- 季节性模式

### 6. 🔥 热门/谣言扫描 (HotScanner/RumorScanner)
- 社交媒体情绪
- 并购传闻
- 内部人交易

## 整合策略

### Phase 1: 核心数据增强
- [x] 财报数据 (earnings_history)
- [x] 分析师数据 (analyst_info)
- [x] 宏观指标 (VIX, SPY, QQQ)
- [x] 股息数据 (dividend_info)

### Phase 2: 新 Agent 加入
- [ ] EarningsAgent - 财报分析师
- [ ] AnalystConsensusAgent - 华尔街共识
- [ ] MacroAgent - 宏观环境
- [ ] DividendAgent - 股息投资者视角

### Phase 3: 增强输出
- [ ] 综合评分卡
- [ ] 风险热力图
- [ ] 多维度雷达图
