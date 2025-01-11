from fastapi import APIRouter, HTTPException, status
from database.connection import Database

from models.users import User, UserSignIn

user_router = APIRouter(
    tags=["User"],
)

user_database = Database(User)

@user_router.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already"
        )
    await user_database.save(user)
    return {
        "message": "User successfully registered!"
    }

# $ curl -X POST localhost:8000/user/signup -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"email": "fastapi@packt.com", "password": "strong!!!", "events": []}'

@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist"
        )
    
    if user_exist.password == user.password:
        return {
            "message": "User signed in sucessfully."
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed"
    )

# $ curl -X POST localhost:8000/user/signin -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"email": "fastapi@packt.com", "password": "strong!!!"}'