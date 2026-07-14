---
name: evidence-synthesis
description: This skill should be used when the user asks to "analyze academic consensus", "find where research agrees or disagrees", "synthesize evidence from multiple papers", "create a consensus meter", "do evidence synthesis", "systematic review data extraction", or "compare findings across studies". Provides structured methodology for analyzing agreement, disagreement, and confidence levels across multiple research papers.
---

# Evidence Synthesis

Systematically analyze academic consensus, conflict, and confidence across multiple research papers. This skill operationalizes the evidence synthesis phase of systematic reviews — going beyond individual paper retrieval to assess the collective state of scientific knowledge on a question.

## Core Concept

Evidence synthesis answers: **"What does the body of evidence say about this question?"**

This differs from literature search (finding papers) and literature review (summarizing papers). Evidence synthesis evaluates the *agreement*, *disagreement*, *confidence*, and *gaps* across findings.

## Workflow

### Step 1: Frame the Research Question
Transform a topic into a structured question:

- **PICO format** (health/clinical): Population, Intervention, Comparison, Outcome
- **PEO format** (qualitative): Population, Exposure, Outcome
- **SPIDER format** (mixed methods): Sample, Phenomenon of Interest, Design, Evaluation, Research type

Define:
- The specific claim or hypothesis to evaluate
- Inclusion/exclusion criteria for papers
- The outcome measures to extract

### Step 2: Retrieve and Screen Papers
Use available skills to gather papers:
- `scientific-skills:pubmed-database` for biomedical literature
- `scientific-skills:openalex-database` for cross-disciplinary search
- `literature-research:semantic-scholar` for S2-powered discovery
- `scientific-skills:literature-review` for systematic search strategies

Screen titles and abstracts against inclusion criteria. Aim for 10-50 papers for synthesis.

### Step 3: Extract Key Data Points
For each included paper, extract into a structured table:

| Field | Description |
|-------|-------------|
| Study ID | Author (Year) or DOI |
| Design | RCT, cohort, case-control, review, etc. |
| Sample | Population and sample size |
| Intervention/Exposure | What was tested |
| Outcome Measure | Primary outcome |
| Key Finding | Direction and magnitude of effect |
| Quality Assessment | Risk of bias (high/medium/low) |
| Confidence | Study-level certainty |

### Step 4: Analyze Agreement and Disagreement
Classify each paper's finding relative to the research question:

- **Supports** — Finding aligns with the claim
- **Refutes** — Finding contradicts the claim
- **Mixed/Neutral** — Finding is ambiguous or partial

Compute the **Consensus Ratio**:
```
Consensus Ratio = (Supports - Refutes) / Total Studies
Range: [-1.0, +1.0]
  +1.0 = unanimous support
  -1.0 = unanimous refutation
   0.0 = equal split or all neutral
```

### Step 5: Assess Confidence Level
Evaluate overall confidence based on:

| Factor | High Confidence | Low Confidence |
|--------|----------------|----------------|
| Study count | 20+ papers | <5 papers |
| Study design | Multiple RCTs | Only observational |
| Consistency | >80% agreement | <60% agreement |
| Sample sizes | Large (n>1000) | Small (n<50) |
| Publication bias | Unlikely | Suspected |

### Step 6: Generate Consensus Report
Produce a structured report with:

1. **Consensus Meter** — Visual indicator of agreement level
2. **Evidence Summary** — 2-3 sentence synthesis of the body of evidence
3. **Key Findings** — Bullet list of consistent findings across papers
4. **Conflicting Findings** — Where papers disagree and why
5. **Confidence Assessment** — Overall certainty with justification
6. **Research Gaps** — Unanswered questions or understudied areas
7. **Recommendation** — What the evidence suggests for practice or further research

## Consensus Meter Format

Present consensus visually:

```
Strongly     Mixed/     Strongly
Refutes      Uncertain   Supports
  ◄━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━►
                    ▲
               [position based on ratio]
```

Position interpretation:
- 0.8 to 1.0: Strong consensus supporting
- 0.4 to 0.8: Moderate consensus supporting
- -0.4 to 0.4: Mixed/uncertain
- -0.8 to -0.4: Moderate consensus refuting
- -1.0 to -0.8: Strong consensus refuting

## Quality Assessment Framework

### For Experimental Studies
- Randomization adequacy
- Blinding
- Allocation concealment
- Selective reporting
- Attrition bias

### For Observational Studies
- Confounding control
- Measurement bias
- Selection bias
- Follow-up completeness

### For Reviews/Meta-analyses
- Search comprehensiveness
- Duplicate screening
- Data extraction reproducibility
- Publication bias assessment

## Handling Disagreement

When papers conflict:

1. **Check study quality** — Higher quality studies carry more weight
2. **Check population differences** — Effects may vary by subgroup
3. **Check outcome measures** — Different measures may yield different conclusions
4. **Check temporal trends** — Earlier studies may use outdated methods
5. **Check funding/source** — Industry-funded studies may show bias
6. **Document the conflict** — Clearly state that evidence is inconsistent

## Error Handling and User Checkpoints

### Checkpoints
- **After Step 2 (retrieve and screen)**: present the final paper list with counts. Require user to confirm the included set before extraction.
- **After Step 3 (data extraction)**: display the structured evidence table. Ask user to verify key data points, especially effect sizes and p-values.
- **After Step 4 (agreement analysis)**: present the support/refute/neutral classification for each paper. Require user confirmation before computing the Consensus Ratio.
- **Before Step 6 (consensus report)**: show the Consensus Meter position and confidence assessment. Ask user whether the assessment accurately reflects the evidence.

### Error Handling
- **Very few papers** (<5): warn user that synthesis conclusions are tentative. Suggest broadening search or switching to narrative description.
- **High heterogeneity**: if papers use vastly different methods or populations, note that quantitative consensus may be misleading. Recommend subgroup analysis.
- **All papers from same group**: if most included papers share authors or funding, flag potential confirmation bias.
- **Conflicting high-quality studies**: if two or more well-designed studies directly contradict each other, do not force consensus. Present both positions and identify the specific methodological difference that may explain the conflict.

## Integration with Other Skills

- **semantic-scholar** — Retrieve papers and TLDR summaries for quick screening
- **citation-graph** — Trace citation lineage to identify seminal vs. derivative works
- **paper-comparison** — Detailed side-by-side analysis of key papers
- **scientific-skills:statistical-analysis** — Meta-analysis of quantitative results

## Additional Resources

### Reference Files
- **`references/methodology.md`** — Detailed methodology for different synthesis types (narrative, scoping, meta-analytic)
