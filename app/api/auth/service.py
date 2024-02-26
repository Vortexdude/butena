from .schema import UserCreation
from .model import Users
from lib.utils import get_hashed_password, verify_password


class UserService:
    def __init__(self, db):
        self.session = db

    async def create_user(self, user: UserCreation):
        data = dict(user.dict())

        # check user exist or not
        user = self.get_user_by_email(data['email'])
        if user:
            return {"Error": "User already exist"}

        data['hashed_password'] = str(get_hashed_password(data['password']))
        data.pop('password')

        new_user = Users(**data)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return data

    def get_user_by_email(self, email: str):
        return self.session.query(Users).filter(Users.email == email).first()

    def get_user_by_id(self, email: str):
        return self.session.query(Users).filter(Users.id == id).first()


class JwtService:
    @staticmethod
    async def authenticate(email: str, password: str):
        from app.core.db.engine import SessionLocal
        with SessionLocal() as session:
            user = session.query(Users).filter(Users.email == email).first()

        if not user:
            return None
        if not verify_password(password=password, hashed_password=str(user.hashed_password)):
            return None

        return user
