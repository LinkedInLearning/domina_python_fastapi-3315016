from fastapi import FastAPI

from app.routers import todo
from app.custom_exceptions import CustomException, custom_exception_handler


app = FastAPI()
app.title = "Hello world API"

app.include_router(todo.router)
app.add_exception_handler(CustomException, custom_exception_handler)
