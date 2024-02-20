from fastapi import APIRouter, HTTPException, status
from .schema import UserCreation, UserOut
from .service import UserService
import pymongo

router = APIRouter()


@router.get("/")
async def root():
    return {"User": "Nitin"}


#  response_model=UserOut
@router.post("/signup", summary="Create New User", response_model=UserOut)
async def create_user(data: UserCreation):
    user = await UserService.find_by_email(data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already present with the email"
        )

    data = await UserService.create_user(data)
    user_in = {
        'user_id': data.user_id,
        'user_name': data.user_name,
        'enabled': data.enabled
    }
    return user_in
