from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Sentiment Analysis Service", version="0.1.0")

# Setup templates and static files
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Load lightweight DistilBERT sentiment analysis model
# This runs on CPU and is optimized for laptops (~67MB)
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=-1,  # Use CPU
)


class TextInput(BaseModel):
    text: str


class SentimentOutput(BaseModel):
    label: str  # POSITIVE or NEGATIVE
    confidence: float  # 0.0 to 1.0
    scores: dict  # {"POSITIVE": 0.xx, "NEGATIVE": 0.xx}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    return {"ok": True, "model": "distilbert-base-uncased-finetuned-sst-2-english"}


@app.post("/api/sentiment", response_model=SentimentOutput)
def analyze_sentiment(body: TextInput):
    """
    Analyze sentiment of input text using DistilBERT model.
    Returns label (POSITIVE/NEGATIVE) and confidence scores.
    """
    result = sentiment_pipeline(body.text)[0]
    label = result["label"]
    score = result["score"]

    # Calculate both positive and negative scores
    if label == "POSITIVE":
        positive_score = score
        negative_score = 1.0 - score
    else:  # NEGATIVE
        positive_score = 1.0 - score
        negative_score = score

    return SentimentOutput(
        label=label,
        confidence=score,
        scores={"POSITIVE": positive_score, "NEGATIVE": negative_score},
    )
