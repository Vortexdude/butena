from fastapi import APIRouter
from .schema import UserCreation
from .service import UserService
import pymongo
router = APIRouter()


@router.get("/")
async def root():
    return {"User": "Nitin"}

#  response_model=UserOut
@router.post("/signup", summary="Create New User")
async def create_user(data: UserCreation):
    try:
        return await UserService.create_user(data)
    except Exception as e:
        raise Exception(f"Due to some technical issue with the database please wait to start up.. {e}")



