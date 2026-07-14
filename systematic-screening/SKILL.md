---
name: systematic-screening
description: This skill should be used when the user asks to "screen papers for systematic review", "do PRISMA screening", "remove duplicate papers", "deduplicate search results", "build a PRISMA flow diagram", "track screening decisions", or mentions systematic review screening, inclusion/exclusion criteria, or title/abstract screening. Provides structured screening workflow management with deduplication, PRISMA reporting, and screening audit trails.
---

# Systematic Screening — PRISMA Workflow Management

Manage the screening phase of systematic reviews: deduplicate results across databases, apply inclusion/exclusion criteria, track decisions, and generate PRISMA flow diagrams. This skill operationalizes the most time-consuming phase of systematic reviews.

## Core Concept

Systematic screening transforms a large, messy set of search results from multiple databases into a clean, verified set of included studies — with a complete audit trail.

```
Search Results (500-5000) → Deduplicate → Screen Titles → Screen Abstracts → Full-text Review → Included (20-50)
```

## Workflow

### Step 1: Import Search Results
Collect results from multiple sources:
- `scientific-skills:pubmed-database` — PubMed/MEDLINE results
- `literature-research:semantic-scholar` — S2 results
- `scientific-skills:openalex-database` — OpenAlex results
- `scientific-skills:biorxiv-database` — bioRxiv preprints
- Manual additions (snowball searching, expert recommendations)

Each result should include: `title`, `authors`, `year`, `abstract`, `doi`, `source_database`

### Step 2: Deduplicate
Remove duplicate records across databases.

**Deduplication strategy (in priority order):**

1. **DOI match** — Exact DOI comparison (most reliable) ✅ `scripts/deduplicate.py`
2. **PMID match** — PubMed ID comparison (manual review fallback)
3. **Title similarity** — SequenceMatcher fuzzy matching (>90% threshold) ✅ `scripts/deduplicate.py`
4. **Author + Year + Title** — Composite key match (manual review fallback)
5. **Manual review** — Flag uncertain matches (confidence 85-92%) for human decision

**Script coverage:** `scripts/deduplicate.py` implements strategies 1 and 3. Strategies 2, 4, and 5 require manual review by the user. When running the script, unmatched records with similarity 85-92% are flagged in the output for human inspection.

**Deduplication record:**
```yaml
duplicate_groups:
  - canonical: "DOI:10.1234/abc"
    duplicates:
      - source: "PubMed"
        local_id: "PMID:12345678"
      - source: "Semantic Scholar"
        local_id: "S2:abc123def"
      - source: "OpenAlex"
        local_id: "OA:W1234567"
    match_method: "DOI exact"
    confidence: 1.0
```

### Step 3: Define Screening Criteria
Document inclusion and exclusion criteria before screening:

```yaml
screening_criteria:
  inclusion:
    - "Published in peer-reviewed journal"
    - "Human studies"
    - "Published 2015-2025"
    - "English language"
    - "Reports [outcome of interest]"
  exclusion:
    - "Conference abstracts only (no full text)"
    - "Animal or in vitro studies"
    - "Review articles (unless looking for reviews)"
    - "Case reports (unless relevant)"
    - "Non-English language"
    - "Population not matching criteria"
```

### Step 4: Title/Abstract Screening
Screen each paper's title and abstract against criteria.

**Decision options:**
- `include` — Clearly meets criteria
- `exclude` — Clearly does not meet criteria
- `maybe` — Uncertain, needs full-text review

**Screening record per paper:**
```yaml
paper_id: "DOI:10.1234/abc"
title: "Paper Title"
decision: "include | exclude | maybe"
reason: "Meets all inclusion criteria" | "Animal study" | "Unclear population"
screener: "AI-assisted" | "Human"
timestamp: "2024-01-15T10:30:00Z"
```

**AI-assisted screening logic:**
1. Check title against exclusion criteria (high confidence exclusion)
2. Check abstract for key inclusion markers (population, intervention, outcome)
3. Flag papers with missing abstracts for manual review
4. Never auto-include — always flag for human confirmation
5. Auto-exclude only on clear violations (wrong species, wrong language, wrong publication type)

### Step 5: Full-Text Review
For papers passing title/abstract screening:

1. Retrieve full text (use `paper-reader` skill)
2. Verify against all inclusion/exclusion criteria
3. Record decision with specific reason

**Full-text screening record:**
```yaml
paper_id: "DOI:10.1234/abc"
decision: "include | exclude"
exclusion_reason: "Wrong comparison group" | null
criteria_checked:
  peer_reviewed: true
  correct_population: true
  correct_intervention: false
  reports_outcome: true
  date_range: true
  language: true
```

### Step 6: Generate PRISMA Flow Diagram

Produce a PRISMA 2020 compliant flow diagram in text/markdown format:

```
┌─────────────────────────────────────────────────┐
│              PRISMA 2020 Flow Diagram             │
├─────────────────────────────────────────────────┤
│                                                   │
│  Identification                                   │
│  ├─ Records from PubMed (n=1,245)                │
│  ├─ Records from S2 (n=892)                      │
│  ├─ Records from OpenAlex (n=654)                │
│  └─ Records from other sources (n=47)            │
│       Total identified: n=2,838                   │
│                    ↓                              │
│  Screening                                        │
│  ├─ Duplicates removed (n=423)                    │
│  └─ Records screened (n=2,415)                    │
│       ├─ Excluded by title/abstract (n=1,892)    │
│       └─ Sought for retrieval (n=523)            │
│            ├─ Not retrieved (n=31)                │
│            └─ Assessed for eligibility (n=492)    │
│                 ├─ Excluded (n=423)               │
│                 │   ├─ Wrong population (n=142)   │
│                 │   ├─ Wrong intervention (n=98)  │
│                 │   ├─ No outcome data (n=87)     │
│                 │   └─ Other (n=96)               │
│                 └─ Included in synthesis (n=69)   │
│                                                   │
└─────────────────────────────────────────────────┘
```

**PRISMA numbers to track:**
```yaml
prisma_counts:
  databases:
    pubmed: 1245
    semantic_scholar: 892
    openalex: 654
    other: 47
  total_identified: 2838
  duplicates_removed: 423
  records_screened: 2415
  excluded_title_abstract: 1892
  sought_for_retrieval: 523
  not_retrieved: 31
  assessed_eligibility: 492
  excluded_fulltext: 423
    reason_1: 142
    reason_2: 98
    reason_3: 87
    reason_other: 96
  included: 69
```

### Step 7: Audit Trail
Maintain a complete record for reproducibility:

```yaml
audit_trail:
  review_id: "SR-2024-001"
  search_date: "2024-01-10"
  screening_start: "2024-01-12"
  screening_end: "2024-01-20"
  screeners: ["Reviewer A", "AI-assisted"]
  conflicts_resolved_by: "Reviewer B"
  total_screening_time: "8 hours"
  inter_rater_reliability:
    kappa: 0.87
    agreement_pct: 93
  notes: "..."
```

## Error Handling and User Checkpoints

### Checkpoints
- **After Step 2 (deduplication)**: present duplicate count and sample duplicates for user spot-check. Require confirmation before removing.
- **After Step 4 (title/abstract screening)**: present summary table showing include/exclude/maybe counts. Require explicit user approval before proceeding to full-text review.
- **After Step 5 (full-text review)**: present final included/excluded lists with reasons. Require user sign-off before generating PRISMA diagram.
- **At each stage**: if screening disagreement exceeds 20% (dual-screening mode), pause and discuss with user before continuing.

### Error Handling
- **Missing abstracts**: if >20% of records lack abstracts, warn user that title-only screening is less reliable. Suggest retrieving abstracts from S2 before screening.
- **Deduplication uncertainty**: if fuzzy title match confidence is between 85-92%, flag for manual review rather than auto-removing.
- **No full text available**: mark as "not retrieved" in PRISMA. Do not skip this step — it must appear in the flow diagram.
- **PRISMA number mismatch**: if counts don't balance (total ≠ included + excluded + pending), halt and ask user to resolve the discrepancy.

## Integration with Other Skills

- **semantic-scholar** / **pubmed-database** / **openalex-database** — Data sources for search results
- **paper-reader** — Full-text extraction for full-text review stage
- **quality-assessment** — Quality assessment of included studies
- **evidence-synthesis** — Final synthesis of included studies
- **research-gaps** — Analyze excluded studies for gap patterns

## Additional Resources

### Reference Files
- **`references/prisma-specification.md`** — PRISMA 2020 checklist and reporting requirements

### Scripts
- **`scripts/deduplicate.py`** — Deduplicate search results across databases
- **`scripts/prisma_report.py`** — Generate PRISMA flow diagram from screening data
