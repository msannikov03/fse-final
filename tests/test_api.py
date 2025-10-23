from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("ok") is True

def test_api_placeholder():
    r = client.post("/api", json={"values":[1.0,2.0]})
    assert r.status_code == 200
    body = r.json()
    assert "tag" in body and "scores" in body
    assert isinstance(body["scores"], list)