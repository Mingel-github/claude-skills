---
name: paper-comparison
description: This skill should be used when the user asks to "compare papers", "compare two studies", "find differences between papers", "side-by-side paper analysis", "identify contradictions in literature", "synthesize multiple papers", or "cross-study comparison". Provides a structured framework for systematic comparison of academic papers across multiple dimensions.
---

# Paper Comparison

Systematically compare multiple academic papers to identify agreements, contradictions, methodological differences, and complementary findings. This skill provides a structured framework that goes beyond surface-level comparison to reveal deep insights about the state of research.

## Core Framework

### Comparison Dimensions

Compare papers across these dimensions:

| Dimension | What to Compare |
|-----------|----------------|
| Research Question | What problem does each paper address? |
| Methodology | Study design, data collection, analytical approach |
| Sample/Population | Who/what was studied, sample size, demographics |
| Key Variables | Independent, dependent, and control variables |
| Findings | Primary results, effect sizes, statistical significance |
| Conclusions | Author interpretations, claimed contributions |
| Limitations | Acknowledged weaknesses, generalizability concerns |
| Theoretical Framework | Underlying theory or conceptual model |
| Reproducibility | Code/data availability, methodological detail |

## Workflow

### Step 1: Gather Papers
Retrieve full details for all papers to compare:
- Use `semantic-scholar` skill for paper details and TLDR
- Use `scientific-skills:pubmed-database` for biomedical papers
- Request abstracts and (if available) full-text access

### Step 2: Extract Comparison Data
Create a structured extraction for each paper:

```yaml
paper:
  id: "DOI or S2 Paper ID"
  title: "Full title"
  authors: [Author1, Author2]
  year: 2024
  venue: "Journal/Conference name"

research_question:
  primary: "Main research question"
  secondary: ["Secondary questions"]

methodology:
  design: "RCT / Cohort / Case-Control / Survey / Simulation / ..."
  data_source: "Dataset used or data collection method"
  sample_size: N
  duration: "Study period"
  analysis: "Statistical/analytical methods"

findings:
  primary: "Main finding"
  effect_size: "Cohen's d / odds ratio / etc."
  significance: "p-value or confidence interval"
  secondary: ["Additional findings"]

conclusions:
  main_claim: "Primary conclusion"
  implications: "Stated implications"
  future_work: "Suggested next steps"

limitations:
  - "Limitation 1"
  - "Limitation 2"
```

### Step 3: Construct Comparison Matrix
Build a side-by-side comparison table:

```
| Dimension       | Paper A          | Paper B          | Paper C          |
|-----------------|------------------|------------------|------------------|
| Design          | RCT (n=500)      | Cohort (n=1200)  | Meta-analysis    |
| Population      | Adults 18-65     | Elderly 65+      | Mixed            |
| Intervention    | Drug X 10mg      | Drug X 20mg      | Drug X (varied)  |
| Primary Outcome | Symptom reduction| Survival rate    | Composite        |
| Key Finding     | 30% improvement  | No significance  | 15% improvement  |
| Conclusion      | Effective        | Inconclusive     | Modest benefit   |
```

### Step 4: Analyze Agreement and Disagreement

**Agreement Analysis:**
- Which findings are consistent across papers?
- What conclusions converge despite different methods?
- Which theoretical frameworks are shared?

**Disagreement Analysis:**
- Where do findings diverge?
- What methodological differences might explain divergence?
- Are there population/context differences that account for different results?

**Complementarity Analysis:**
- Do papers address different aspects of the same problem?
- Does one paper's methodology address another's limitations?
- Do findings from different populations strengthen generalizability?

### Step 5: Synthesize Comparison

Produce a structured synthesis:

```markdown
## Comparison Synthesis: [Topic]

### Points of Agreement
- Finding 1: [shared across X/Y papers]
- Finding 2: [shared across X/Y papers]

### Points of Disagreement
- Issue 1: Paper A says X, Paper B says Y
  - Possible explanation: [methodological/population difference]
- Issue 2: ...

### Complementary Findings
- Paper A establishes X, Paper B extends to Y
- Combined, they suggest Z

### Methodological Comparison
| Aspect | Strongest Approach | Weakest Approach |
|--------|-------------------|------------------|
| Sample | Paper B (n=1200)  | Paper A (n=30)   |
| Design | Paper A (RCT)     | Paper C (survey) |

### Overall Assessment
[2-3 sentence synthesis of what the comparison reveals]
```

## Comparison Templates

### Two-Paper Deep Comparison
Use for direct head-to-head analysis of competing approaches or replication studies.

### Multi-Paper Landscape Comparison
Use for 3-10 papers covering the same topic from different angles. Focus on identifying the research frontier.

### Chronological Comparison
Order papers by publication date to trace how understanding of a topic has evolved over time.

## Visualization Aids

### Venn Diagram of Findings
For 2-3 papers, show overlap and unique findings.

### Heatmap Matrix
For 5+ papers, show agreement/disagreement across dimensions using color coding.

### Timeline Comparison
Plot papers on a timeline showing how methods and findings have evolved.

## Error Handling and User Checkpoints

### Checkpoints
- **After Step 2 (data extraction)**: display the structured extraction for each paper. Ask user to verify key data points, especially methodology and findings.
- **After Step 4 (agreement/disagreement analysis)**: present classifications (supports/refutes/mixed) for each paper. Require user review before generating the synthesis.
- **Before final synthesis**: if papers are too heterogeneous for meaningful comparison (different populations, different interventions), warn user and suggest narrowing the scope.

### Error Handling
- **Incomparable papers**: if papers differ fundamentally (e.g., in vitro vs clinical trial), note that direct comparison may be misleading. Suggest comparing within subgroups instead.
- **Missing key data**: if a paper lacks critical comparison fields (e.g., no sample size, no effect size), mark as "data unavailable" in the matrix. Do not estimate.
- **Conflicting reporting**: if a paper reports different numbers in abstract vs results section, flag the discrepancy and use the more detailed (usually results section) value with a note.
- **Single-paper comparison**: if only 1 paper is provided, explain that comparison requires 2+ papers. Offer to find similar papers using `semantic-scholar` recommendations.

## Integration with Other Skills

- **semantic-scholar** — Retrieve paper details, TLDR, citations
- **evidence-synthesis** — Aggregate comparison results into consensus assessment
- **citation-graph** — Visualize how compared papers cite each other
- **research-trends** — Place compared papers in temporal context

## Additional Resources

### Reference Files
- **`references/comparison-framework.md`** — Extended templates for different comparison types (clinical trials, ML papers, social science studies)
