from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    json_response = r.json()
    assert json_response.get("ok") is True
    assert json_response.get("model") == "sentiment-analysis"

def test_sentiment_positive():
    r = client.post("/api/sentiment", json={"text": "I love this! It's amazing!"})
    assert r.status_code == 200
    body = r.json()
    assert "tag" in body and "scores" in body
    assert isinstance(body["scores"], list)
    assert len(body["scores"]) == 2
    assert body["tag"] in ["POSITIVE", "NEGATIVE"]
    assert body["tag"] == "POSITIVE"
    assert body["scores"][0] > 0.5

def test_sentiment_negative():
    r = client.post("/api/sentiment", json={"text": "This is terrible and I hate it."})
    assert r.status_code == 200
    body = r.json()
    assert body["tag"] == "NEGATIVE"
    assert body["scores"][1] > 0.5

def test_sentiment_neutral():
    r = client.post("/api/sentiment", json={"text": "The sky is blue."})
    assert r.status_code == 200
    body = r.json()
    assert "tag" in body and "scores" in body