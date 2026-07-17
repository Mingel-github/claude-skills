---
name: paper-deep-reader
description: 精读论文，提取结构化信息：研究问题、方法、实验数据、团队、创新点、对比分析
version: 1.2.0
author: Your Name
triggers:
  - "精读论文"
  - "deep read"
  - "提取论文信息"
  - "总结论文"
inputs:
  - name: txt_file
    type: file
    description: 论文TXT文件
    required: false
  - name: txt_dir
    type: path
    description: TXT目录（批量模式）
    required: false
  - name: output_dir
    type: path
    description: 输出目录
    required: true
  - name: max_papers
    type: number
    description: 最多处理数量（0=全部）
    default: 0
  - name: formula_level
    type: string
    description: 公式详细程度 (none/compact/full)，默认compact
    default: compact
  - name: compare_methods
    type: boolean
    description: 是否做方法对比点评
    default: false
  - name: team_detail
    type: string
    description: 团队信息详细程度 (brief/detailed/genealogy)，默认brief
    default: brief
outputs:
  - name: summary_md
    type: file
    description: 精读总结Markdown文件
  - name: summary_json
    type: file
    description: 结构化JSON文件
---

# Paper Deep Reader

深度精读论文，提取结构化信息供后续综述使用。

## 文献集大小判断（重要）

**先统计论文数量，选择对应策略**：

- **≤30篇（小集）**：无需逐篇精读。直接将所有论文全文交给 Claude，结合 review-generator 的撰写提示词一步合成综述。如果仍希望生成结构化摘要备用，可使用下方精读模板。
- **>30篇（大集）**：按下方流程逐篇精读，按优先级顺序处理。

## 读取格式说明

- 优先读取 `references/extraction_fields.md` 获取提取字段模板（若文件存在）
- 若不存在，使用下列内置模板

## 执行流程

### 单篇模式
1. 读取TXT文件全文
2. 根据 `formula_level` / `compare_methods` / `team_detail` 参数调整提取范围
3. 按提取模板逐项分析
4. 输出 `.summary.md` 和 `.summary.json`

### 批量模式
1. 扫描 `txt_dir` 下所有 `.txt` 文件
2. 跳过已有 `.summary.md` 的论文（断点续跑）
3. 先处理高优先级论文
4. 逐一精读，每次完成后保存
5. 全部完成后生成 `all_summaries.json` 汇总

## 提取字段

### 核心字段（必提取）

1. **研究问题与背景** — 核心问题 + 现有方法不足 + 问题定义
2. **核心方法** — 方法名称、算法流程（全过程推演）、关键公式（见公式控制）
3. **实验数据与性能指标** — 关键指标（精度/RMSE/成功率/计算时间等）、实验数据集/场景、与其他方法的对比结果
4. **创新点** — 3-5点核心贡献
5. **局限与未来方向** — 方法局限、适用场景边界、未来工作

### 可选字段（根据参数启用）

6. **方法对比点评**（compare_methods=true）：
   - 相比同类方法的主要优势
   - 主要局限或不足
   - 适用场景的边界条件

7. **团队与机构信息**（team_detail）：
   - brief：第一作者+通讯作者+所在学校/学院
   - detailed：+ 实验室名称、主攻方向、代表人物、标志性论文
   - genealogy：+ 师承关系、合作与竞争关系（用于综述"团队谱系"部分）

## 公式控制

| formula_level | 行为 |
|---------------|------|
| `none` | 全程禁止公式符号，用自然语言描述方法过程 |
| `compact`（默认） | 仅保留1-2个核心公式，每个需附文字解释 |
| `full` | 保留完整数学推导，每个公式附文字解释 |

## 格式要求

- 公式用 LaTeX：行内 `$...$`，独立 `$$...$$`
- 数值数据精确呈现，不四舍五入
- 不存在的部分写"未提及"
- 输出用中文
- 方法过程做"全过程推演"：像给非专业人士讲故事一样完整描述

## 输出格式

### Markdown 示例

```markdown
# {论文标题}

## 1. 研究问题与背景
- **要解决的问题**：...
- **现有方法不足**：...

## 2. 核心方法
- **方法名称**：...
- **全过程推演**：1. 2. 3. ...
- **关键公式**：$$...$$（附文字解释）

## 3. 实验数据与性能指标
| 指标 | 数值 | 数据集/场景 |
|------|------|-------------|
| ... | ... | ... |
- **对比结果**：...

## 4. 创新点
1. ...
2. ...

## 5. 局限与未来方向
- **方法局限**：...
- **适用边界**：...
- **未来工作**：...

## 6. 方法对比点评（可选）
- **优势**：...
- **不足**：...
- **边界条件**：...

## 7. 团队与机构（可选）
- **第一作者**：...（学校/学院）
- **通讯作者**：...（学校/学院/实验室）
- **主攻方向**：...
```

### JSON 输出

```json
{
  "title": "论文标题",
  "sections": {
    "1. 研究问题与背景": "...",
    "2. 核心方法": "...",
    "3. 实验数据与性能指标": "...",
    "4. 创新点": "...",
    "5. 局限与未来方向": "..."
  },
  "optional_sections": {
    "6. 方法对比点评": "...",
    "7. 团队与机构": "..."
  }
}
```

## 使用示例

单篇：
```
/skill paper-deep-reader

TXT文件: 04_txts/1.txt
输出目录: 05_summaries
公式详细程度: compact
方法对比: false
团队信息: brief
```

批量：
```
/skill paper-deep-reader

TXT目录: 04_txts
输出目录: 05_summaries
最大数量: 10
公式详细程度: compact
方法对比: true
团队信息: detailed
```

## 注意事项

- 输入TXT文件过长时截断处理
- 大集（>30篇）按优先级顺序处理
- 小集（≤30篇）可跳过逐篇精读，直接合成综述
- 支持断点续跑（跳过已有 `.summary.md` 的论文）

## 输出文件

```
05_summaries/
├── 1.summary.md
├── 1.summary.json
├── 2.summary.md
├── 2.summary.json
└── all_summaries.json
```
