---
name: research-trends
description: This skill should be used when the user asks to "find trending papers", "analyze research trends", "discover emerging topics", "find hot research areas", "track citation velocity", "identify rising papers", or "what's new in [field]". Analyzes publication and citation patterns to identify trending research directions and emerging topics.
---

# Research Trends Analysis

Identify emerging research directions, trending papers, and hot topics by analyzing publication volume, citation velocity, and temporal patterns. This skill helps researchers stay ahead of their field rather than chasing established knowledge.

## Core Metrics

### Citation Velocity
Rate at which a paper accumulates citations over time:
```
Citation Velocity = Citations in last 12 months / Months since publication
```
High velocity relative to age indicates a trending paper.

### Citation Acceleration
Whether a paper's citation rate is increasing or decreasing:
```
Acceleration = (Citations in recent 6 months) - (Citations in prior 6 months)
```
Positive acceleration = gaining momentum.

### Publication Volume Growth
Rate of increase in publications on a topic:
```
Growth Rate = (Papers in year N) / (Papers in year N-1)
```
Growth rate > 1.5 suggests an emerging hot topic.

## Workflow

### Step 1: Define the Analysis Scope
- **Topic-based**: "What's trending in CRISPR gene editing?"
- **Field-based**: "What are the hot topics in computational biology?"
- **Author-based**: "What new directions is [researcher] pursuing?"
- **Venue-based**: "What were the most cited papers from NeurIPS 2024?"

### Step 2: Retrieve Temporal Data

**Input:** search query string, year range (e.g., `2020-2026`), max results
**Output:** list of papers with `{title, authors, year, citationCount, publicationDate, tldr, fieldsOfStudy}`

Using S2 API with time-based queries:

```bash
# Papers from specific years, sorted by citation count
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=CRISPR&year=2024-2026&sort=citationCount:desc&limit=100&fields=title,authors,year,citationCount,publicationDate,tldr,fieldsOfStudy"

# Recent papers (by publication date)
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=CRISPR&sort=publicationDate:desc&limit=50&fields=title,authors,year,citationCount,publicationDate,tldr,fieldsOfStudy"

# Bulk year-by-year: repeat for each year to get volume counts
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=CRISPR&year=2020&limit=1&fields=title"  # Check total via response "total" field
```

Using OpenAlex for volume analysis:
```bash
# Works count by year (grouped)
curl "https://api.openalex.org/works?filter=display_name.search:CRISPR&group_by=publication_year"
```
- Cross-reference S2 individual paper data with OpenAlex volume statistics
- If query returns >10,000 results, warn user to narrow scope (see Error Handling)

### Step 3: Compute Trend Metrics

**Input:** paper list from Step 2
**Output:** paper list enriched with `{age, velocity, acceleration, heat_score, pattern}`

For each paper in the result set, compute sequentially:

1. **Age** = (Current year - Publication year) × 12 + (Current month - Publication month). Minimum age = 1 month.
2. **Citation Velocity** = Total citations / Age (citations per month). Threshold: velocity > 5.0/mo = trending for papers < 2 years old; > 2.0/mo = trending for papers 2-5 years old.
3. **Citation Acceleration** = Recent citations (estimated) minus prior period. Positive acceleration = gaining momentum.
4. **Heat Score** = Weighted combination:

```
Heat = (Citation_Velocity * 2.0) + (Total_Citations / 100.0) + (1.0 / Age_in_months * 12)
```

**Heat Score interpretation:**
| Heat Score | Interpretation |
|---|---|
| > 15 | Explosive — immediate high-impact paper |
| 8–15 | Hot — rapidly gaining attention |
| 3–8 | Warm — solid and growing |
| < 3 | Cold — stable or declining interest |

5. **Pattern Classification** based on age and velocity:
   - **Burst** (age < 12 months, heat > 8): immediate impact
   - **Sleeper** (age 24-48 months, velocity increasing > 50% vs prior year): overlooked but rising
   - **Steady Classic** (age > 60 months, velocity 1-3/mo): foundational
   - **Flash** (initial heat > 10, but velocity declining > 30% YoY): trendy but fading

### Step 4: Identify Emerging Topics

**Input:** enriched paper list from Step 3
**Output:** list of topic clusters with `{label, paper_count, growth_rate, papers, is_emerging}`

Topic clustering procedure:

1. **Extract keywords**: from titles and TLDR fields, tokenize words > 4 characters, remove stopwords. Use `fieldsOfStudy` as secondary labels.
2. **Build co-occurrence matrix**: for each pair of keywords, count how many papers contain both. Keep pairs with co-occurrence ≥ 3.
3. **Form clusters**: group keywords connected by co-occurrence (single-link clustering, threshold ≥ 3 shared papers). Assign each cluster a descriptive label from its top keywords.
4. **Calculate growth per cluster**:
   ```
   Cluster Growth = (Papers in most recent year) / (Papers in prior year)
   ```
   - Growth > 1.5 → emerging (new hot topic)
   - Growth < 0.7 → declining (possible dead end)
   - Cluster appearing only in most recent year → nascent (flag for monitoring)
5. **Filter**: remove clusters with < 3 papers (statistically unreliable). Present remaining sorted by growth rate descending.

**Topic indicators:**
- New keyword combinations appearing in recent papers
- Rapidly growing sub-clusters (growth > 1.5)
- Papers from ≥ 3 different research groups converging on similar topics

### Step 5: Generate Trend Report

```markdown
## Research Trends: [Topic/Field]

### Trending Papers (Last 12 Months)
| Rank | Paper | Heat Score | Citations | Velocity |
|------|-------|-----------|-----------|----------|
| 1    | Title | 8.7       | 150       | 12.5/mo  |
| 2    | Title | 7.2       | 89        | 7.4/mo   |

### Emerging Topics
1. **[Topic A]** — X papers in 2024 vs Y in 2023 (Z% growth)
2. **[Topic B]** — New keyword cluster appearing in 5+ recent papers

### Rising Authors
- Author X: 3 high-velocity papers in this area
- Author Y: Recent pivot to this topic with high-impact results

### Research Frontiers
- [Underexplored area with growing interest]
- [Novel method gaining rapid adoption]

### Declining Topics
- [Previously hot topic with decreasing publication rate]

### Field Summary
[2-3 paragraph overview of where the field is heading]
```

## Analysis Patterns

### The "Sleeper" Pattern
Paper published 2-3 years ago with low citations that suddenly shows high citation velocity — indicates a paper whose importance was initially overlooked.

### The "Burst" Pattern
Paper published <1 year ago with already high citation count — indicates immediate impact, likely a breakthrough or highly anticipated result.

### The "Steady Classic" Pattern
Paper published 5+ years ago with consistent citation rate — foundational work that continues to be relevant.

### The "Flash" Pattern
Paper with high initial citations that rapidly declined — likely a trendy but ultimately less impactful contribution.

## Temporal Analysis Techniques

### Publication Volume Over Time
Query papers by year to plot the growth curve of a research area. Use S2 bulk search or OpenAlex aggregation.

### Citation Network Evolution
Compare citation graphs at different time points to see how the intellectual landscape has shifted.

### Author Migration
Track when prominent researchers start publishing in new areas — a leading indicator of emerging trends.

## Error Handling and User Checkpoints

### Checkpoints
- **After Step 3 (compute trend metrics)**: present the heat score rankings and pattern classifications to user. Ask whether the top papers align with the user's domain knowledge.
- **Before Step 4 (identify emerging topics)**: present the keyword clusters. Require user confirmation that topic clustering makes sense before drawing conclusions about "emerging" vs "declining" areas.
- **Before Step 5 (trend report)**: show the report draft. Ask user to validate the "Rising Authors" and "Research Frontiers" sections, as these claims have the highest impact.

### Error Handling
- **Insufficient data for year-over-year comparison**: if fewer than 3 years of data are available, note that trend detection is unreliable. Present findings as "snapshot" rather than "trend".
- **Outlier papers**: if a single paper with extreme citation count (e.g., >10x the median) dominates the analysis, flag it and offer to recompute with and without the outlier.
- **Search query too broad**: if "Machine Learning" returns 100K+ papers, warn user that results are not representative. Suggest narrowing with sub-fields, venues, or year ranges.
- **Pattern classification confidence**: if a paper's pattern (Sleeper vs Burst) is ambiguous (e.g., age=14 months, velocity=8), present both possible classifications and let user decide.

## Integration with Other Skills

- **semantic-scholar** — Primary data source for paper search and citation data
- **scientific-skills:openalex-database** — Alternative data source with volume statistics
- **citation-graph** — Visualize how trending papers connect to the broader literature
- **paper-comparison** — Deep-dive into competing approaches in a hot area

## Additional Resources

### Reference Files
- **`references/trend-patterns.md`** — Detailed catalog of trend patterns and their interpretations

### Scripts
- **`scripts/analyze_trends.py`** — Python script for computing heat scores and generating trend reports
