from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from planner.auth.jwt_handler import create_access_token
from planner.database.connection import Database

from planner.models.users import User, TokenResponse
from planner.auth.hash_password import HashPassword

user_router = APIRouter(
    tags=["User"],
)

user_database = Database(User)
hash_password = HashPassword()

@user_router.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already"
        )
    
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    return {
        "message": "User successfully registered!"
    }

# $ curl -X POST localhost:8000/user/signup -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"email": "fastapi@packt.com", "password": "strong!!!", "events": []}'

@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist"
        )
    
    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": "User signed in sucessfully.",
            "token_type": "Bearer"
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed"
    )

# $ curl -X POST localhost:8000/user/signin -H 'accept: application/json' -H 'Content-Type: application/x-www-form-urlencoded' -d 'grant_type=&username=reader%40packt.com&password=exemplary&scope=&client_id=&client_secret='