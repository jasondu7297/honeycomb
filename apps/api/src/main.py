from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from src.memory.router import router as memory_router
from src.runner import Runner
from src.workflows.router import router as workflows_router
from src.utils.extract_state_fields import parse_all_snapshots
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

@app.post("/run")
async def run(request: Request):
    # Parse the JSON body for the user message
    data = await request.json()
    user_input = data.get("message", "Who was the 10th US president?")

    # Create a generator that yields output from TestRunner.run()
    def event_generator():
        runner = Runner()
        for output in runner.run(user_input):
            yield output

    return StreamingResponse(event_generator(), media_type="text/plain")
