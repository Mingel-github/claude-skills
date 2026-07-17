---
name: review-generator
description: 基于精读总结生成学术综述，输出Markdown（→Word via PasteMD）、交互式HTML文献库、创新点汇总、团队谱系
version: 1.2.0
author: Your Name
triggers:
  - "生成综述"
  - "生成报告"
  - "输出HTML"
  - "review"
inputs:
  - name: summary_dir
    type: path
    description: 精读总结目录（05_summaries）
    required: true
  - name: output_dir
    type: path
    description: 输出目录
    required: true
  - name: review_title
    type: string
    description: 综述标题
    required: false
  - name: review_type
    type: string
    description: 输出类型：all / html / survey / innovation / word
    default: all
outputs:
  - name: survey_md
    type: file
    description: Markdown综述（含LaTeX公式，可直接用PasteMD转为Word）
  - name: index_html
    type: file
    description: 交互式文献数据库HTML
  - name: innovation_md
    type: file
    description: 创新点汇总
  - name: genealogy_md
    type: file
    description: 团队谱系分析
---

# Review Generator

基于精读总结生成学术综述。

## 输出类型

| 类型 | 输出 | 说明 |
|------|------|------|
| `all` | 全部 | 同时生成所有输出 |
| `survey` | survey.md | Markdown综述（核心），含LaTeX公式 |
| `html` | index.html | 交互式文献数据库 |
| `innovation` | innovation_points.md | 创新点分类汇总 |
| `word` | survey.md | 同survey，配合PasteMD使用 |

## 配置说明

- 风格定义见 `references/style_guide.md`（自然语言描述，改风格不用碰代码）
- HTML模板见 `assets/template.html`
- 侧边栏配置见 `assets/sidebar_config.json`
- 布局配置见 `assets/layout_config.json`

## 执行流程

### Step 1: 收集素材
- 读取 `summary_dir` 下所有 `.summary.md` 和 `all_summaries.json`
- 读取 `references/style_guide.md` 获取风格要求
- 读取 `assets/layout_config.json` 获取需生成的模块列表
- 读取 `assets/sidebar_config.json` 获取筛选器配置

### Step 2: 数据统计
生成统计图表所需数据：
- 年份分布（各年论文数量趋势）
- 方法类别分布（各方法分类的论文数）
- 团队分布（各团队/机构的论文数）
- 问题焦点分布（各子方向的论文数）
- 相关性评分分布

### Step 3: 生成 Markdown 综述（survey.md）
根据风格指南综合提炼。模块包括：
- **摘要**：2-3段话概括整体发现和核心趋势
- **研究概述**：领域全景描述
- **研究脉络**：按时间线或方法演进逻辑组织，不逐篇罗列
- **核心方法分类**：按方法类别分组介绍，每组含代表性论文
- **创新点汇总**：按主题归类去重，每条一句话
- **技术对比表**：只列关键差异，不过度展开
- **实验数据汇总**：关键性能指标横向对比
- **团队谱系**：重要研究团队及专注方向，师承与合作关系
- **未来方向**：基于现有不足给出2-3个具体建议
- **参考文献**：IEEE格式，汇总所有引用

### Step 4: 生成交互式文献数据库（index.html）
包含以下功能：
- 文献列表表格（标题、作者、年份、方法类别、团队、评分）
- 全文搜索（标题/作者/摘要）
- 多条件筛选（年份范围、方法类别、团队、文献类型）
- 点击展开详细信息（摘要、创新点、性能指标）
- 按列排序

### Step 5: 生成团队谱系（genealogy.md）
- 列出重要研究团队（聚焦到学院/实验室级别）
- 每个团队：学术机构、代表人物、主攻分支、标志性论文
- 师承关系、合作与竞争关系（展现学术生态）
- 团队演进时间线

### Step 6: 生成 Word 文档
运行 `scripts/gen_docx.py` 将 `survey.md` 转换为格式化 Word 文档：
```
python scripts/gen_docx.py <survey.md> <output.docx>
```
生成的 `.docx` 包含：
- **Word 内置标题样式**（Heading 1/2/3），导航窗格可跳转
- **自动目录域**（右键 → 更新域即可生成目录）
- **可点击交叉引用**（正文 [N] → 参考文献条目）
- **参考文献悬挂缩进**（首行外伸、右对齐、IEEE 格式）
- **中文字体宋体 + 英文 Times New Roman**，无 MS Gothic

> 备选方案：亦可通过 PasteMD（https://github.com/RICHQAQ/PasteMD）将 Markdown 转为 Word，LaTeX→OMML 公式效果更佳。

## 风格要求

遵循 `references/style_guide.md`：
- 简洁直接，避免冗余修饰
- 综合提炼，不逐篇罗列
- 不用夸张词汇
- 涉及具体研究团队时，详细说明其学术机构、代表人物、主攻分支和标志性论文
- "团队谱系"部分要写出师承、合作与竞争关系，展现学术生态感

## 使用示例

```
/skill review-generator

精读目录: 05_summaries
输出目录: 06_review
综述标题: GNSS完好性监测研究综述
输出类型: all
```

## 输出文件

```
06_review/
├── survey.md              # Markdown综述
├── survey.docx            # Word文档（标题样式/目录/交叉引用/悬挂缩进）
├── index.html             # 交互式文献数据库
├── papers_data.json       # 文献元数据与精读数据
├── innovation_points.md   # 创新点分类汇总
└── genealogy.md           # 团队谱系分析
```
