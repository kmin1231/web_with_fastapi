from fastapi import APIRouter
from model import Todo

todo_router = APIRouter()

todo_list = []

@todo_router.post("/todo")
async def app_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {
        "message": "Todo added successfully."
    }

@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return {
        "todos": todo_list
    }

# $ curl -X GET localhost:8000/todo

# $ curl -X POST localhost:8000/todo
# -H 'accept: application/json'
# -H 'Content-Type: application/json'
# -d '{"id":1, "item":"First Todo is to finish this book!"}'