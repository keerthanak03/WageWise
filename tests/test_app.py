from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_usage():
    response = client.get("/usage")

    assert response.status_code == 200

    data = response.json()

    assert "total_requests" in data
    assert "prompt_tokens" in data
    assert "completion_tokens" in data
    assert "total_tokens" in data