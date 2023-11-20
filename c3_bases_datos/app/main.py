from fastapi import FastAPI

from app.database  import engine
from app.models import todo_model
from app.routers import todo_router

app = FastAPI()

todo_model.Base.metadata.create_all(bind=engine)

app.include_router(todo_router.router)
