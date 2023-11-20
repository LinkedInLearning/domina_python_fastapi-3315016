from fastapi import APIRouter, HTTPException, Path, status

from app.database import DB_DEPENDECY
from app.models.todo_model import Todo
from app.schemas.todo_schema import TodoSchema

router = APIRouter(
    prefix="/todo",
    tags=["todo"]
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_all(db: DB_DEPENDECY):
    return db.query(Todo).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(db: DB_DEPENDECY, todo_request: TodoSchema):

    todo_model = Todo(**todo_request.model_dump())
    
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return todo_model


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: DB_DEPENDECY, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(
        Todo.id==todo_id,
    ).first()
    if todo_model:
        return todo_model

    raise HTTPException(status_code=404, detail="Todo not found.")


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: DB_DEPENDECY,
    todo_request: TodoSchema,
    todo_id: int = Path(gt=0)
):
    todo_model = db.query(Todo).filter(
        Todo.id==todo_id,
    ).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return todo_model


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: DB_DEPENDECY, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(
        Todo.id==todo_id,
    ).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.query(Todo).filter(Todo.id==todo_id).delete()
    db.commit()
