from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_returns_ok():
    r = client.get("/health")
    print(r)
    assert r.status_code == 200
    body = r.json()
    assert body["api"] == "ok"
    assert "database" in body
    assert "redis" in body