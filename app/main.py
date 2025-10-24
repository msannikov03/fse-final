from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Sentiment Analysis Service", version="0.1.0")

sentiment_pipeline = pipeline(
    "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=-1
)


class TextInput(BaseModel):
    text: str


class SentimentOutput(BaseModel):
    tag: str
    scores: list[float]


@app.get("/")
def root():
    return {"ok": True, "model": "sentiment-analysis", "version": "0.1.0"}


@app.post("/api/sentiment", response_model=SentimentOutput)
def analyze_sentiment(body: TextInput):
    """
    Analyze sentiment of input text.
    Returns label (POSITIVE/NEGATIVE) and confidence scores.
    """
    result = sentiment_pipeline(body.text)[0]
    label = result["label"]
    score = result["score"]

    if label == "POSITIVE":
        scores = [score, 1.0 - score]
    else:
        scores = [1.0 - score, score]

    return SentimentOutput(tag=label, scores=scores)
