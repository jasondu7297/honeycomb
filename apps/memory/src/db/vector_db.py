from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

N_DIMENSIONS = 384 

# Define the index mapping
index_name = "vector_index_v0"
mapping = {
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "embedding": {
                "type": "dense_vector",
                "dims": N_DIMENSIONS,  # Change based on your embedding model
                "index": True,
                "similarity": "cosine"  # Options: "l2_norm", "dot_product", "cosine"
            }
        }
    }
}

# Create the index
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)


from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2", truncate_dim=N_DIMENSIONS)

# Sample text
texts = [
    "Elasticsearch is a powerful search engine.",
    "Vector search enables semantic similarity queries.",
    "I love AI and machine learning."
]

# Convert texts to embeddings
documents = [
    {"text": text, "embedding": model.encode(text).tolist()}
    for text in texts
]

# Index the documents
for i, doc in enumerate(documents):
    es.index(index=index_name, id=i, body=doc)

# Query text
query_text = "AI-powered search engines"
query_embedding = model.encode(query_text).tolist()

# Search for similar documents
knn_query = {
    "size": 3,  # Number of results to return
    "knn": {  # k-NN search block
        "field": "embedding",  # Name of the dense_vector field
        "query_vector": query_embedding,  # Query embedding
        "k": 3,  # Number of nearest neighbors to retrieve
        "num_candidates": 10  # More candidates = better recall, but slower
    },
    "_source": ["text"]  # Only retrieve the "text" field
}


response = es.search(index=index_name, body=knn_query)
print(response)

# Display results
for hit in response["hits"]["hits"]:
    print(f"Score: {hit['_score']}, Text: {hit['_source']['text']}")