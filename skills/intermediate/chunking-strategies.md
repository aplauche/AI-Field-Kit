---
name: chunking-strategies
description: "Use this when implementing document chunking for RAG, splitting text into chunks with overlap, or preparing documents for vector databases"
---

# Document Chunking Strategies

Different chunking approaches for different content types - token-based for consistency, sentence-based for coherence.

## Example

```python
class Chunker:
  def __init__(self, chunk_size=500, overlap=50):
    self.chunk_size = chunk_size
    self.overlap = overlap

  def chunk_by_tokens(self, text, tokenizer):
    """When you want all chunks to be the same token length"""
    tokens = tokenizer.encode(text)
    chunks = []

    for i in range(0, len(tokens), self.chunk_size - self.overlap):
      chunk_tokens = tokens[i:i + self.chunk_size]
      chunk_text = tokenizer.decode(chunk_tokens)
      chunks.append(chunk_text)

    return chunks

  def chunk_by_sentence(self, text):
    """Split at a sentence boundry for coherence"""
    sentences = text.split(". ")
    chunks = []
    current_chunk_sentences = []
    current_size = 0

    for sentence in sentences:
      sentence_size = len(sentence.split())
      if current_size + sentence_size > self.chunk_size:
        chunks.append('. '.join(current_chunk_sentences) + '.')
        # for overlap include in next chunk too
        current_chunk_sentences = [sentence]
        current_size = sentence_size
      else:
        current_chunk_sentences.append(sentence)
        current_size += sentence_size

    if current_chunk_sentences:
      chunks.append('. '.join(current_chunk_sentences))

    return chunks

  def chunk_by_arbitrary(self, text):
    """Implement your own arbitrary chunker by using the above as a base"""
```

## Key Points

- **Token-based**: Consistent chunk sizes, good for embedding models with token limits
- **Sentence-based**: Preserves semantic coherence, better for readable content
- **Overlap**: Prevents losing context at chunk boundaries (typically 10-20% of chunk size)
- For structured content (markdown, code), consider custom chunkers that respect structure
