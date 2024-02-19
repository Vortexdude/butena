from fastapi import APIRouter, Depends
from .schema import UserOut, UserAuth
from uuid import uuid4

router = APIRouter()


@router.get("/")
async def root():
    return {"User": "Nitin"}


@router.post("/signup", summary="Create New User", response_model=UserOut)
async def create_user(data: UserAuth):
    user = {
        'user_id': '6cf304be-0cb3-42ca-b3c7-3d713f7de728',
        'email': 'nitin@gmail.com',
        'username': "nnamdev",
        'password': "dfdf545",
        'first_name': "nitin",
        "last_name": "Namdev"
    }
    return user

