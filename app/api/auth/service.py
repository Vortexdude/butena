from .schema import UserCreation
from .model import Users
from lib.utils import get_hashed_password, verify_password
from uuid import UUID


class UserService:
    def __init__(self, db):
        self.session = db

    async def create_user(self, user: UserCreation):
        data = dict(user.dict())
        data['hashed_password'] = str(get_hashed_password(data['password']))
        data.pop('password')
        user_in = Users(**data)
        self.session.add(user_in)
        self.session.commit()
        self.session.refresh(user_in)
        return data

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
