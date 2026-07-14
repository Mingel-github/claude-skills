---
name: annotated-bibliography
description: This skill should be used when the user asks to "create an annotated bibliography", "generate bibliography with notes", "write annotations for papers", "organize my references", "export a reading list", "create a literature summary table", or mentions annotated bibliographies, reference annotations, or structured reading lists. Generates structured annotations for collections of academic papers, organized by theme, methodology, or chronology.
---

# Annotated Bibliography — Structured Reference Collections

Generate organized, annotated bibliographies from collections of academic papers. Each entry includes a structured annotation covering purpose, methodology, findings, and relevance — going far beyond a simple reference list.

## Core Concept

An annotated bibliography transforms a flat list of citations into a **curated, annotated research resource**. Each entry answers four questions about a paper:

1. **What** did they study? (Purpose)
2. **How** did they study it? (Methodology)
3. **What** did they find? (Key Findings)
4. **Why** does it matter? (Relevance to your research)

## Annotation Template

### Standard Annotation
```yaml
entry:
  citation:
    apa: "Smith, J., Jones, K., & Lee, M. (2024). Novel approach to X using Y. Nature Medicine, 30(4), 123-135. https://doi.org/10.1234/abc"
    vancouver: "Smith J, Jones K, Lee M. Novel approach to X using Y. Nat Med. 2024;30(4):123-35."
    bibtex: "@article{smith2024novel, author={Smith, J and Jones, K and Lee, M}, title={Novel approach to X using Y}, journal={Nature Medicine}, volume={30}, number={4}, pages={123--135}, year={2024}}"

  annotation:
    purpose: "Investigated whether Y improves outcomes in patients with X"
    methodology: "Phase 3 RCT (n=500), multi-center, double-blind, 12-month follow-up"
    key_findings:
      - "30% improvement in primary endpoint (p<0.001)"
      - "Safety profile comparable to standard of care"
      - "Subgroup analysis showed stronger effect in severe cases"
    relevance: "Directly addresses our research question about Y as an intervention for X; one of the largest RCTs to date"
    quality: "High — well-designed RCT with adequate sample size and blinding"

  metadata:
    study_type: "RCT"
    sample_size: 500
    year: 2024
    doi: "10.1234/abc"
```

### Concise Annotation (1-2 paragraphs)
```
Smith et al. (2024) conducted a multi-center, double-blind RCT (n=500) to evaluate
Y as a treatment for X over 12 months. The study found a 30% improvement in the
primary endpoint (p<0.001) with a safety profile comparable to standard of care.
Notably, subgroup analysis revealed stronger effects in severe cases. This study is
directly relevant to our research as it provides the strongest experimental evidence
to date for Y's efficacy in X, with a well-designed methodology and adequate power.
```

### Comprehensive Annotation (for key papers)
```
Smith, Jones, and Lee (2024) investigated the efficacy of Y intervention for
improving outcomes in patients with condition X.

PURPOSE: The authors aimed to determine whether Y provides clinically meaningful
improvement over standard treatment in a diverse patient population.

METHODOLOGY: Phase 3, multi-center (n=12 sites), double-blind randomized controlled
trial with 500 participants, stratified by disease severity. Intervention group
received Y for 12 months; control group received placebo. Primary endpoint: change
in symptom severity score. Secondary endpoints: quality of life, adverse events,
biomarker changes. Analysis: intention-to-treat with pre-specified subgroup analyses.

KEY FINDINGS: (1) 30% improvement in primary endpoint vs. control (95% CI: 22-38%,
p<0.001, Cohen's d=0.82). (2) Quality of life improved significantly (p=0.003).
(3) Safety profile comparable to control (adverse event rate 12% vs 11%). (4)
Subgroup analysis: effect stronger in severe cases (d=1.1) vs moderate (d=0.5).

RELEVANCE: This is the largest and most rigorous trial of Y for X to date. Its
findings directly support our hypothesis that Y is effective, particularly in
severe cases. The multi-center design enhances generalizability. Limitations
include 12-month duration (long-term effects unknown) and exclusion of patients
with comorbidities.

QUALITY ASSESSMENT: Low risk of bias (RoB 2). Adequate randomization, blinding,
and follow-up (94% retention). Pre-registered (ClinicalTrials.gov: NCT0123456).
```

## Organization Schemes

### By Theme/Topic
Group papers by the sub-topic they address:
```markdown
## Theme 1: Efficacy of Intervention X
- Smith (2024) — Strongest RCT evidence
- Jones (2023) — First positive trial
- ...

## Theme 2: Safety of Intervention X
- Lee (2024) — Comprehensive safety analysis
- ...
```

### By Methodology
Group by study design:
```markdown
## Randomized Controlled Trials
- Smith (2024), Jones (2023) — ...

## Observational Studies
- Brown (2022), Davis (2021) — ...

## Systematic Reviews
- Wilson (2023) — ...
```

### By Chronology
Ordered by publication date to show evolution:
```markdown
## 2019-2020: Early Evidence
- First observational studies suggesting benefit

## 2021-2022: Growing Evidence
- Larger cohort studies, first RCTs

## 2023-2024: Confirmatory Evidence
- Phase 3 RCTs, meta-analyses
```

### By Relevance
Ordered by importance to the user's research:
```markdown
## Essential (Directly addresses research question)
- Smith (2024) — Key trial
- ...

## Highly Relevant (Addresses related questions)
- Jones (2023) — Adjacent population
- ...

## Background (Provides context)
- Brown (2020) — Historical overview
- ...
```

## Literature Summary Table

Generate a compact summary table for quick reference:

```markdown
| Citation | Design | N | Intervention | Key Finding | Quality | Relevance |
|----------|--------|---|-------------|-------------|---------|-----------|
| Smith 2024 | RCT | 500 | Drug X 10mg | 30% improvement (p<.001) | High | ★★★ |
| Jones 2023 | RCT | 200 | Drug X 20mg | 15% improvement (p=.03) | Moderate | ★★★ |
| Lee 2022 | Cohort | 1200 | Drug X (varied) | No association | Low (observational) | ★★ |
```

## Export Formats

### APA Annotated Bibliography
```
Smith, J., Jones, K., & Lee, M. (2024). Novel approach to X using Y. Nature
    Medicine, 30(4), 123-135. https://doi.org/10.1234/abc

    Smith et al. investigated the efficacy of Y for X in a multi-center RCT (n=500).
    [Annotation continues...]
```

### BibTeX with Annotation
```bibtex
@article{smith2024novel,
  author = {Smith, J and Jones, K and Lee, M},
  title = {Novel approach to X using Y},
  journal = {Nature Medicine},
  volume = {30},
  number = {4},
  pages = {123--135},
  year = {2024},
  doi = {10.1234/abc},
  annotation = {Investigated Y for X. RCT n=500. Found 30% improvement.
    Highly relevant to our research question. Quality: High.},
  relevance = {essential}
}
```

### Markdown (default)
Full structured annotation with headers and formatting.

## Workflow

### Step 1: Collect Papers

**Input format** — Accept papers in any of these formats:
- List of DOIs: `["10.1234/abc", "10.5678/def"]`
- List of S2 Paper IDs: `["S2:abc123", "S2:def456"]`
- Structured list with metadata (preferred):
```yaml
papers:
  - title: "Paper Title"
    authors: "Smith J, Jones K"
    year: 2024
    doi: "10.1234/abc"
    abstract: "..."  # optional but recommended
```
- Free-text list: user provides titles, skill resolves via `semantic-scholar`

Gather papers from:
- `semantic-scholar` search results
- `systematic-screening` included studies
- Manual additions

**Output:** validated paper list with DOIs resolved and duplicates removed.

### Step 2: Extract Structured Data

Use `paper-reader` to extract from each paper. Extraction fields depend on annotation depth:

| Annotation Depth | Required Fields | Source |
|---|---|---|
| **Concise** | title, authors, year, abstract, main_finding | abstract + metadata |
| **Standard** | + methodology, sample_size, key_results (3-5) | full text or TLDR |
| **Comprehensive** | + study_design_details, limitations, quality_notes, effect_sizes | full text required |

For papers without full-text access, generate from abstract + metadata and mark as `[Metadata-only annotation]`.

**Output per paper:**
```yaml
extracted:
  purpose: "One sentence on research question"
  methodology: "Design + sample + intervention"
  key_findings: ["finding1", "finding2", "finding3"]
  limitations: ["limitation1", "..."]
  relevance_tier: "essential | highly_relevant | background"  # user-assigned
```

### Step 3: Generate Annotations
Apply the annotation template at the desired depth:
- **Concise**: 1-2 paragraphs (for 20+ papers)
- **Standard**: 3-5 sentences per section (for 10-20 papers)
- **Comprehensive**: Full analysis (for <10 key papers)

If user does not specify depth, select based on paper count: <10 → comprehensive, 10-20 → standard, >20 → concise.

### Step 4: Organize and Export

**Organization scheme selection:**
- User specifies → use their choice (theme/method/chronology/relevance)
- User does not specify → default to **relevance** if user has a stated research question, otherwise **theme**

**Export format selection:**
| Format | Best For | Citation Style |
|---|---|---|
| **Markdown** | Reading/review | Custom structured |
| **APA 7th** | Social sciences | Author (Year) |
| **Vancouver** | Biomedical | Numbered [1] |
| **BibTeX** | LaTeX/Reference managers | @article{key...} |
| **Chicago** | Humanities | Notes-Bibliography |

Generate the final bibliography with:
1. Header (topic, paper count, date, organization scheme)
2. Organized sections with annotations
3. Literature Summary Table at the end

## Error Handling and User Checkpoints

### Checkpoints
- **Before generating annotations (Step 3)**: ask user to select (1) annotation depth (concise/standard/comprehensive), (2) organization scheme (by theme/method/chronology/relevance), (3) citation format (APA/Vancouver/BibTeX/MLA/Chicago). Present a sample annotation for approval before batch processing.
- **After generating all annotations**: present a summary showing count, average annotation length, and the first 3 entries for user spot-check.
- **Before final export**: show the complete formatted output for user review. Allow editing of individual entries before saving.

### Error Handling
- **Missing abstract or full text**: if a paper has no abstract and full text is unavailable, generate a minimal annotation from title + metadata only. Clearly mark as "[Metadata-only annotation]".
- **Citation format errors**: if the user's requested format is unfamiliar, fall back to APA 7th and note the fallback. Do not guess formatting rules.
- **Too many papers for comprehensive annotation** (>30): warn user that comprehensive mode may be impractical. Suggest switching to concise mode or splitting into batches.
- **Duplicate papers in list**: if the same paper appears multiple times, merge into a single entry and note the deduplication.

## Integration with Other Skills

- **semantic-scholar** — Get paper metadata and TLDR for annotation generation
- **paper-reader** — Extract structured data for comprehensive annotations
- **evidence-synthesis** — Use synthesis results to enrich annotations
- **paper-comparison** — Cross-reference comparison findings
- **quality-assessment** — Include quality ratings in annotations
- **citation-management** — Generate properly formatted citations

## Additional Resources

### Reference Files
- **`references/citation-formats.md`** — Detailed citation formatting rules for APA 7th, Vancouver, Chicago, MLA, and BibTeX
