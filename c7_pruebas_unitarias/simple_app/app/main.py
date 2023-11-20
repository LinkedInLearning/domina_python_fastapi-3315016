from fastapi import FastAPI

from app.routers import todo


app = FastAPI(
    title="TODO API",
)

app.include_router(todo.router)


@app.get("/", tags=["home"])
async def home():
    return {
        "name": "TODO Rest API",
        "version": "1.0.0"
    }
