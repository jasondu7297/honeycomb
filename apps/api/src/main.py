from fastapi import FastAPI
# from pydantic import BaseModel

from src.memory.router import router as memory_router

app = FastAPI()

# Sample route
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

app.include_router(memory_router, prefix='/memory')
