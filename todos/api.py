from fastapi import FastAPI
from todo import todo_router

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Hello, world!"
    }

app.include_router(todo_router)

# $ uvicorn api:app --port 8000 --reload
# $ curl http://localhost:8000