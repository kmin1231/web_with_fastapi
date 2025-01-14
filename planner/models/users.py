from pydantic import BaseModel, EmailStr
from typing import Optional, List
from beanie import Document, Link
from models.events import Event

class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = None

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "username": "strong!",
                "events": [],
            }
        }

# class UserSignIn(BaseModel):
#     email: EmailStr
#     password: str

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "email": "fastapi@packt.com",
#                 "password": "strong!!!",
#                 "events": [],
#             }
#         }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str