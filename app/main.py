from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(title="Text Analysis Service", version="0.1.0")

# Setup templates and static files
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


class TextInput(BaseModel):
    text: str


class TextOutput(BaseModel):
    tag: str
    scores: list[float]
    stats: dict


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/api", response_model=TextOutput)
def api(body: TextInput):
    """
    Analyze text and return statistics and sentiment analysis.
    """
    text = body.text

    # Count words
    words = text.split()
    word_count = len(words)

    # Count characters
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", ""))

    # Count sentences (simple heuristic)
    sentence_endings = text.count(".") + text.count("!") + text.count("?")
    sentence_count = max(1, sentence_endings)

    # Simple sentiment analysis (based on word patterns)
    positive_words = [
        "good",
        "great",
        "excellent",
        "amazing",
        "wonderful",
        "fantastic",
        "love",
        "best",
        "awesome",
        "beautiful",
        "perfect",
        "happy",
        "nice",
    ]
    negative_words = [
        "bad",
        "terrible",
        "awful",
        "horrible",
        "worst",
        "hate",
        "poor",
        "sad",
        "disappointing",
        "ugly",
        "wrong",
    ]

    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    # Calculate sentiment score (0 to 1, where 1 is most positive)
    total_sentiment = positive_count + negative_count
    if total_sentiment > 0:
        sentiment_score = (positive_count + 0.5 * negative_count) / (
            total_sentiment * 1.5
        )
    else:
        sentiment_score = 0.5  # Neutral

    # Determine category
    if word_count < 10:
        category = "Short Text"
    elif word_count < 50:
        category = "Medium Text"
    else:
        category = "Long Text"

    # Add sentiment to category
    if sentiment_score > 0.6:
        category += " (Positive)"
    elif sentiment_score < 0.4:
        category += " (Negative)"
    else:
        category += " (Neutral)"

    stats = {
        "words": word_count,
        "characters": char_count,
        "characters_no_spaces": char_count_no_spaces,
        "sentences": sentence_count,
    }

    return TextOutput(
        tag=category, scores=[sentiment_score, 1.0 - sentiment_score], stats=stats
    )
