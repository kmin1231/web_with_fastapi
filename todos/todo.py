from fastapi import APIRouter

todo_router = APIRouter()

@todo_router.post("/todo")
async def app_todo(todo: dict) -> dict:
    todo_list.append(todo)
    return {
        "message": "Todo added successfully."
    }

@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return {
        "todos": todo_list
    }