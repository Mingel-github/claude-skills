---
name: paper-filter
description: 基于摘要筛选论文，判断是否值得全文阅读
version: 1.2.0
author: Your Name
triggers:
  - "筛选论文"
  - "过滤文献"
  - "filter papers"
inputs:
  - name: metadata_csv
    type: file
    description: papers_metadata.csv (由wos-parser生成)
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
  - name: filtered_csv
    type: file
    description: 筛选后的论文列表（含双序号）
  - name: filter_stats_json
    type: file
    description: 筛选统计JSON
---

# Paper Filter

基于摘要筛选论文，判断是否值得全文阅读。

筛选标准见 `references/filter_criteria.md`。

## 执行流程

### Step 1: 读取输入
- 读取 `papers_metadata.csv`
- 提取每篇论文的 wos_id、seq_id、title、abstract、author_address、doc_type、year
- 读取 `references/filter_criteria.md` 获取用户自定义的排除/优先标准

### Step 2: 分批评估
将论文分成每批20-30篇，对每批执行以下评估：

针对每篇论文，根据四个维度打分（1-5分）：
- **相关性**：与研究目标的匹配程度
- **创新性**：方法/结论是否新颖
- **可复现性**：是否包含足够细节（算法、参数、公式）
- **完整性**：是否有理论分析 + 实验验证

保留标准：综合评分 ≥ 12 分 **且** 相关性 ≥ 3 分

### Step 3: 特殊处理规则

**综述类文章**：
- 仅保留发表于近3-5年的高质量期刊/会议综述
- 标注文献类型为"综述"
- 优先保留覆盖用户关注子方向的综述

**同一团队去重**：
- 基于 author_address 字段识别同一团队（聚焦到学院/实验室级别）
- 同一团队的相似工作只保留最新/最完整的一篇
- 除非各篇有明显不同的技术贡献或解决不同子问题

**自定义排除/包含**：
- 读取 `references/filter_criteria.md` 中的排除和优先标准
- 排除纯应用报告、无方法创新的演示类文章

### Step 4: 输出结果
生成两个文件：

**filtered_papers.csv**（保留的论文）：
- 保留 wos_id 不变
- 重新分配 seq_id（从1开始递增）
- 包含原始所有字段
- 新增 `method_category` 列（方法类别标签）
- 新增 `filter_rationale` 列（筛选理由2-3句）

**filter_stats.json**：
```json
{
  "total": 632,
  "kept": 150,
  "rejected": 482,
  "kept_reviews": 15,
  "deduplicated": 8,
  "avg_scores": {"相关性": 3.8, "创新性": 3.2, ...},
  "details": [
    {"title": "...", "decision": "KEEP", "scores": {"相关性": 5, ...}, "rationale": "..."}
  ]
}
```

### Step 5: 报告总结
输出筛选统计摘要：
- 各维度平均分
- 保留率
- 综述保留数
- 去重数
- 方法类别分布

## 使用示例

```
/skill paper-filter

输入文件: 01_metadata/papers_metadata.csv
研究目标: 研究GNSS完好性监测算法，重点关注多故障检测与隔离方法
输出目录: 02_filtered
```

## 输入要求

- CSV文件由 `wos-parser` 生成
- 必须包含字段：`wos_id`, `seq_id`, `title`, `abstract`, `author_address`, `doc_type`, `year`

## 输出文件

```
02_filtered/
├── filtered_papers.csv    # 筛选后论文（新seq_id从1开始，含method_category和filter_rationale列）
└── filter_stats.json      # 筛选统计与明细
```
