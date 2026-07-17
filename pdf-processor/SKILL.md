---
name: pdf-processor
description: PDF处理：解锁加密、本地提取全文（免费）、公式修复
version: 1.1.0
author: Your Name
triggers:
  - "处理PDF"
  - "PDF转TXT"
  - "提取文本"
  - "pdf processor"
  - "修复公式"
inputs:
  - name: priority_csv
    type: file
    description: priority_list.csv (由paper-prioritizer生成)
    required: true
  - name: pdf_dir
    type: path
    description: PDF文件存放目录
    required: true
  - name: output_dir
    type: path
    description: 输出目录
    required: true
outputs:
  - name: raw_txt_dir
    type: path
    description: 所有PDF的原始提取文本
  - name: fixed_txt_dir
    type: path
    description: 高优先级论文的公式修复版
dependencies:
  - python: PyMuPDF, pikepdf, pandas
---

# PDF Processor

处理PDF文件，分两步：本地提取TXT（全部论文）+ 公式修复（高优先级论文）。

## 处理逻辑

| 批次 | 本地提取 | 公式修复 | 用于精读 |
|------|---------|---------|---------|
| 高优先级 | ✓ | ✓ | 修复版 |
| 中优先级 | ✓ | ✗ | 原始版 |
| 低优先级 | ✓ | ✗ | 不精读 |

## 执行流程

### Step 1: 本地提取（scripts/extract_pdf.py）

使用 PyMuPDF + pikepdf 免费提取全文：

```bash
python scripts/extract_pdf.py --priority <priority_list.csv> --pdf-dir <PDF目录> --output <输出目录>
```

功能：
- 自动检测并解除PDF加密（无需密码的那种）
- 两栏论文智能提取（自动识别左右栏）
- 分离正文与参考文献（识别 References/Bibliography/参考文献 标记）
- 输出到 `{output_dir}/raw/` 目录

**依赖安装**：
```bash
pip install pymupdf pikepdf pandas
```

### Step 2: 公式修复（高优先级论文）

仅对高优先级论文执行。读取 `raw/{seq_id}.raw.txt`，将其中的数学公式转换为 LaTeX 格式：

- 识别数学表达式、公式、符号
- 行内公式转 `$...$`，独立公式转 `$$...$$`
- 希腊字母转 LaTeX 命令（σ→`\sigma`，μ→`\mu` 等）
- 上下标转 LaTeX 格式（x²→`x^{2}`，xᵢ→`x_{i}`）
- 分数转 `\frac{}{}`，根号转 `\sqrt{}`
- 保持所有文本内容不变，只改公式部分
- 输出到 `{output_dir}/fixed/{seq_id}.txt`

修复标准见 `references/fix_prompt.md`。

## 使用示例

```
/skill pdf-processor

优先级列表: 02_filtered/priority_list.csv
PDF目录: 03_pdfs
输出目录: 04_txts
```

## 输出目录结构

```
04_txts/
├── raw/                  # 所有论文的原始提取
│   ├── 1.raw.txt
│   ├── 2.raw.txt
│   └── ...
└── fixed/                # 高优先级修复版 + 中低优先级原始版
    ├── 1.txt             # 高优先级 → 公式修复版
    ├── 2.txt             # 中优先级 → 原始版
    └── ...
```
