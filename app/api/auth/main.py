from fastapi import Depends
from fastapi import APIRouter
from .schema import UserCreation
from .service import UserService
from app.core.db.models import User
from .depends import get_current_user
from app.core.db.engine import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", summary="Root endpoint")
async def root():
    """
    Example root endpoint
    """
    return {"User": "Nitin"}


#  response_model=UserOut
@router.post("/signup", summary="Create New User")
async def create_user(data: UserCreation, db: Session = Depends(get_db)):
    """
    Endpoint to create a new user
    """

    user_service = UserService(db=db)
    created_user = await user_service.create(data)
    return {
        'user_id': created_user.user_id,
        'user_name': created_user.user_name,
        'enabled': created_user.enabled
    }


@router.post('/me', summary="Get the current user and detail")
async def me(user: User = Depends(get_current_user)):
    """
    Endpoint to get details of the current user
    """

    return user
