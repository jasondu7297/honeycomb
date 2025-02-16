"""
Defines API routes for managing history, including rollbacks, branches, and re-runs.
"""
from fastapi import APIRouter, Query

from src.workflows.History import WorkflowHistory

router = APIRouter()

@router.get("/get_history")
def get_history() -> str:
    return WorkflowHistory.get_history()

@router.post("/update")
def update(checkpoint_id: str, new_prompt: str):
    return WorkflowHistory.update(checkpoint_id, new_prompt)
