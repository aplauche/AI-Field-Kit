import numpy as np

# How to compare embeddings for similarity manually

def cosine_similarity(vec1, vec2):
  # classic dot product
  dot_product = np.dot(vec1, vec2)

  # Measuring magnitude
  mag1 = np.sqrt(np.sum(vec1 ** 2))
  mag2 = np.sqrt(np.sum(vec2 ** 2))

  # the magic...
  similarity = dot_product / (mag1 * mag2)
  return similarity