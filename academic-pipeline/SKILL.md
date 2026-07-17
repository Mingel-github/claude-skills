---
name: academic-pipeline
description: 学术文献处理完整流水线。依次执行：WoS解析 → 筛选 → 优先级排序 → PDF处理 → 精读 → 生成综述
version: 1.1.0
author: Your Name
triggers:
  - "跑一遍流水线"
  - "完整处理这批文献"
  - "academic pipeline"
inputs:
  - name: wos_file
    type: file
    description: Web of Science导出的文本文件
    required: true
  - name: research_goal
    type: string
    description: 研究目标描述，用于筛选和排序
    required: true
  - name: output_dir
    type: path
    description: 输出根目录
    required: true
outputs:
  - name: final_report
    type: file
    description: 最终综述报告
dependencies:
  - wos-parser
  - paper-filter
  - paper-prioritizer
  - pdf-processor
  - paper-deep-reader
  - review-generator
---

# Academic Pipeline

学术文献处理完整流水线，按顺序执行所有步骤。

## 流水线概览

```
WoS文件 + 研究目标
        │
        ▼
[Step 1] wos-parser       → 01_metadata/papers_metadata.csv
        │
        ▼
[Step 2] paper-filter     → 02_filtered/filtered_papers.csv
        │
        ▼
[Step 3] paper-prioritizer → 02_filtered/priority_list.csv
        │
        ▼
[Step 4] pdf-processor    → 04_txts/ (raw + fixed)
        │
        ▼
[Step 5] paper-deep-reader → 05_summaries/*.summary.md
        │
        ▼
[Step 6] review-generator → 06_review/ (HTML + survey + innovation)
        │
        ▼
    最终综述报告
```

## 执行流程

按顺序逐步执行，每步完成后检查输出再继续下一步。

### Step 1: WoS 解析
- **调用**: `/skill wos-parser`
- **输入**: WoS导出文件
- **输出**: `01_metadata/papers_metadata.csv` + `parse_stats.json`
- **检查点**: 确认记录数、有摘要数

### Step 2: 论文筛选
- **调用**: `/skill paper-filter`
- **输入**: `papers_metadata.csv` + research_goal
- **输出**: `02_filtered/filtered_papers.csv` + `filter_stats.json`
- **检查点**: 确认保留率是否合理（通常20-40%）

### Step 3: 优先级排序
- **调用**: `/skill paper-prioritizer`
- **输入**: `filtered_papers.csv` + research_goal
- **输出**: `02_filtered/priority_list.csv` + `priority_stats.json`
- **检查点**: 确认高/中/低优先级分布

### Step 3.5: PDF 自动匹配（新增）
在 Step 4 之前自动执行：
1. 检查 `03_pdfs/` 是否已有命名好的 PDF（有则跳过）
2. 若无，扫描项目根目录 `papers/` 文件夹（或当前目录下的 `*.pdf`）
3. 读取 `priority_list.csv` 获取论文标题列表
4. 对每个 PDF 文件名与论文标题做模糊匹配（SequenceMatcher）
5. 将匹配成功的 PDF 复制到 `03_pdfs/{seq_id}.pdf`

执行命令：
```bash
python -c "
import csv, os, shutil
from pathlib import Path
from difflib import SequenceMatcher

pdf_dir = Path('papers')
if not pdf_dir.exists():
    pdf_dir = Path('.')
target = Path('output/03_pdfs')
target.mkdir(parents=True, exist_ok=True)

# Check if already populated
existing = list(target.glob('*.pdf'))
if existing:
    print(f'03_pdfs already has {len(existing)} PDFs, skipping')
    return

# Read priority list
with open('output/02_filtered/priority_list.csv', 'r', encoding='utf-8') as f:
    papers = list(csv.DictReader(f))

pdfs = list(pdf_dir.glob('*.pdf'))
print(f'Found {len(pdfs)} PDFs in {pdf_dir}, {len(papers)} papers in priority list')

for p in papers:
    title = p.get('title', '')
    best_score = 0
    best_pdf = None
    for pdf in pdfs:
        score = SequenceMatcher(None,
            title.lower().replace(' ', '')[:80],
            pdf.stem.lower().replace('_', ' ').replace('-', ' ').replace(' ', '')[:80]
        ).ratio()
        # Also try matching against pdf_original field
        pdf_orig = p.get('pdf_original', '')
        if pdf_orig:
            score2 = SequenceMatcher(None,
                pdf_orig.lower().replace(' ', '')[:80],
                pdf.stem.lower().replace('_', ' ').replace('-', ' ').replace(' ', '')[:80]
            ).ratio()
            score = max(score, score2)
        if score > best_score:
            best_score = score
            best_pdf = pdf
    if best_score > 0.4:
        dest = target / f'{p[\"seq_id\"]}.pdf'
        shutil.copy2(best_pdf, dest)
        print(f'  [{p[\"seq_id\"]}] {p[\"title\"][:50]}... <- {best_pdf.name} (score={best_score:.2f})')
    else:
        print(f'  [{p[\"seq_id\"]}] {p[\"title\"][:50]}... NO MATCH (best={best_score:.2f})')
"
```

### Step 4: PDF 处理
- **调用**: `/skill pdf-processor`
- **输入**: `priority_list.csv` + `03_pdfs/` 目录
- **输出**: `04_txts/raw/` + `04_txts/fixed/`
- **检查点**: 确认高优先级PDF已全部提取

### Step 5: 论文精读
- **调用**: `/skill paper-deep-reader`
- **输入**: `04_txts/fixed/` + `priority_list.csv`
- **输出**: `05_summaries/*.summary.md`
- **检查点**: 确认高优先级论文已全部生成总结

### Step 6: 生成综述
- **调用**: `/skill review-generator`
- **输入**: `05_summaries/`
- **输出**: `06_review/survey.md` + `survey.docx` + `index.html` + `innovation_points.md` + `genealogy.md` + `papers_data.json`
- **Word 生成**: 综述 markdown 写完后，自动调用 `review-generator/scripts/gen_docx.py` 生成格式化 Word 文档
  ```bash
  python .claude/skills/review-generator/scripts/gen_docx.py output/06_review/survey.md output/06_review/survey.docx
  ```
  Word 文档特性：标题样式（Heading 1/2/3）、可更新目录域、可点击交叉引用、参考文献悬挂缩进两端对齐、宋体+Times New Roman

## 目录结构

```
{output_dir}/
├── 01_metadata/
│   ├── papers_metadata.csv
│   └── parse_stats.json
├── 02_filtered/
│   ├── filtered_papers.csv
│   ├── filter_stats.json
│   ├── priority_list.csv
│   └── priority_stats.json
├── 03_pdfs/                # 手动放置PDF文件
│   └── {seq_id}.pdf
├── 04_txts/
│   ├── raw/
│   │   └── {seq_id}.raw.txt
│   └── fixed/
│       └── {seq_id}.txt
├── 05_summaries/
│   ├── {seq_id}.summary.md
│   ├── {seq_id}.summary.json
│   └── all_summaries.json
└── 06_review/
    ├── survey.md
    ├── survey.docx            # Word文档（自动生成）
    ├── index.html
    ├── papers_data.json
    ├── innovation_points.md
    └── genealogy.md
```

## 使用示例

```
/skill academic-pipeline

WoS文件: savedrecs5.txt
研究目标: 研究GNSS完好性监测算法，重点关注多故障检测与隔离方法
输出目录: ./output
```

## 注意事项

1. 每个Step可独立执行，出现中断后可从中断点继续
2. PDF文件放入项目根目录 `papers/` 文件夹即可，Step 3.5 会自动模糊匹配并复制到 `03_pdfs/`
3. Step 5 和 6 依赖 AI 处理，处理时间与论文数量成正比
4. 建议先在小样本（如3-5篇）上测试完整流程
5. 生成 Word 需要 `python-docx` 库：`pip install python-docx`
