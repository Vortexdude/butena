from fastapi import Depends
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from .schema import UserCreation
from .service import UserService
from .model import Users
from .depends import get_current_user
from core.db.engine import get_db
router = APIRouter()


@router.get("/")
async def root():
    return {"User": "Nitin"}


#  response_model=UserOut
@router.post("/signup", summary="Create New User")
async def create_user(data: UserCreation, db: Session = Depends(get_db)):
    user = UserService(db)
    return await user.create_user(data)


@router.post('/me', summary="Get the current user and detail")
async def me(user: Users = Depends(get_current_user)):
    return user
