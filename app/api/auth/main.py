from fastapi import Depends
from fastapi import APIRouter, HTTPException, status
from .schema import UserCreation
from .service import UserService
from .model import User
from .depends import get_current_user
from app.core.db.engine import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
async def root():
    return {"User": "Nitin"}


#  response_model=UserOut
@router.post("/signup", summary="Create New User")
async def create_user(data: UserCreation, db: Session = Depends(get_db)):
    user_service = UserService(db=db)
    data = await user_service.create(data)
    user_in = {
        'user_id': data.user_id,
        'user_name': data.user_name,
        'enabled': data.enabled
    }
    return user_in


@router.post('/me', summary="Get the current user and detail")
async def me(user: User = Depends(get_current_user)):
    return user
