---
name: cosine-similarity
description: "Use this when implementing vector similarity, comparing embeddings, or building semantic search from scratch"
---

# Cosine Similarity for Embeddings

Calculate similarity between vectors - the foundation of semantic search and RAG.

## Example

```python
import numpy as np

def cosine_similarity(vec1, vec2):
  # Classic dot product
  dot_product = np.dot(vec1, vec2)

  # Measuring magnitude
  mag1 = np.sqrt(np.sum(vec1 ** 2))
  mag2 = np.sqrt(np.sum(vec2 ** 2))

  # The magic...
  similarity = dot_product / (mag1 * mag2)
  return similarity


# Usage example
embedding1 = np.array([0.1, 0.2, 0.3, 0.4])
embedding2 = np.array([0.15, 0.25, 0.35, 0.45])

similarity = cosine_similarity(embedding1, embedding2)
print(f"Similarity: {similarity}")  # Close to 1.0 = very similar
```

## Key Points

- **Dot product**: Measures alignment between vectors
- **Magnitude**: Length of vector (L2 norm)
- **Result range**: -1 (opposite) to 1 (identical)
- Higher similarity = more semantically related
- Used to rank search results in RAG systems
- Most vector DBs compute this automatically, but understanding helps debugging
