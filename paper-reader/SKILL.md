---
name: paper-reader
description: This skill should be used when the user asks to "read this paper", "parse a research paper", "extract key findings from a paper", "summarize a paper's structure", "extract PICO from a paper", "identify key claims in a paper", "analyze a paper's methodology", "extract data from a study", or mentions structured reading of academic papers. Provides structured parsing and analysis of academic papers into extractable, comparable data.
---

# Paper Reader — Structured Academic Paper Parsing

Parse academic papers into structured, machine-readable data. Extract key claims, methodology details, results, and framework elements so that downstream skills (evidence-synthesis, paper-comparison, quality-assessment) can operate on consistent, structured inputs.

## Core Concept

A "raw paper" (PDF or text) becomes a **structured extraction** — a standardized JSON/YAML record that captures the paper's essential research components. This is the data input layer for the entire literature-research pipeline.

## Workflow

### Step 1: Acquire the Paper
Obtain the paper's content through available means:
- **PDF file**: Use `scientific-skills:pdf` to extract text from PDF
- **DOI/URL**: Use `semantic-scholar` to get abstract, metadata, and open access PDF URL
- **Pre-formatted text**: Use directly

Prioritize open access PDFs for full-text analysis. Fall back to abstract + metadata when full text is unavailable.

### Step 2: Identify Paper Type
Classify the paper to apply the correct extraction template:

| Type | Indicators | Extraction Template |
|------|-----------|-------------------|
| **Original Research** | Methods, Results, Data | PICO Framework |
| **Review (Narrative)** | Comprehensive summary, no new data | Review Framework |
| **Systematic Review / Meta-analysis** | PRISMA, pooled analysis | SR/MA Framework |
| **Case Report** | Single patient/case presentation | CARE Framework |
| **Methodology Paper** | Novel method, benchmark, algorithm | Methods Framework |
| **Commentary/Editorial** | Opinion, no original data | Commentary Framework |
| **Conference Abstract** | Short format, no full text | Abstract Framework |

Detection heuristics:
- Contains "systematic review" or "meta-analysis" in title → SR/MA
- Contains "case report" or patient count = 1 → Case Report
- Contains "we propose" + benchmark → Methodology
- Length < 1000 words → Abstract/Commentary
- Otherwise → Original Research (default)

### Step 3: Parse Paper Structure
Identify and extract major sections:

```
┌─────────────────────────────┐
│  Title                       │
│  Authors + Affiliations      │
│  Abstract                    │
├─────────────────────────────┤
│  1. Introduction             │ → Background, research gap, objectives
│  2. Methods / Methodology    │ → Study design, sample, analysis
│  3. Results / Findings       │ → Data, statistics, tables, figures
│  4. Discussion               │ → Interpretation, limitations, implications
│  5. Conclusion               │ → Summary, future work
├─────────────────────────────┤
│  References                  │ → Cited works
│  Supplementary Material      │ → Extra data
└─────────────────────────────┘
```

### Step 4: Extract Structured Data
Use the appropriate extraction template based on paper type.

#### PICO Extraction (Original Research)
```yaml
study_id: "Author (Year)" or DOI
paper_type: "original_research"

population:
  description: "Who was studied"
  sample_size: N
  demographics: "Age, sex, condition"
  setting: "Clinical, community, lab, online"
  inclusion_criteria: [...]
  exclusion_criteria: [...]

intervention:
  description: "What was done"
  duration: "How long"
  dose_or_intensity: "How much"
  delivery_method: "How administered"

comparison:
  type: "Control group | Placebo | Alternative intervention | Before-after"
  description: "What was compared"

outcome:
  primary:
    measure: "What was measured"
    result: "What was found"
    effect_size: "Cohen's d / OR / RR / MD"
    confidence_interval: "95% CI: [lower, upper]"
    p_value: "p = ..."
  secondary: [...]
  time_points: "When measured"

key_claims:
  - claim: "Statement of a finding"
    evidence: "Supporting data from results"
    strength: "strong | moderate | weak"
    section: "results | discussion"
```

#### Review Framework Extraction
```yaml
study_id: "Author (Year)"
paper_type: "review"

scope: "What topics were covered"
databases_searched: [...]
inclusion_criteria: [...]
number_of_studies_reviewed: N
key_findings:
  - finding: "..."
    supporting_studies: N
    consistency: "consistent | mixed | inconsistent"
identified_gaps: [...]
conclusions: "..."
```

#### Methods Framework Extraction
```yaml
study_id: "Author (Year)"
paper_type: "methodology"

problem_addressed: "What gap does this method fill"
proposed_method:
  name: "Method name"
  key_innovation: "What's new"
  inputs: "What data it requires"
  outputs: "What it produces"
evaluation:
  benchmarks: [...]
  metrics: [...]
  results: "Performance numbers"
  comparisons: "vs. baseline methods"
limitations: [...]
```

### Step 5: Extract Tables and Figures
For each table/figure encountered:

```yaml
tables:
  - number: "Table 1"
    title: "Baseline characteristics"
    key_data:
      - "Mean age: 45.2 (SD 12.3) in intervention vs 43.8 (SD 11.9) in control"
      - "Female: 52% vs 52%"
    relevance: "Confirms groups were balanced at baseline"

figures:
  - number: "Figure 1"
    title: "Kaplan-Meier survival curve"
    description: "Shows survival probability over 24 months"
    key_insight: "Intervention group had significantly longer survival"
```

### Step 6: Generate Structured Summary
Produce a concise structured summary:

```markdown
## Paper Summary: [Title]

**Type:** Original Research (RCT)
**Authors:** Smith J, Jones K, Lee M (2024)
**Journal:** Nature Medicine

### Research Question
[One sentence]

### Methodology
[Study design, sample, duration]

### Key Findings
1. [Finding 1 with effect size]
2. [Finding 2 with effect size]

### Key Claims
| # | Claim | Strength | Evidence |
|---|-------|----------|----------|
| 1 | ... | Strong | p<0.001, d=0.82 |
| 2 | ... | Moderate | p=0.03, d=0.45 |

### Limitations
1. ...
2. ...

### Relevance Assessment
[How this paper relates to the user's research question]
```

## Extraction Best Practices

### Claim Extraction Rules
- Extract claims only from Results and Discussion sections
- Distinguish author claims from data-supported findings
- Tag each claim with the supporting statistical evidence
- Note when claims are speculative (hedging language: "may", "could", "suggests")

### Number Extraction
- Always include units and confidence intervals
- Distinguish absolute vs. relative effects
- Note if numbers are estimated from figures
- Flag missing numerical data

### Handling Missing Information
When a section or data point is not available:
- Mark as `null` rather than guessing
- Note what is missing and why it matters
- Suggest whether the missing data affects downstream analysis

## Error Handling and User Checkpoints

### Checkpoints
- **After Step 2 (paper type classification)**: present detected type and confidence level to user. If ambiguous (e.g., "methodology" vs "original research"), ask user to confirm or override.
- **Before Step 4 (extraction)**: if full text is not available, warn user that extraction will be limited to abstract + metadata. Ask whether to proceed.
- **After Step 5 (tables/figures)**: if key numerical data was estimated from figures rather than text, flag each estimate for user verification.

### Error Handling
- **Unparseable PDF**: if text extraction produces garbled output, fall back to extracting only title, authors, and abstract from metadata. Do not attempt structured extraction on corrupt text.
- **Missing sections**: if a major section (Methods, Results) is absent, mark extraction fields as `null` rather than guessing from other sections.
- **Non-English paper**: if the paper is not in English, note the language and attempt extraction with reduced confidence. Warn user about potential translation errors.
- **Very short paper** (<1000 words): likely an abstract or editorial. Skip PICO extraction and use the abstract-only template instead.

## Integration with Other Skills

- **semantic-scholar** — Get paper metadata, TLDR, and open access PDF
- **scientific-skills:pdf** — Extract text from PDF files
- **paper-comparison** — Feed structured extractions into comparison framework
- **evidence-synthesis** — Feed extractions into consensus analysis
- **quality-assessment** — Assess methodological quality from extracted methods section
- **systematic-screening** — Use extracted data for screening decisions

## Additional Resources

### Reference Files
- **`references/extraction-templates.md`** — Complete extraction templates for all paper types

### Scripts
- **`scripts/extract_paper.py`** — Parse paper text into structured JSON extraction
