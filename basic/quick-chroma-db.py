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
  query_texts=["your question goes here..."]
  n_results=1
)

print(results['documents'][0])


