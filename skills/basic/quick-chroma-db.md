---
name: quick-chroma-db
description: "Use this when setting up a quick vector database, prototyping semantic search, or implementing simple RAG with ChromaDB"
---

# Quick ChromaDB Setup

Minimal setup for vector database with semantic search - good for prototyping.

## Example

```python
import chromadb

# Chroma generates embeddings with default model - good for quick and dirty prototyping

client = chromadb.Client()
collection = client.create_collection("my documents")

# Add documents manually to your collection

collection.add(
  documents=["important info 1", "important info 2"],
  ids=["doc1", "doc2"]
)

# Semantic search

results = collection.query(
  query_texts=["your question goes here..."],
  n_results=1
)

print(results['documents'][0])
```

## Key Points

- ChromaDB auto-generates embeddings with a default model
- No separate embedding step needed for quick prototypes
- `n_results` controls how many matches to return
- For production, configure a persistent directory and custom embeddings
