# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec complete[cite: 3]

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.[cite: 3]

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.[cite: 3]

---

## Design Decisions

---

### Query approach

I will call _collection.query(query_texts=[query], n_results=n_results).
ChromaDB will automatically use the same embedding function we used during
ingestion to embed the query string, and then it will return the top n_results
closest chunks based on cosine distance.

---

### Return structure

A list of dictionaries. A single item in the return list will look like this:
{
"text": "When a 7 is rolled, no one collects any resources...",
"game": "Catan",
"distance": 0.142
}

---

### Handling the nested result structure

Because we are passing a single query string inside a list (query_texts=[query]),
ChromaDB returns nested lists of results. I must extract the data at index [0]
for each field to get the actual results.
Example: results["documents"][0], results["metadatas"][0], and results["distances"][0].

---

### Relevance threshold

I will not filter by distance score in this function. I will return all n_results
chunks. The tradeoff is that highly irrelevant chunks (distance > 0.6) might be
returned if the question doesn't match any rulebooks, but it is better to handle
this downstream in the LLM prompt (by telling the LLM to ignore irrelevant context)
rather than hardcoding a strict numerical cutoff here.

---

### Edge cases

(a) Empty collection: I will check _collection.count() first. If it's 0, return [].
(b) No good matches: Returns chunks anyway, but they will have high distance scores.
(c) Matches multiple games: Semantic search will return chunks from all matched games,
sorted purely by distance. The LLM will need to distinguish between them using the "game" metadata.

---

## Implementation Notes

**Test query and top result returned:**

Query: What happens when you roll a 7?
Top result game: Catan
Distance score: 0.142
Does it make sense? yes, it accurately fetched the robber rules.

**One thing about the query results that surprised you:**
The distance scores are highly sensitive to specific game terminology.

