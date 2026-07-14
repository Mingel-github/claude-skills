---
name: semantic-scholar
description: This skill should be used when the user asks to "search Semantic Scholar", "find papers on S2", "get paper citations", "find related papers", "get paper recommendations", "look up a paper by DOI", "find papers by author", "get TLDR summary", or mentions Semantic Scholar API. Provides access to 230M+ academic papers via the Semantic Scholar Academic Graph API and Recommendations API.
---

# Semantic Scholar Integration

Integrate with the Semantic Scholar (S2) API for academic paper discovery, citation analysis, and research recommendations. S2 indexes 230M+ papers across all scientific disciplines with AI-enhanced metadata.

## Core Capabilities

### Paper Search
Search papers by keyword with advanced filtering:

```
GET https://api.semanticscholar.org/graph/v1/paper/search
```

**Key parameters:**
- `query` — Full-text search (supports AND, OR, negation, phrases, fuzzy matching)
- `year` — Filter by year or range (e.g., `2020-2024`)
- `minCitationCount` — Minimum citation threshold
- `venue` — Filter by publication venue (e.g., `Nature,Science`)
- `fieldsOfStudy` — Filter by discipline
- `openAccessPdf` — Restrict to open access papers
- `sort` — Sort by `citationCount:desc`, `publicationDate:desc`, etc.
- `fields` — Comma-separated fields to return

**Recommended fields:** `paperId,title,abstract,authors,year,citationCount,referenceCount,venue,publicationDate,openAccessPdf,tldr,externalIds`

**Example:**
```
GET /graph/v1/paper/search?query=CRISPR+gene+editing&fields=title,abstract,authors,year,citationCount,tldr&year=2022-2024&sort=citationCount:desc&limit=20
```

### Paper Details
Retrieve detailed information about a specific paper:

```
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}
```

**Supported ID formats:**
- S2 Paper ID (SHA hash)
- `CorpusId:<id>`
- `DOI:<doi>` (e.g., `DOI:10.1038/nature12373`)
- `ARXIV:<id>` (e.g., `ARXIV:2106.15928`)
- `PMID:<id>` (PubMed ID)
- `PMCID:<id>` (PubMed Central ID)
- `URL:<url>`

**Example:**
```
GET /graph/v1/paper/DOI:10.1038/nature12373?fields=title,abstract,authors,year,citationCount,references,citations,tldr
```

### Citations (Papers that cite this paper)
```
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations?fields=title,authors,year,citationCount&limit=100
```

### References (Papers cited by this paper)
```
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references?fields=title,authors,year,citationCount,isInfluential&limit=100
```

### Paper Recommendations
Discover related papers based on a seed paper:

```
GET https://api.semanticscholar.org/recommendations/v1/papers/forpaper/{paper_id}?limit=50&fields=title,abstract,authors,year,citationCount
```

For multiple seed papers (positive and negative examples):
```
POST https://api.semanticscholar.org/recommendations/v1/papers/
Body: {"positivePaperIds": ["id1","id2"], "negativePaperIds": ["id3"]}
```

### Batch Paper Retrieval
Retrieve up to 500 papers at once:

```
POST https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,abstract,authors,year,citationCount
Body: {"ids": ["DOI:10.1038/nature12373", "ARXIV:2106.15928"]}
```

### Author Search
```
GET https://api.semanticscholar.org/graph/v1/author/search?query=Yoshua+Bengio
GET https://api.semanticscholar.org/graph/v1/author/{author_id}?fields=name,paperCount,citationCount,hIndex
```

## TLDR Summaries

The `tldr` field provides AI-generated single-sentence summaries of papers. Always include this field when available — it is one of S2's most distinctive features.

## Rate Limits

- Unauthenticated: 100 requests per 5 minutes
- With API key (header `x-api-key`): 1 request per second (higher tiers available)
- Register at https://www.semanticscholar.org/product/api#api-key

## Workflow Patterns

### Literature Discovery Workflow
1. Start with a keyword search to identify seed papers
2. Use recommendations to find related papers
3. Fetch citations and references for key papers
4. Use batch retrieval to get details for collected paper IDs

### Citation Tracing Workflow
1. Get paper details for the target paper
2. Fetch references to find prior/ancestor works
3. Fetch citations to find derivative/successor works
4. Identify influential citations via `isInfluential` field

### Author-Centered Discovery
1. Search for the author by name
2. Get author details (paper count, h-index, citation count)
3. Fetch author's papers
4. Get recommendations based on their key papers

## Error Handling and User Checkpoints

### Checkpoints
- **Before batch operations** (>20 papers): pause and show estimated API call count. Require user confirmation.
- **Before pagination**: if `token` field indicates more results, ask user whether to fetch more or proceed with current set.
- **Before deep citation traversal** (citations of citations): warn about exponential growth. Ask user to set a depth limit.

### Error Handling
- **HTTP 429 (Rate Limited)**: stop immediately. Report current progress. Wait for user to provide API key or decide to continue later.
- **HTTP 404 (Paper not found)**: if DOI/PMID lookup fails, try alternative ID formats (CorpusId, URL). If all fail, skip and log.
- **Empty results**: if search returns 0 papers, suggest broadening query, removing filters, or trying alternative keywords.
- **Missing fields**: if requested `tldr` or `abstract` is null, note the gap and proceed without it. Do not fabricate summaries.

## Implementation Notes

- Use `curl` or Python `requests` for API calls
- Always request the `tldr` field for concise paper summaries
- Use batch endpoints to minimize API calls
- Cache paper IDs for follow-up queries
- The `isInfluential` flag in references/citations highlights key papers

## Additional Resources

### Reference Files
- **`references/api-reference.md`** — Complete API endpoint reference with all parameters and response schemas

### Scripts
- **`scripts/s2_search.py`** — Python utility for common S2 API operations (search, detail, citations, recommendations)
