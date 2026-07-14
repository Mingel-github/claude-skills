---
name: citation-graph
description: This skill should be used when the user asks to "visualize citation network", "build citation graph", "find prior works", "find derivative works", "trace citation lineage", "map paper relationships", "find seminal papers", or mentions citation network visualization. Constructs and visualizes academic citation networks from Semantic Scholar and OpenAlex data.
---

# Citation Graph Visualization

Build and visualize citation networks to understand the intellectual lineage of research topics. Discover how ideas flow through the academic literature via citation relationships — from foundational prior works to recent derivative works.

## Core Concepts

### Citation Relationship Types
- **Prior Works** — Papers cited BY the target paper (references/bibliography)
- **Derivative Works** — Papers that cite the target paper (citations)
- **Co-citations** — Papers frequently cited together with the target
- **Bibliographic Coupling** — Papers sharing many references with the target

### Graph Structure
```
                    ┌──────────────┐
         ┌─────────│  Prior Work A │◄───┐
         │         └──────────────┘    │
┌────────┴───┐   ┌──────────────┐  ┌───┴──────────┐
│ Prior Work B│──►│ Target Paper │──►│Derivative X  │
└────────────┘   └──────┬───────┘  └──────────────┘
                        │          ┌──────────────┐
         ┌──────────────┘     ┌───►│Derivative Y  │
         │                    │    └──────────────┘
┌────────┴───┐          ┌────┴───────┐
│ Prior Work C│          │Derivative Z│
└────────────┘          └────────────┘
```

## Workflow

### Step 1: Identify Seed Paper(s)
Start with one or more papers as the graph origin:
- Provide paper title, DOI, or S2 Paper ID
- Use `semantic-scholar` skill to resolve paper IDs

**Input:** paper identifier (DOI, S2 ID, or title)
**Output:** resolved S2 Paper ID + metadata (title, year, citationCount)

### Step 2: Fetch Citation Data
**Input:** resolved S2 Paper ID
**Output:** two lists — `prior_works[]` and `derivative_works[]`, each with {paperId, title, authors, year, citationCount, isInfluential}

Using the S2 API:

**References (prior works):**
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/{id}/references?fields=title,authors,year,citationCount,isInfluential&limit=100"
```

**Citations (derivative works):**
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/{id}/citations?fields=title,authors,year,citationCount,isInfluential&limit=100"
```

### Step 3: Build the Graph Data
**Input:** `prior_works[]` and `derivative_works[]` from Step 2
**Output:** graph object with nodes[] and edges[] in a standard format

**Node attributes:**
- `id` — Paper ID
- `label` — Author (Year) short title
- `year` — Publication year
- `citations` — Citation count (for node sizing)
- `influential` — Boolean flag

**Edge attributes:**
- `type` — "cites" (target → prior) or "cited-by" (target ← derivative)
- `influential` — Whether this is an influential citation

### Step 4: Generate Visualization

#### Rendering Decision Tree

Determine the best output format based on available tools:

```
1. Check: is `dot` (Graphviz) installed?
   → YES: Use Option A (DOT) — best for static, publication-quality graphs
   → NO: continue

2. Check: is Python with networkx/matplotlib available?
   → YES: Use Option B (NetworkX script) — best for programmatic graph building
   → NO: continue

3. Fallback: Use Option C (HTML/D3.js) or output raw JSON
   → HTML: best for interactive exploration, no dependencies
   → JSON: best for importing into Cytoscape, Gephi, or other tools
```

When multiple options are available, prefer based on use case:
- **Publication figure** → Option A (DOT/PNG)
- **Exploratory analysis** → Option B (Python)
- **Sharing/interactive** → Option C (HTML)
- **External tool integration** → JSON format (see `references/graph-formats.md`)

#### Option A: Graphviz (DOT format)
Generate a DOT file and render with `dot`:

```
digraph citation_graph {
    rankdir=BT;  // Bottom-to-top: prior works at bottom
    node [shape=box, style=filled];

    // Prior works (bottom, blue)
    "PriorA" [label="Author A (2018)\nFoundational Work", fillcolor="#4ECDC4"];
    "PriorB" [label="Author B (2019)\nKey Method", fillcolor="#4ECDC4"];

    // Target (center, red)
    "Target" [label="Target Paper (2022)", fillcolor="#FF6B6B", penwidth=2];

    // Derivative works (top, orange)
    "DerivX" [label="Author X (2023)\nExtension", fillcolor="#FFE66D"];
    "DerivY" [label="Author Y (2024)\nApplication", fillcolor="#FFE66D"];

    // Edges
    "Target" -> "PriorA";
    "Target" -> "PriorB";
    "DerivX" -> "Target";
    "DerivY" -> "Target";
}
```

Render: `dot -Tpng graph.dot -o citation_graph.png`

#### Option B: Python (NetworkX + Matplotlib)
Use `scripts/build_citation_graph.py` to build and visualize:
```bash
python scripts/build_citation_graph.py --paper "DOI:10.1038/nature12373" --depth 2 --output citation_graph.png
```

#### Option C: HTML (D3.js force-directed graph)
For interactive exploration, generate an HTML file with D3.js force layout. See `references/d3-template.md`.

### Step 5: Analyze the Graph

**Input:** rendered graph from Step 4
**Output:** analysis report with key metrics and identified paper roles

**Key metrics to compute:**
- **In-degree** — How many papers cite this paper (impact)
- **Out-degree** — How many references this paper has (grounding)
- **Betweenness centrality** — Papers bridging different research communities
- **Temporal clustering** — Groups of papers from the same era

**Identify:**
- Seminal/foundational works (high in-degree, older)
- Bridge papers (high betweenness centrality)
- Research fronts (clusters of recent derivative works)
- Orphan papers (few connections — potential gap or novel direction)

## Multi-Paper Graph

To build a graph from multiple seed papers:

1. Fetch references and citations for each seed
2. Merge overlapping nodes (same paper cited by multiple seeds)
3. Weight edges by co-occurrence frequency
4. This reveals shared intellectual heritage and divergent paths

## Depth Control

Control graph expansion depth:
- **Depth 1** — Direct references + citations only (typically 50-200 nodes)
- **Depth 2** — Expand the top-N most-cited depth-1 papers (100-500 nodes)
- **Depth 3+** — Only for broad field mapping (use with caution, exponential growth)

**Node budget strategy:**
1. Start with Depth 1. Count total nodes.
2. If > 100 nodes, apply filters in priority order:
   - Remove non-influential citations with < 10 citations (least important)
   - Restrict year range to last 10 years
   - Keep only the top-20 most-cited prior works and top-30 most-cited derivative works
3. If still > 100 after filtering, ask user to choose: split into sub-graphs OR reduce depth.
4. Never render > 150 nodes — readability collapses.

For readability, target **50-100 nodes** in the visualization. Filter by:
- Citation count threshold (recommended: ≥ 5 citations)
- Year range (recommended: last 10-15 years)
- Influential citations only (use `isInfluential=true` filter)

## Error Handling and User Checkpoints

### Checkpoints
- **Before expanding beyond depth 1**: show estimated total node count. If estimated >200 nodes, warn user and ask to set filter thresholds (citation count, year range, or influential-only).
- **After Step 2 (fetch citation data)**: present summary stats (N references, N citations, % influential). Ask user whether to proceed or adjust limits.
- **Before rendering**: if the graph has >100 nodes, warn that readability degrades. Suggest filtering strategies or splitting into sub-graphs.

### Error Handling
- **Paper not found in S2**: if the seed paper ID returns 404, try alternative ID formats (DOI, PMID, title search). If all fail, report to user with suggested alternatives.
- **Rate limiting during bulk fetch**: if HTTP 429 encountered during multi-paper graph building, pause and report progress. Suggest using API key or reducing batch size.
- **Graphviz not installed**: if `dot` command fails, fall back to JSON output format. Provide the JSON file and instructions for the user to render locally.
- **Disconnected components**: if the citation graph has isolated sub-graphs (no path to target), flag these separately. They may represent parallel research threads rather than directly related work.

## Integration with Other Skills

- **semantic-scholar** — Primary data source for citation data
- **scientific-skills:openalex-database** — Alternative data source with different coverage
- **evidence-synthesis** — Use citation graph to identify key papers for synthesis
- **research-trends** — Overlay temporal trends on the citation graph

## Additional Resources

### Reference Files
- **`references/graph-formats.md`** — Detailed format specifications (DOT, GEXF, JSON)

### Scripts
- **`scripts/build_citation_graph.py`** — Python script to build and render citation graphs from S2 API data
