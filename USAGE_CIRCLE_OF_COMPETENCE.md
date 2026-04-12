# Circle of Competence 使用说明

## 已创建的文件

### 1. `circle_of_competence.py`
定义了 29 位大师的能力圈配置，包括：
- **expert_sectors**: 核心能力圈行业
- **avoid_sectors**: 明确回避的行业  
- **expert_asset_types**: 擅长的资产类型
- **expert_geographies**: 熟悉的地域

## 集成到 ai_hedge_fund.py

在 `ai_hedge_fund.py` 顶部添加导入：

```python
from circle_of_competence import (
    CircleOfCompetence, 
    get_circle_of_competence,
    CompetenceLevel
)
```

## 修改分析流程

在每个投资大师的 `analyze` 方法开头添加：

```python
def analyze(self, data: Dict) -> AgentSignal:
    # 1. 检查能力圈
    coc = get_circle_of_competence(self.name)
    level, reason, confidence_adj = coc.check(data)
    
    if level == CompetenceLevel.OUTSIDE:
        return AgentSignal(
            agent_name=self.name,
            signal="neutral",
            confidence=int(30 * confidence_adj),  # 大幅降低置信度
            reasoning=f"Outside circle of competence: {reason}",
            key_metrics={"circle_of_competence": False}
        )
    
    # 2. 正常分析流程...
```

## 使用示例

```python
from circle_of_competence import check_all_masters, get_experts_for_sector

# 检查所有大师对某个标的的能力圈
data = {"sector": "Technology", "asset_type": "stock"}
results = check_all_masters(data)

# 获取某个行业的专家
experts = get_experts_for_sector("Technology")
# Returns: ['Cathie Wood', 'Ken Griffin', 'Steve Cohen', ...]

# 获取回避某个行业的大师
avoiders = get_avoiders_for_sector("Technology")
# Returns: ['Warren Buffett', 'Ben Graham', 'Mohnish Pabrai']
```

## 测试

```bash
cd ~/.agents/skills/ai-hedge-fund-skill
python3 circle_of_competence.py
```

## 下一步改进

1. **Meta-Skill Composition**: 组合多个大师的观点
2. **CLI 向导**: 交互式配置
3. **版本追踪**: 记录大师观点的演变
4. **回测验证**: 用历史数据验证预测
