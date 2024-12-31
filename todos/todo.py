from fastapi import APIRouter, Path
from model import Todo, TodoItem

todo_router = APIRouter()

todo_list = []

@todo_router.post("/todo")
async def app_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {
        "message": "Todo added successfully."
    }

# $ curl -X POST localhost:8000/todo -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"id": 1, "item": "First Todo is to finish this book!"}'
# $ curl -X POST localhost:8000/todo -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"id": 1, "item": {"item": "First Todo is to finish this book!", "status": "in progress"}}'

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

@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: TodoItem, todo_id: int = Path(..., title="The ID of the todo to be updated.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {
                "message": "Todo updated successfully."
            }
    return {
        "message": "Todo with supplied ID doesn't exist."
    }

# $ curl -X PUT localhost:8000/todo/1 -H 'accpet: application/json' -H 'Content-Type: application/json' -d '{"item": "Read the next chapter of the book"}'

@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return {
                "message": "Todo deleted successfully."
            }
    return {
        "message": "Todo with supplied ID doesn't exist."
    }

# $ curl -X DELETE localhost:8000/todo/1 -H 'accept: application/json'

@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return {
        "message": "Todos deleted"
    }

# $ curl -X DELETE localhost:8000/todo -H 'accept: application/json'