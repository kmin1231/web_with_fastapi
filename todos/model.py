from pydantic import BaseModel
from typing import List

class Todo(BaseModel):
    id: int
    item: str

class Item(BaseModel):
    item: str
    status: str

# class Todo(BaseModel):
#     id: int
#     item: Item  # nested pydantic model

class TodoItem(BaseModel):
    item: str

    class Config:
        schema_extra = {
            "example": {
                "item": "Read the next chapter of the book."
            }
        }

class TodoItems(BaseModel):
    todos: List[TodoItem]

    class Config:
        schema_extra = {
            "example": {
                "todos": [
                    {
                        "item": "Example schema 1!"
                    },
                    {
                        "item": "Example schema 2!"
                    }
                ]
            }
        }