---
name: wos-parser
description: 解析Web of Science导出文件，提取元数据并为每篇文献分配双序号（wos_id固定，seq_id可变）
version: 1.2.0
author: Your Name
triggers:
  - "解析WoS"
  - "WoS解析"
  - "parse wos"
  - "wos parser"
inputs:
  - name: wos_file
    type: file
    description: Web of Science导出的文本文件（标记格式或纯文本格式）
    required: true
  - name: output_dir
    type: path
    description: 输出目录
    required: true
outputs:
  - name: metadata_csv
    type: file
    description: 包含所有文献元数据+双序号的CSV
  - name: stats_json
    type: file
    description: 解析统计信息JSON
dependencies:
  - python: re, csv, json, pathlib
---

# WoS Parser

解析Web of Science导出文件，提取元数据并为每篇文献分配双序号。

## 支持的格式

- **标记格式**（推荐）：WoS 导出时选择"纯文本"，格式为 `FN/VR/PT/AU/TI/AB/PY/ER`
- **纯文本格式**：以 `Record X of Y` 开头的旧格式

## 双序号说明

- **wos_id**：原始序号（1, 2, 3...），永不变化，用于追溯原始位置
- **seq_id**：筛选后序号（初始=wos_id，筛选后重新编号），用于后续流程

## 提取字段

| 字段 | WoS标签 | 说明 |
|------|---------|------|
| wos_id | — | 原始序号（不可变） |
| seq_id | — | 可变序号（初始=wos_id，筛选后重新编号） |
| author | AU | 作者（多人以 ; 分隔） |
| title | TI | 标题 |
| journal | — | 期刊名（从 source 提取） |
| source | SO | 完整来源信息（期刊+卷+页+DOI） |
| year | PY | 出版年 |
| doi | DI | DOI |
| abstract | AB | 摘要 |
| doc_type | DT | 文献类型（Article/Review/Proceedings Paper...） |
| pub_type | PT | 出版物类型（J=期刊，C=会议，B=书籍...） |
| wos_ut | UT | WoS唯一标识符（入藏号） |
| author_address | C1 | 作者机构地址 |
| funding | FU | 基金资助信息 |
| times_cited | TC | 被引次数（WoS核心合集） |
| issn | SN | ISSN |
| isbn | BN | ISBN |
| researcher_id | RI | ResearcherID |
| author_ids | AI | 作者标识符（ORCID等） |
| pubmed_id | PM | PubMed ID |
| conference_title | CT | 会议全称 |
| sponsors | SP | 会议主办方 |
| conference_city | CL | 会议城市 |
| usage_u1 | U1 | 使用计数（最近180天） |
| usage_u2 | U2 | 使用计数（2013年至今） |
| z9 | Z9 | 总被引次数（核心合集） |

## 执行流程

1. 要求用户提供 WoS 导出文件路径和输出目录
2. 判断文件数量：
   - **单文件**：`python scripts/parse_wos.py --input <文件> --output <目录>`
   - **多文件**（WoS 每次最多导出 1000 条）：`python scripts/parse_wos.py --input f1.txt --input f2.txt --output <目录>`
   - 多文件时自动连续编号（文件1: 1-1000, 文件2: 1001-2000, ...），也可用 `--start-id` 手动指定起始序号
3. 解析完成后，报告统计信息（总数、有摘要数、有DOI数等）
4. 输出合并后的 `papers_metadata.csv` 和 `parse_stats.json`

## 使用示例

```
/skill wos-parser

输入文件: savedrecs5.txt
输出目录: 01_metadata
```

## 配置说明

- WoS格式说明见 `references/wos_format.md`
- 示例文件见 `assets/sample_wos.txt`
