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

    def __str__(self):
        return self.text

class KNNResponse(BaseModel):
    results: list[KNNResult]

    def __str__(self):
        return "\n\n".join(str(result) for result in sorted(self.results, key=lambda result: result.score, reverse=True))
