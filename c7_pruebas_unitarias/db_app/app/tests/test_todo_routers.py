from fastapi import status

from app.models.todo_model import Todo


def test_post_todo(client, test_db_session):

    payload = {
        "title": "Test TODO",
        "description": "This is a description",
        "priority": 4,
        "complete": False
    }
    response = client.post("/todo", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    todo = test_db_session.query(Todo).filter(Todo.title==payload["title"]).first()
    assert todo is not None
