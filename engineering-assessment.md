# Software Engineering - Technical Assessment

### The Challenge Prompt: Next Construction Solutions

**Subject:** Urgent: Core Search Logic for Next Builders Field App

We’ve just started a project with **Next Builders**, a large commercial construction firm. They are drowning in documents: specs, safety logs, material invoices, and regulation codes.

Their Site Superintendents need a way to quickly find critical information on their iPads while on the job site. A simple keyword search is failing because they often describe problems ("how to fix cracked foundation") rather than using exact terminology. However, sometimes they *do* need exact matches for specific regulation codes (e.g., "OSHA 1926.501").

**Your Task:** By end of day, we need a Proof of Concept (PoC) Python script that demonstrates a **Hybrid Search** pipeline combining semantic understanding with keyword precision.

### The Dataset (Sample `documents.json`)

*Use this small, representative dataset for your PoC.*

```json
[
  {
    "id": "doc_1",
    "type": "Safety Regulation",
    "content": "OSHA 1926.501(b)(1): Each employee on a walking/working surface (horizontal and vertical surface) with an unprotected side or edge which is 6 feet (1.8 m) or more above a lower level shall be protected from falling by the use of guardrail systems, safety net systems, or personal fall arrest systems."
  },
  {
    "id": "doc_2",
    "type": "Incident Report",
    "content": "Site: West Creek Hangar. Date: Oct 12. A worker slipped on an icy patch near the north scaffolding tower. No serious injury, but requested review of winter footwear protocols and salting procedures for walkways."
  },
  {
    "id": "doc_3",
    "type": "Material Spec",
    "content": "ASTM C150 Type I Portland Cement. General-purpose cement suitable for all uses where the special properties of other types are not required. Used in pavement, sidewalks, reinforced concrete buildings, bridges, railway structures, tanks, and reservoirs."
  },
  {
    "id": "doc_4",
    "type": "Procedure Manual",
    "content": "Cold Weather Concreting: When air temperature is below 40°F (4°C), heaters must be used to ensure the concrete does not freeze before curing. Insulating blankets should be applied immediately after finishing."
  },
  {
    "id": "doc_5",
    "type": "Technical Bulletin",
    "content": "Update regarding high-strength bolts. Effective immediately, switch from A325 Type 1 to A490 bolts for all primary steel structural connections on the Downtown Highrise project due to revised load calculations."
  }
]
```

### Technical Requirements

Please write a Python script that fulfills these requirements. You may use standard libraries like `scikit-learn` (for TF-IDF/keyword simulation), `numpy` (for calculations),  `sentence-transformers` (for embeddings) or others you are familiar with.

**1. Setup & Ingestion**

- Load the sample documents.
- Generate embeddings for these documents using a standard, open-source model.

**2. Implement Three Search Functions**
You need to define Python functions that take a user `query` string and return ranked results.

- **`keyword_search(query, documents, k=3)`:**
    - Should prioritize exact matches of acronyms (OSHA, ASTM) and specific numbers.
    - *Note: For this PoC, any simple keyword search is acceptable (TD-IF or BM25).*
- **`semantic_search(query, documents, k=3)`:**
    - Convert the query to an embedding and use cosine similarity to find the nearest document embeddings.
- **`hybrid_search(query, documents, k=3)`:**
    - This is the core of the challenge. Run both keyword and semantic searches.
    - **Crucial:** Implement a fusion strategy to combine the results into a single, re-ranked list. Do NOT just average the raw scores. Use **Reciprocal Rank Fusion (RRF)** or explain and implement any justified alternative.

**3. The Test Queries**
We will be testing your hybrid search works by printing the top results for a few distinct search scenarios. You can use the following for testing:

- **Scenario A (Keyword Heavy):** `query = "specs for ASTM C150 cement"`
    - *Expected Top Result:* `doc_3`
- **Scenario B (Semantic Intent):** `query = "what do we do if pouring concrete when it's freezing outside?"`
    - *Expected Top Result:* `doc_4` (Keyword search might fail here as "freezing" isn't in the doc, but "40°F" and "Cold Weather" are).