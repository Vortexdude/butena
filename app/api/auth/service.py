from .schema import UserCreation
from .model import User
from app.lib.utils import JWT, get_hashed_password, verify_password


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
        user = User.find_one(User.email == email)
        return user

    @staticmethod
    async def authenticate(email: str, password: str):
        user = UserService.find_by_email(email)
        if not user:
            return None
        if not verify_password(password=password, hashed_password=str(user.hashed_password)):
            return None

        return user
