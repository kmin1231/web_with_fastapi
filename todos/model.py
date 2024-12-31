from pydantic import BaseModel

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