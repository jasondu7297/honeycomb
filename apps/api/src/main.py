from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.memory.router import router as memory_router
from src.workflows.router import router as workflows_router
from src.utils.extract_state_fields import parse_all_snapshots
from fastapi.responses import JSONResponse
from src.workflows.History import WorkflowHistory

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # Allow requests from your React app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample route
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

app.include_router(memory_router, prefix='/memory')
app.include_router(workflows_router, prefix='/history')

# apps/api/main.py (or wherever you set up FastAPI)
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from src.TestRunner import TestRunner

@app.post("/run")
async def run_test(request: Request):
    # Parse the JSON body for the user message
    data = await request.json()
    user_input = data.get("message", "Who was the 10th US president?")

    # Create a generator that yields output from TestRunner.run()
    def event_generator():
        runner = TestRunner()
        for output in runner.run(user_input):
            yield output

    return StreamingResponse(event_generator(), media_type="text/plain")


@app.get("/get_history")
def get_history() -> str:
    res = WorkflowHistory.get_history()
    print(res)
    return res

@app.post("/update")
def update(checkpoint_id: int, new_prompt: str):
    return WorkflowHistory.update(checkpoint_id, new_prompt)

# # Endpoint for retrieving state history as JSON
# @app.get("/state_history")
# async def state_history_endpoint():
#     state_history = parse_all_snapshots(input_string)
#     return JSONResponse(
#         content=state_history,
#         headers={
#             "Access-Control-Allow-Origin": "http://localhost:3000",
#             "Access-Control-Allow-Credentials": "true",
#         }
#     )
