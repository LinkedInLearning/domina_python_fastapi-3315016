from enum import Enum

from fastapi import FastAPI

from routers import support, todo


tags_info = [
    {
        "name": "home",
        "description": "Short description of the home tag",
        "externalDocs": {
            "description": "FastAPI docs",
            "url": "https://fastapi.tiangolo.com/",
        }
    },
    {
        "name": "todo",
        "description": "Task that need to be completed"
    },
    {
        "name": "support",
        "description": "TODO API support"
    }
]


app = FastAPI(
    title="TODO API",
    openapi_tags=tags_info
)

app.include_router(support.router)
app.include_router(todo.router)


class Tags(Enum):
    home: str = "home"


@app.get("/", tags=[Tags.home])
async def home():
    return {
        "name": "TODO Rest API",
        "version": "1.0.0"
    }
