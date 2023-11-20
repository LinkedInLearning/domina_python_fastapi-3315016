from fastapi import FastAPI

app = FastAPI()
app.title = "Hello world API"


@app.get("/", name="home")
async def hello_world():
    return {"message": "Hello world!"}
