"""
Defines the Document data model for storing text and embeddings in Elasticsearch.
"""
from pydantic import BaseModel

class Document(BaseModel):
    text : str 
    embedding : list[float]

# Pydantic response model for KNN queries
class KNNResult(BaseModel):
    text: str 
    score: float 

class KNNResponse(BaseModel):
    results: list[KNNResult]
