---
name: paper-prioritizer
description: 对筛选后的论文排序，推荐优先下载和精读顺序
version: 1.1.0
author: Your Name
triggers:
  - "优先级排序"
  - "排序论文"
  - "推荐下载顺序"
  - "prioritize"
inputs:
  - name: filtered_csv
    type: file
    description: filtered_papers.csv (由paper-filter生成)
    required: true
  - name: research_goal
    type: string
    description: 研究目标描述
    required: true
  - name: output_dir
    type: path
    description: 输出目录
    required: true
outputs:
  - name: priority_csv
    type: file
    description: 含优先级排序的论文列表
  - name: priority_stats_json
    type: file
    description: 分批统计信息
---

# Paper Prioritizer

对筛选后的论文进行排序，推荐优先下载和精读顺序。

## 排序维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 相关性 | 高 | 与研究目标的核心匹配度 |
| 创新性 | 高 | 方法是否新颖有突破 |
| 可复现性 | 中 | 是否包含算法细节和参数 |
| 时效性 | 低 | 发表年份（新近优先） |

## 分批策略

| 批次 | 比例 | 处理方式 |
|------|------|----------|
| 高优先级 | 前 20% | 立即下载PDF，全文精读 |
| 中优先级 | 前 20%-50% | 第二批次，选择性精读 |
| 低优先级 | 后 50% | 仅保留元数据，暂不精读 |

## 执行流程

### Step 1: 读取输入
- 读取 `filtered_papers.csv`
- 获取每篇论文的 seq_id、title、abstract、year 等信息

### Step 2: AI排序
根据研究目标，对论文进行综合排序，考虑：
1. 与研究目标的相关性（最重要）
2. 方法的创新性
3. 是否包含可复现的算法和仿真细节
4. 发表年份（新近优先）

### Step 3: 分配批次
- 前 20%：高优先级（立即精读）
- 20%-50%：中优先级（选择性精读）
- 后 50%：低优先级（暂不精读）

### Step 4: 输出结果

**priority_list.csv** 新增字段：
- `priority_score`：优先级分数
- `batch`：高优先级 / 中优先级 / 低优先级
- `download_order`：推荐下载顺序（1-N）

**priority_stats.json**：各批次统计

## 使用示例

```
/skill paper-prioritizer

输入文件: 02_filtered/filtered_papers.csv
研究目标: 研究GNSS完好性监测算法，重点关注多故障检测与隔离方法
输出目录: 02_filtered
```

## 输入要求

- CSV文件由 `paper-filter` 生成
- 必须包含字段：`seq_id`, `title`, `abstract`, `year`

## 输出文件

```
02_filtered/
├── priority_list.csv      # 含优先级排序的论文列表
└── priority_stats.json    # 分批统计信息
```
