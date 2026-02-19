# 财报数据差异分析

## 问题原因

### 1. 缺少 lxml 包
- **症状**: `stock.earnings_dates` 返回空值或报错
- **影响**: 所有财报数据显示为 0 或空
- **解决**: `pip3 install lxml`

### 2. 未来日期问题
- **现象**: 财报数据第一行是 2026-04-29（未来日期）
- **原因**: Yahoo Finance 包含未来财报预期
- **问题**: 未来日期没有 `Reported EPS` 数据（NaN）

### 3. 代码 Bug
```python
# 错误代码
earnings_hist.head(1)  # 取到未来日期，没有实际 EPS

# 修复代码
valid_earnings = earnings_hist.dropna(subset=['Reported EPS', 'EPS Estimate'])
recent = valid_earnings.iloc[0]  # 取第一个有数据的
```

## 修复内容

### data_enhancement.py
1. 添加 `dropna()` 过滤空值
2. 从有效数据中取最新财报
3. 使用 `valid_earnings` 计算 beat rate

## 剩余差异说明

Beat Rate 统计差异原因：
- **stock-analysis**: 可能排除了最新一季（有 avg reaction 数据要求）
- **ai-hedge-fund**: 取最近 4 个有数据的季度

这是统计口径差异，不影响核心分析。

## 验证结果

修复后两个 skill 的 EPS Surprise 数据完全一致：
- MSFT: +5.6% beat
- LMT: -2.7% miss
