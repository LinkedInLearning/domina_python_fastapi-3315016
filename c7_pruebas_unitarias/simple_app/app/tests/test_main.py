from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"name": "TODO Rest API", "version": "1.0.0"}
