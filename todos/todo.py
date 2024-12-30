from fastapi import APIRouter, Path
from model import Todo

todo_router = APIRouter()

todo_list = []

@todo_router.post("/todo")
async def app_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {
        "message": "Todo added successfully."
    }

# $ curl -X POST localhost:8000/todo
# -H 'accept: application/json'
# -H 'Content-Type: application/json'
# -d '{"id": 1, "item": {"item": "First Todo is to finish this book!", "status": "in progress"}}'

@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return {
        "todos": todo_list
    }

# $ curl -X GET localhost:8000/todo

@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int = Path(..., title="The ID of the todo to retrieve")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo": todo
            }
    return {
        "message": "Todo with supplied ID doesn't exist."
    }

# $ curl -X GET localhost:8000/todo/1