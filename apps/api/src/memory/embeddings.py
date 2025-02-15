"""
Generates 384-dimensional text embeddings using the all-MiniLM-L6-v2 model from SentenceTransformers.
"""
from sentence_transformers import SentenceTransformer

N_DIMENSIONS = 384

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2", truncate_dim=N_DIMENSIONS)

def embedding_of_text(text: str):
    return model.encode(text).tolist()
