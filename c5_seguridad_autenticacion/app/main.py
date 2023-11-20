from fastapi import FastAPI

from app.database  import engine

from app.models import todo_model
from app.models import user_model

from app.routers import auth_router
from app.routers import todo_router
from app.routers import user_router

app = FastAPI()

todo_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(todo_router.router)
app.include_router(user_router.router)
