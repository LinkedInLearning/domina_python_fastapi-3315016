from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.base import BaseHTTPMiddleware

from app.middleware import add_process_time_header
from app.routers import todo


app = FastAPI(
    title="TODO API",
)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo.router)


@app.get("/", tags=["home"])
async def home():
    return {
        "name": "TODO Rest API",
        "version": "1.0.0"
    }
