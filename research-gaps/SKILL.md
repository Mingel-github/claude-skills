---
name: research-gaps
description: This skill should be used when the user asks to "find research gaps", "identify understudied areas", "what hasn't been studied", "find open questions in a field", "identify methodological gaps", "find population gaps", "what's missing in the literature", or mentions research opportunities, unanswered questions, or unexplored areas. Systematically identifies research gaps by analyzing topic coverage, methodological blind spots, and understudied populations across a body of literature.
---

# Research Gaps — Systematic Gap Identification

Identify what is missing, understudied, or absent from a body of literature. This skill transforms a collection of papers into a map of research opportunities — answering "what should be studied next?"

## Core Concept

Research gaps represent the delta between "what is known" and "what needs to be known." This skill systematically identifies gaps across multiple dimensions.

## Gap Taxonomy

### Type 1: Topic Gaps
Entire sub-topics that have not been addressed.

**Detection:**
1. Map all papers to a topic taxonomy (manually or via S2 `fieldsOfStudy`)
2. Identify topics with zero or very few papers
3. Compare topic distribution against the research question's scope

```yaml
topic_gaps:
  - topic: "Effect of X on Y in pediatric populations"
    papers_found: 0
    papers_in_adjacent_topics: 12
    gap_type: "complete_absence"
    opportunity: "High — adjacent research exists but this specific intersection is unexplored"

  - topic: "Long-term effects of X (>5 years)"
    papers_found: 2
    expected_based_on_short_term: 15
    gap_type: "under_representation"
    opportunity: "Medium — limited evidence exists but more is needed"
```

### Type 2: Method Gaps
Established methods not applied to specific problems.

**Detection:**
1. Catalog methods used across papers
2. Identify methods used in adjacent fields
3. Find method-problem combinations with no papers

```yaml
method_gaps:
  - method: "Bayesian hierarchical modeling"
    applied_to: "Medical diagnosis"
    not_applied_to: "Educational assessment"
    adjacent_evidence: "Bayesian models work well in medical context"
    opportunity: "Transfer successful method to new domain"

  - method: "Randomized controlled trial"
    topic: "Effect of X on Y"
    current_methods: ["Observational (8)", "Survey (5)", "Case series (2)"]
    gap: "No experimental evidence — all evidence is observational"
    opportunity: "First RCT would be high-impact"
```

### Type 3: Population Gaps
Understudied demographic groups, geographic regions, or settings.

**Detection:**
1. Extract population data from papers (use `paper-reader`)
2. Catalog demographic coverage
3. Identify unrepresented groups

```yaml
population_gaps:
  - population: "Elderly (>75 years)"
    papers_found: 3
    papers_in_general_adult: 45
    gap_ratio: 0.067
    concern: "Treatment effects may differ in elderly"

  - population: "Sub-Saharan Africa"
    papers_found: 1
    papers_from_North_America: 28
    gap_type: "geographic"
    concern: "Findings may not generalize across healthcare systems"

  - population: "Rural communities"
    papers_found: 2
    papers_from_urban: 35
    gap_type: "setting"
    concern: "Access and implementation differ by setting"
```

### Type 4: Outcome Gaps
Important outcomes not measured or reported.

```yaml
outcome_gaps:
  - outcome: "Quality of life"
    studied_in: 5
    expected_frequency: 15
    gap: "Patient-reported outcomes under-represented"

  - outcome: "Long-term safety (>2 years)"
    studied_in: 2
    short_term_safety_studied_in: 30
    gap: "Safety profile only established short-term"

  - outcome: "Cost-effectiveness"
    studied_in: 0
    efficacy_studied_in: 25
    gap: "No economic evaluation despite clinical evidence"
```

### Type 5: Time Gaps
Previously active research areas that have stalled, or emerging questions with no published work yet.

```yaml
time_gaps:
  - topic: "Molecular mechanisms of X"
    last_active_year: 2018
    gap_years: 8
    status: "abandoned_or_solved"
    needs_verification: "Check if subsequent review resolved this"

  - topic: "X in the context of recent-event-Y"
    papers_found: 0
    context: "Event Y (2023) created new urgency"
    gap_type: "temporal"
    opportunity: "First-mover advantage for early research"
```

### Type 6: Contradiction Gaps
Studies that disagree, requiring resolution research.

```yaml
contradiction_gaps:
  - question: "Does X improve Y?"
    supporting: 8
    refuting: 5
    neutral: 3
    possible_explanations:
      - "Different populations studied"
      - "Different doses/durations"
      - "Different outcome measures"
    needed: "Head-to-head comparison controlling for these variables"
```

## Workflow

### Step 1: Define Analysis Scope
- Specify the research domain and question
- Determine what constitutes a "gap" (threshold for under-representation)
- Identify comparison benchmarks (adjacent fields, expected coverage)

### Step 2: Collect and Structure Literature
Use other skills to gather papers:
- `semantic-scholar` for broad search
- `paper-reader` for structured extraction (see output schema below)
- `systematic-screening` for organized results

**Required output schema** — Each paper must be structured as follows before passing to Step 3:

```yaml
# This is the interface contract between Step 2 and Step 3.
# Every paper in the corpus MUST have these fields populated.
structured_paper:
  id: "DOI or S2 Paper ID"
  title: "Full paper title"
  year: 2024

  # At least ONE of the following 4 dimensions must be populated.
  # Empty arrays are acceptable but reduce gap detection accuracy.
  topics: ["topic_a", "topic_b"]           # from fieldsOfStudy or manual tagging
  methods: ["method_x", "method_y"]         # from methodology section extraction
  populations: ["adults", "elderly"]        # from participant/sample section
  outcomes: ["primary_outcome", "secondary_outcome"]  # from results section

  # Optional but recommended
  citation_count: 45
  venue: "Nature Medicine"
```

**Validation before proceeding to Step 3:**
- Total papers must be >= 10 (below this threshold, gap detection is unreliable)
- At least 70% of papers must have populated `topics` and `methods` fields
- If validation fails, return to collection step with broader search terms

Build a structured corpus summary:
```yaml
corpus:
  total_papers: 87
  year_range: "2015-2024"
  dimensions_coverage:
    topics: 82   # papers with topics populated
    methods: 75  # papers with methods populated
    populations: 60
    outcomes: 70
  extraction_fields: [topics, methods, populations, outcomes, year]
```

### Step 3: Map Coverage
**Input:** structured paper corpus from Step 2
**Output:** coverage_matrix (papers × categories) + per-cell counts

Create a coverage matrix — for each dimension, count papers:

**Matrix construction procedure:**
1. Extract unique values for each dimension: `topics` from all papers, `methods` from all papers, `populations`, `outcomes`
2. For each dimension pair (e.g., topics × methods), count papers that have both values
3. Mark cells as gaps using thresholds:
   - **0 papers** = complete gap (priority 1)
   - **1-2 papers** = tentative gap (priority 2)
   - **< 20% of row/column average** = relative gap (priority 3)

```
|                | Topic A | Topic B | Topic C |
|----------------|---------|---------|---------|
| Method 1       | 12      | 8       | 0 ← gap |
| Method 2       | 5       | 0 ← gap | 3       |
| Pop: Adults    | 15      | 6       | 2       |
| Pop: Elderly   | 1 ← gap | 0 ← gap | 0 ← gap |
| Pop: Children  | 0 ← gap | 3       | 0 ← gap |
```

### Step 4: Identify Gaps
Apply gap detection rules:
- **Zero papers** = complete gap (high opportunity)
- **1-2 papers** = tentative gap (need confirmation)
- **Significantly less than adjacent cells** = relative gap
- **Declining publication rate** = abandoned topic

### Step 5: Prioritize Gaps
Score each gap for researchability:

**Gap Priority Formula:**
```
Score = (Impact × 0.4) + (Feasibility × 0.3) + (Novelty × 0.3)
```
Where each factor is rated 1-10:
- **Impact** — How important is filling this gap? (clinical significance, theoretical advancement, policy relevance)
- **Feasibility** — How practical is it to study? (available methods, accessible populations, existing data)
- **Novelty** — How original would the research be? (first-mover advantage, methodological innovation)

**Score interpretation:**
| Score | Priority | Action |
|---|---|---|
| ≥ 8.0 | Critical | Strong candidate for immediate research |
| 6.0-7.9 | High | Worth pursuing, good return on effort |
| 4.0-5.9 | Medium | Consider if resources allow |
| < 4.0 | Low | Low priority, niche interest |

```yaml
gap_priority:
  - gap: "No RCTs in pediatric population"
    impact: 9  # Critical clinical need
    feasibility: 6  # Ethical complexity
    novelty: 9  # First study of its kind
    score: 8.1
    recommendation: "Critical — first-mover advantage with high clinical impact"

  - gap: "No cost-effectiveness analysis"
    impact: 7
    feasibility: 9  # Can use existing clinical data
    novelty: 3  # Standard analysis type
    score: 6.4
    recommendation: "High — straightforward study with policy relevance"
```

### Step 6: Generate Gap Map Report

```markdown
## Research Gap Map: [Topic]

### Executive Summary
Analyzed 87 papers spanning 2015-2024. Identified 12 research gaps across 4 dimensions.

### Gap Heatmap
```
             Method1  Method2  Method3
Pop_Adults   ████████ ██████   ████
Pop_Elderly  █░░░░░░░ ░░░░░░░  ░░░░░
Pop_Children ░░░░░░░░ ███░░░░  ░░░░░
```
█ = well-studied  ░ = gap

### Priority Gaps
| # | Gap Type | Description | Score | Recommendation |
|---|----------|-------------|-------|---------------|
| 1 | Population | No studies in elderly | 8.5 | Strong candidate |
| 2 | Method | No RCT evidence | 8.0 | High-priority |
| 3 | Outcome | No QoL measures | 7.5 | Important addition |

### Opportunities
1. **First RCT in pediatric population** — Score 8.5, no experimental evidence
2. **Long-term follow-up study** — Score 7.0, only short-term data exists
3. ...
```

## Error Handling and User Checkpoints

### Checkpoints
- **After Step 3 (coverage mapping)**: present the coverage matrix heatmap to user. Ask whether the topic taxonomy captures the right dimensions.
- **After Step 4 (gap identification)**: present detected gaps with their evidence (zero papers, declining trend, etc.). Require user confirmation before scoring — some "gaps" may reflect search strategy limitations rather than true research absences.
- **Before Step 6 (gap map report)**: show the prioritized gap list. Ask user to validate the top 3 gaps, as these will shape the final recommendations.

### Error Handling
- **Insufficient corpus** (<10 papers): warn user that gap identification from sparse data is unreliable. Gaps may reflect search failure, not research absence. Suggest broadening search before gap analysis.
- **Over-represented sub-topics**: if one sub-topic dominates the corpus (>60% of papers), note that gap detection may be biased. Gaps in under-represented areas may be artifacts of search strategy.
- **Gap hallucination risk**: if a gap is detected based on keyword absence but the topic is addressed differently (different terminology), flag this as a potential false positive. Do not declare a gap without verifying that the research truly doesn't exist under alternative terms.
- **Temporal bias**: recent papers may not yet have citations, making them appear as "inactive" areas. Account for publication lag when assessing time gaps.

## Integration with Other Skills

- **paper-reader** — Extract structured data for coverage mapping
- **evidence-synthesis** — Contradiction gaps from consensus analysis
- **research-trends** — Distinguish abandoned topics from emerging gaps
- **systematic-screening** — Use screened corpus as gap analysis input
- **author-network** — Identify who is best positioned to fill each gap

## Additional Resources

### Reference Files
- **`references/gap-detection-methods.md`** — Detailed gap detection algorithms and scoring frameworks
