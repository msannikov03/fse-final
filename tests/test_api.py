from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "Text Analysis Service" in r.text
    assert "<!DOCTYPE html>" in r.text


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("ok") is True


def test_api_short_text():
    r = client.post("/api", json={"text": "Hello world"})
    assert r.status_code == 200
    body = r.json()
    assert "tag" in body and "scores" in body and "stats" in body
    assert isinstance(body["scores"], list)
    assert "Short Text" in body["tag"]
    assert body["stats"]["words"] == 2


def test_api_positive_text():
    r = client.post("/api", json={"text": "This is amazing and wonderful! I love it."})
    assert r.status_code == 200
    body = r.json()
    assert "Positive" in body["tag"]
    assert body["scores"][0] > 0.5  # Positive sentiment score


def test_api_negative_text():
    r = client.post("/api", json={"text": "This is terrible and awful. I hate it."})
    assert r.status_code == 200
    body = r.json()
    assert "Negative" in body["tag"]
    assert body["scores"][0] < 0.5  # Negative sentiment score


def test_api_stats():
    text = "Hello. How are you?"
    r = client.post("/api", json={"text": text})
    assert r.status_code == 200
    body = r.json()
    assert body["stats"]["words"] == 4
    assert body["stats"]["sentences"] == 2
    assert body["stats"]["characters"] == len(text)
