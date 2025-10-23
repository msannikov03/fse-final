from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Service", version="0.1.0")

class Input(BaseModel):
    values: list[float]

class Output(BaseModel):
    tag: str
    scores: list[float]

@app.get("/")
def root():
    return {"ok": True}

@app.post("/api", response_model=Output)
def api(body: Input):
    scores = [1.0, 0.0]
    return Output(tag="placeholder", scores=scores)