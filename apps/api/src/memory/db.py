"""
Handles Elasticsearch indexing, storage, and k-NN search for text embeddings.
"""
from elasticsearch import Elasticsearch

from memory.embeddings import N_DIMENSIONS, embedding_of_text
from memory.models import Document

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Define the index mapping
index_name = "vector_index_v0"
mapping = {
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "embedding": {
                "type": "dense_vector",
                "dims": N_DIMENSIONS,   # Change based on your embedding model
                "index": True,
                "similarity": "cosine"  # Options: "l2_norm", "dot_product", "cosine"
            }
        }
    }
}

# Create the index
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)

def write(document: Document):
    es.index(index=index_name, body=document.__dict__)

def knn(query: str, k: int):
    query_embedding = embedding_of_text(query)

    # Search for similar documents
    knn_query = {
        "size": k,                              # Number of results to return
        "knn": {                                # k-NN search block
            "field": "embedding",               # Name of the dense_vector field
            "query_vector": query_embedding,    # Query embedding
            "k": 3,                             # Number of nearest neighbors to retrieve
            "num_candidates": 10                # More candidates = better recall, but slower
        },
        "_source": ["text"]                     # Only retrieve the "text" field
    }

    response = es.search(index=index_name, body=knn_query)
    return response

