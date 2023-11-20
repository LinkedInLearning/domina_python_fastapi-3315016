from fastapi import APIRouter, HTTPException, status

from app.custom_exceptions import CustomException
from app.schemas.todo_schema import Todo


router = APIRouter(
    prefix="/todo",
    tags=["todo"]
)

TODO_LIST = [
    {"id": 1, "description": "Aprender Python", "complete": True},
    {"id": 2, "description": "Aprender FastAPI", "complete": False},
    {"id": 3, "description": "Tarea 3", "complete": False}
]


@router.get("")
async def get_all():
    filtered_todos = TODO_LIST
    return filtered_todos


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(todo_id: int):
    try:
        todo_data = next(todo for todo in TODO_LIST if todo["id"] == todo_id)
        return todo_data
    except:
        # raise HTTPException(
        #     status_code=404,
        #     detail="TODO not found",
        #     headers={"X-Error": "Header error"}
        # )
        raise CustomException(name=f"TODO id {todo_id}")


@router.post("", response_model=Todo, status_code=status.HTTP_201_CREATED,)
async def create_todo(data: Todo):
    TODO_LIST.append(data)
    return data
