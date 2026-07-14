# Claude Code Skills 管理手册

> 安装位置：`C:\Users\mingel\.claude\skills\`  
> 总数：30 个，约 618 KB  
> 整理日期：2026-07-10

---

## 🟢 ON — 日常自动触发（8 个）

这些 skill 每次对话都可能用到，保持开启：

| Skill | 大小 | 功能 | 触发方式 |
|-------|------|------|----------|
| `semantic-scholar` | 8 KB | 搜索 2.3 亿篇学术论文（Semantic Scholar API） | 说"搜索某某主题论文" |
| `paper-reader` | 12 KB | 结构化解析论文：PICO 提取、方法分析、关键结论 | 说"读这篇论文" |
| `literature-research-liteng` | 8 KB | 深度全文阅读，HARD-GATE 防摘要幻觉 | 说"深入研究这篇" |
| `systematic-screening` | 12 KB | PRISMA 文献筛选、去重、筛选审计 | 说"系统综述筛选" |
| `evidence-synthesis` | 8 KB | 跨多篇论文证据合成，分析共识/分歧 | 说"综合这些论文" |
| `coding-standards` | 28 KB | TDD 默认工作流、命名/类型/安全/Git 规范 | 写代码即触发 |
| `code-review` | 108 KB | 四阶段代码审查（20+ 语言），按严重度分级 | 说"review 代码" |
| `humanizer` | 36 KB | 去除 AI 写作痕迹，让文本像人写的 | 说"去 AI 味" |

---

## 🟡 NAMEONLY — 点名才触发（14 个）

这些 skill 需要明确说出名称才加载，避免误触发：

| Skill | 大小 | 功能 | 何时点名使用 |
|-------|------|------|-------------|
| `annotated-bibliography` | 12 KB | 生成带注释的参考文献列表 | 要输出参考文献清单 |
| `author-network` | 12 KB | 分析作者合作网络 | 想知道某领域谁和谁合作 |
| `citation-graph` | 12 KB | 构建引文网络可视化 | 想看论文之间的引用关系 |
| `quality-assessment` | 12 KB | RoB 2 / NOS / AMSTAR 2 / CASP 评估 | 需要评估论文方法论质量 |
| `paper-comparison` | 8 KB | 多篇论文横向对比 | 比较 2+ 篇论文的异同 |
| `research-gaps` | 16 KB | 识别研究空白 | 找还没人做的方向 |
| `research-trends` | 12 KB | 分析研究趋势+新兴话题 | 了解领域热点 |
| `literature-search` | 8 KB | 中等深度文献搜索（AI 摘要级） | 快速了解一个领域 |
| `literature-review` | 4 KB | 系统性文献综述 | 需要写正式文献综述 |
| `fact-check` | 4 KB | 逐条核验声明真伪 | 验证某句话是否站得住 |
| `recursive-decomposition` | 8 KB | 大任务递归拆解策略 | 代码库太大/文件太多 |
| `doc-coauthoring` | 16 KB | 三阶段文档协作（收集→起草→读者测试） | 需要结构化写文档 |
| `pdf-processing-pro` | 56 KB | PDF 表单/表格/OCR 处理 | 扫描版 PDF 要 OCR |
| `scientific-toolkit-skill` | 10 KB | MATLAB/Python 科学计算+期刊图表 | 写科研计算代码 |

---

## 🔴 OFF — 暂时关闭（8 个）

这些 skill 与已有 skill 重叠或场景太窄，需要时再开：

| Skill | 大小 | 关闭原因 | 何时重新打开 |
|-------|------|---------|-------------|
| `autoresearch` | 28 KB | 被 `paper-reader` + `literature-review` 组合替代 | 需要完全自主运行的研究项目 |
| `literature-overview` | 8 KB | 被 `literature-search`（中深度）完全覆盖 | 仅需极快速扫一眼时 |
| `deep-research` | 4 KB | 和 `literature-review` 重叠 | 需要宽→深多轮调研 |
| `research-coordinator` | 4 KB | 太重了，你是自己的调度者 | 有特别复杂的研究任务 |
| `paper-analysis-assistant` | 60 KB | 9 步流水线太臃肿，`paper-reader` 更精准 | 需要论文→PPT 一键转换 |
| `office-academic-skill` | 12 KB | 学术 Word/PPT 场景窄 | 需要生成学术报告/答辩 PPT |
| `ml-paper-writing` | 40 KB | 仅适用于 NeurIPS/ICML/ICLR 等 ML 顶会 | 投稿 ML 顶会时 |
| `research-writing-skill` | 44 KB | 和 `humanizer` + 手动润色重叠 | 需要中文论文写+审稿回复 |

---

## 🔧 Skill 使用指南

### 什么是 Skill？

Skill 就是一个 Markdown 文件（`SKILL.md`），Claude Code 读入后将其中的规则和流程作为行为指南。
本质 = **可复用的知识外挂**，零代码，改规则就是改文本。

### 三种状态切换

在 Claude Code 中输入 `/skills`，用方向键选中一个 skill，回车切换状态：

```
on   → 自动触发（匹配 description 关键词即加载）
off  → 完全不触发
only → 独占模式，只触发这个，其他全压制
nameonly → 仅在显式点名时触发，模糊词语不误触发
```

### 触发逻辑

Claude 根据 skill 的 `description` 字段中关键词匹配决定是否加载：

```
你说 "帮我读这篇论文" → 匹配 paper-reader 的 description → 自动加载
你说 "帮我 humanize 这段" → 匹配 humanizer → 自动加载
你说 "帮我写个排序函数" → 匹配 coding-standards → 自动加载
```

nameonly 的 skill 则必需明确说出名字才会加载。

### 手动管理

```bash
# 安装
npx skills add <github-repo>                          # 一键安装
cp -r <skill-folder> ~/.claude/skills/                 # 手动复制

# 开关
mv ~/.claude/skills/<name> ~/.claude/disabled/         # 临时禁用
mv ~/.claude/disabled/<name> ~/.claude/skills/         # 重新启用

# 删除
rm -rf ~/.claude/skills/<name>

# 项目专属（替代全局）
mkdir <project>/.claude/skills/<name>                  # 仅本项目生效，可 git 共享

# 查看已安装
ls ~/.claude/skills/
# 或在 Claude Code 中输入 /skills
```

### 上下文消耗

- 30 个 skill 共 ~618 KB（约 150K token）
- 实际只会加载触发的 skill，全部 ON 不意味着一次加载 30 个
- ON 的 8 个约 150 KB，nameonly 的只在点名时加载
- 你的模型有 1M token 上下文，完全不用担心溢出

### 最佳实践

1. **保持 ON 的少而精** — 只保留高频通用 skill
2. **场景化用 nameonly** — 低频但重要的设 nameonly，用时点名
3. **定期清理** — 超过 2 周没用过的 skill 考虑关掉或删除
4. **同名冲突** — 两个 skill 有相同的 `name` 会导致冲突，装之前检查

---

## 📋 快速参考卡片

```
🔍 搜论文    → "用 semantic-scholar 搜索 XXX"
📖 读论文    → 直接说"读这篇论文"（自动触发 paper-reader）
📚 整理文献  → "用 systematic-screening 筛选" + "用 annotated-bibliography 导出"
✅ 防幻觉    → "用 literature-research-liteng 深度读" + "用 fact-check 验证"
✍️ 写论文    → humanizer 润色 + doc-coauthoring 协作 + ml-paper-writing(ML顶会)
💻 写代码    → coding-standards(写前) + code-review(写后)
🔬 科研计算  → "用 scientific-toolkit-skill 写 MATLAB/Python"
📄 扫描PDF   → "用 pdf-processing-pro 做 OCR"
```
