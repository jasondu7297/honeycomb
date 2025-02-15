from typing import TypedDict
# from langgraph.graph import MessagesState, END

class StepState(TypedDict):
    user_query: str
    agent: str
    result: str                     # Collect outputs from each step
    done: bool                      # True if we've finished
    last_error: str | None          # For error handling, if any


class Workflow:
    steps: list[StepState]