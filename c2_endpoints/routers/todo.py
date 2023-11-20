from fastapi import APIRouter, HTTPException, Path, status, UploadFile
from pydantic import BaseModel, Field
from typing import Annotated, Optional, Union


router = APIRouter(
    prefix="/todo",
    tags=["todo"]
)

class Todo(BaseModel):
    id: Optional[int] = None
    description: str = Field(min_length=5, max_length=500)
    complete: bool = Field(default=False)


TODO_LIST = [
    {"id": 1, "description": "Aprender Python", "complete": True},
    {"id": 2, "description": "Aprender FastAPI", "complete": False},
    {"id": 3, "description": "Tarea 3", "complete": False}
]


@router.get("")
async def get_all(completed: Union[bool, None] = None):
    filtered_todos = TODO_LIST
    if completed is not None:
        filtered_todos = list(filter(
            lambda todo: todo["complete"] == completed, TODO_LIST
        ))
    return filtered_todos


@router.get("/{todo_id}")
async def get_todo(todo_id: int):
    try:
        todo_data = next(todo for todo in TODO_LIST if todo["id"] == todo_id)
        return todo_data
    except:
        raise HTTPException(status_code=404, detail="TODO not found")


# TODO with model definition
@router.post(
    "",
    response_model=Todo,
    name="Create TODO",
    summary="Create a TODO element",
    description="Creates a TODO element given an id a description and a complete status",
    response_description="Created TODO element",
    status_code=status.HTTP_201_CREATED,
    # deprecated=True
)
async def create_todo(data: Todo):
    """ Creates a TODO element, requires the following data to be created:
    - id (int): Optional, number that identifies the TODO element
    - description (str):  Required, string with the description of the TODO element
    - complete (bool): True if TODO es complete, else False. Default value is False
    """
    TODO_LIST.append(data)
    return data


@router.post("/{todo_id}/file")
async def upload_todo_file(
    todo_id: Annotated[int, Path()],
    file: UploadFile
):
    try:
        todo_data = next(todo for todo in TODO_LIST if todo["id"] == todo_id)
        todo_data["file_name"] = file.filename
        print(file.content_type)
        print(file.file)
        file_content = await file.read()
        return todo_data
    except:
        raise HTTPException(status_code=404, detail="TODO not found")
