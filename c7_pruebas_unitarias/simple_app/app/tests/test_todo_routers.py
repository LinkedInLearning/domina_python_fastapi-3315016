from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_all_ok():
    response = client.get(f"/todo")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_todo_ok():
    todo_id = 1
    response = client.get(f"/todo/{todo_id}")
    assert response.status_code == 200


def test_get_todo_not_found():
    todo_id = 5
    response = client.get(f"/todo/{todo_id}")
    assert response.status_code == 404


def test_create_todo():
    payload = { "description": "Test TODO", "complete": False}
    response = client.post(f"/todo", json=payload)
    assert response.status_code == 201

    response = client.get(f"/todo")
    assert len(response.json()) == 4

