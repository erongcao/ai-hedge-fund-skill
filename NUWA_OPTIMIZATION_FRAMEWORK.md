# 女娲方法论优化框架 - AI Hedge Fund Skill

## 当前状态诊断

### ✅ 已有（22个蒸馏文件）
- 基本的心智模型列表
- 决策启发式
- 反模式
- 诚实边界
- analyze() 方法实现

### ❌ 缺失（女娲标准）
1. **Agentic Protocol**（回答工作流）- 99%缺失
2. **心智模型三重验证**（跨域复现、生成力、自创术语）
3. **表达DNA**（句式、词汇、节奏、幽默）
4. **内在张力**（价值观冲突）
5. **智识谱系**（影响来源）
6. **Phase 2.5/4.5 检查点**（质量验证）

---

## 优化方案（按优先级）

### Phase 1: 高优先级（立即实现）

#### 1.1 添加 Agentic Protocol
每个大师都需要一个 "回答工作流"，定义遇到问题时如何分析：

```python
# 示例：Buffett 的 Agentic Protocol
AGENTIC_PROTOCOL = {
    "step1_question_classification": {
        "needs_facts": ["具体公司分析", "财务数据评估"],
        "pure_framework": ["投资哲学", "人生建议"],
        "mixed": ["用案例说明抽象概念"]
    },
    "step2_research": {
        "if_company": [
            "查护城河来源（品牌/成本/网络效应）",
            "查ROE历史（10年以上）",
            "查管理层持股",
            "查债务水平"
        ],
        "tools": ["WebSearch", "FinancialData"]
    },
    "step3_response": "基于事实，用Buffett风格输出"
}
```

#### 1.2 补充心智模型验证
每个心智模型需要：
- ✅ 名称 + 一句话描述
- ✅ 来源证据（≥2个场景）
- ❌ 跨域复现（在≥2个不同领域出现？）
- ❌ 生成力（能推断此人对新问题的立场？）
- ❌ 排他性（不是所有聪明人都这样想？）

#### 1.3 添加能力圈硬边界
已在 `circle_of_competence.py` 实现，需要集成到每个大师。

---

### Phase 2: 中优先级（体验优化）

#### 2.1 表达DNA细化
当前只有"风格描述"，需要具体规则：

| 维度 | 当前 | 优化后 |
|------|------|--------|
| 句式 | "简洁直接" | "短句为主，每句<15字，多用句号" |
| 词汇 | "价值投资术语" | "护城河、安全边际、能力圈、内在价值" |
| 确定性 | "自信" | "用'显然'、'很明显'开头，少用'可能'" |
| 引用 | "不引用" | "喜欢用具体公司案例（Coke、See's）" |

#### 2.2 添加智识谱系
```python
INTELLECTUAL_LINEAGE = {
    "influenced_by": ["Ben Graham", "Phil Fisher"],
    "influenced": ["Mohnish Pabrai", "Terry Smith"],
    "intellectual_siblings": ["Charlie Munger"],
    "opposite_school": ["Efficient Market Hypothesis"]
}
```

#### 2.3 内在张力
每个大师的价值观冲突：
- **Buffett**: "长期持有" vs "机会成本"（为什么不卖Coke？）
- **Dalio**: "分散化" vs "alpha追求"
- **Ackman**: "高置信度" vs "Valeant教训"

---

### Phase 3: 低优先级（长期价值）

#### 3.1 版本追踪
```python
VERSION_HISTORY = [
    {"version": "1.0", "date": "2024-01", "focus": "核心框架"},
    {"version": "2.0", "date": "2026-04", "focus": "加入OKX支持"},
    # 未来更新...
]
```

#### 3.2 Meta-Skill组合
```python
# 投资委员会模式
class InvestmentCommittee:
    def __init__(self, masters: List[str]):
        self.masters = [load_distilled(m) for m in masters]
    
    def debate(self, ticker: str) -> ConsensusReport:
        # 让多个大师辩论
        # 生成"多方观点汇总"
```

#### 3.3 回测验证
```python
# 用历史数据验证
BACKTEST_CASES = [
    {"date": "2008-09", "event": "Lehman破产", "expected_signal": "bearish"},
    {"date": "2020-03", "event": "COVID崩盘", "expected_signal": "buy_opportunity"},
]
```

---

## 实施计划

### 方案A：全面重写（推荐）
用女娲skill重新蒸馏22位大师，生成符合完整标准的skill。

**时间**: 2-3天
**质量**: 最高
**风险**: 可能引入新问题

### 方案B：增量优化（稳妥）
在现有文件基础上，逐项补充缺失内容。

**时间**: 1天
**质量**: 中等
**风险**: 低

### 方案C：重点突破（快速）
只优化最常用的5位大师（Buffett, Dalio, Graham, Wood, Soros）。

**时间**: 半天
**质量**: 核心大师最优
**风险**: 最低

---

## 建议

鉴于你已经能正常运行，建议**方案C**：

1. 先优化 **Buffett**（作为标杆）
2. 再优化 **Dalio**（对比不同风格）
3. 再优化 **3位期货交易员**（Dennis, Jones, Seykota）
4. 其余19位保持现状

要我执行哪个方案？
