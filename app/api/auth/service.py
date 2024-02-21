from .schema import UserCreation
from .model import User
from app.lib.utils import get_hashed_password, verify_password
from uuid import UUID

class UserService:
    @staticmethod
    async def create_user(user: UserCreation):
        user_in = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=get_hashed_password(user.password)
        )
        await user_in.insert()
        return user_in

    @staticmethod
    async def find_by_email(email: str):
        user = await User.find(User.email == email).first_or_none()
        return user

    @staticmethod
    async def find_by_id(user_id: UUID):
        user = await User.find(User.user_id == user_id).first_or_none()
        return user

    @staticmethod
    async def authenticate(email: str, password: str):
        user = await UserService.find_by_email(email)

        if not user:
            return None
        if not verify_password(password=password, hashed_password=str(user.hashed_password)):
            return None

        return user
