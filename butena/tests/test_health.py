from fastapi.testclient import TestClient
from butena.app.core.main import get_app
client = TestClient(get_app())


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"message": "You are live"}





