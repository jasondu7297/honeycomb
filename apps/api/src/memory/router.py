"""
Defines API routes for managing client memory, including storing and retrieving text embeddings.
"""
from fastapi import APIRouter, Query

import src.memory.service as service
from src.memory.models import KNNResponse 

router = APIRouter()

@router.post("/conversation")
def remember_conversation(conversation: list[str] = Query(..., description="The conversation history to write to the user memory")):
    return service.remember_conversation(conversation)

@router.get("/knn", response_model=KNNResponse)
def get_knn(query: str = Query(..., description="Query text for which to find nearest neighbours"),
            k: int = Query(..., description="Number of nearest neighbours to retrieve")):
    return service.knn(query, k)
