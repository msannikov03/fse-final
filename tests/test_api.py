import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "Sentiment Analysis" in r.text
    assert "<!DOCTYPE html>" in r.text


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body.get("ok") is True
    assert "distilbert" in body.get("model", "").lower()


def test_sentiment_positive():
    r = client.post("/api/sentiment", json={"text": "I love this! It's amazing!"})
    assert r.status_code == 200
    body = r.json()
    assert "label" in body
    assert "confidence" in body
    assert "scores" in body
    assert body["label"] == "POSITIVE"
    assert body["confidence"] > 0.5
    assert body["scores"]["POSITIVE"] > body["scores"]["NEGATIVE"]


def test_sentiment_negative():
    r = client.post("/api/sentiment", json={"text": "This is terrible and I hate it."})
    assert r.status_code == 200
    body = r.json()
    assert body["label"] == "NEGATIVE"
    assert body["confidence"] > 0.5
    assert body["scores"]["NEGATIVE"] > body["scores"]["POSITIVE"]


def test_sentiment_neutral():
    r = client.post("/api/sentiment", json={"text": "The sky is blue."})
    assert r.status_code == 200
    body = r.json()
    assert body["label"] in ["POSITIVE", "NEGATIVE"]
    assert 0.0 <= body["confidence"] <= 1.0


def test_sentiment_long_text():
    long_text = "This product exceeded all my expectations! The quality is outstanding and I'm very happy with my purchase. Highly recommended!"
    r = client.post("/api/sentiment", json={"text": long_text})
    assert r.status_code == 200
    body = r.json()
    assert body["label"] == "POSITIVE"
    assert body["scores"]["POSITIVE"] + body["scores"]["NEGATIVE"] == pytest.approx(
        1.0, abs=0.01
    )
