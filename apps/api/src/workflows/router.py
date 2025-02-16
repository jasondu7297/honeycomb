"""
Defines API routes for managing history, including rollbacks, branches, and re-runs.
"""
from fastapi import APIRouter, Query

from src.workflows.History import WorkflowHistory
from langgraph.types import StateSnapshot
from src.utils.extract_state_fields import parse_all_snapshots
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/get")
def get_history() -> str:
    print("Getting history...")
    history = WorkflowHistory.get_history()
    state_history = parse_all_snapshots(history)
    return JSONResponse(
        content=state_history,
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Credentials": "true",
        }
    )
    
@router.post("/update")
def update(payload: dict):
    print("Updating history...")
    print(payload['checkpoint_id'])
    print(payload['new_prompt'])
    return WorkflowHistory.update(payload['checkpoint_id'], payload['new_prompt'])
