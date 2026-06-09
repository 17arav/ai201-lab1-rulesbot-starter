# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec complete[cite: 2]

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.[cite: 2]

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user.[cite: 2]

---

## Design Decisions

---

### Context formatting

I will loop through the retrieved chunks and format them with clear markers:
=== START CHUNK (Game: [Game Name]) ===
[Chunk Text]
=== END CHUNK ===

---

### System prompt — grounding instruction

Answer the query using ONLY the rule text provided below. Do not assume, guess, or bring in outside knowledge about board games. If the answer cannot be completely derived from the provided chunks, reply exactly with: "I'm sorry, but I cannot find the answer to that question in the provided rule books."

---

### System prompt — citation instruction

State clearly which game the rule applies to at the beginning or end of your answer, matching the game label provided in the context.

---

### Fallback behavior

"I'm sorry, but I cannot find the answer to that question in the provided rule books."

---

### Handling low-relevance chunks

I will pass all retrieved chunks to the LLM but let the strict system grounding prompt force the LLM to ignore chunks that do not explicitly contain the answer.

---

### Message structure

messages = [
{"role": "system", "content": SYSTEM_GROUNDING_AND_CITATION_PROMPT},
{"role": "user", "content": f"Context:\n{formatted_context}\n\nQuestion: {query}"}
]

---

## Implementation Notes

**Test query and response:**

Query: How do you get out of Jail in Monopoly?
Response: According to the Monopoly rules, you can get out of jail by paying a $50 fine, rolling doubles, or using a Get Out of Jail Free card.
Correctly grounded? yes
Cited the right game? yes

**One thing you changed from your original spec after seeing the actual output:**
Emphasized the exact fallback string in the system prompt so the model didn't try to synthesize loose explanations.

