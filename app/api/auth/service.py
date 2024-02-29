from .schema import UserCreation
from app.core.db.models import User
from app.core.utils import JWT
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status
from app.core.db.engine import SessionLocal


class UserService:

    def __init__(self, db):
        self.db: Session = db

    async def create(self, data: UserCreation):
        _data = data.dict()
        user = self.find_by_email(email=_data['email'])
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already present with the email"
            )

        _data['hashed_password'] = JWT.get_password_hash(_data['password'])
        _data.pop('password')

        user_in = User(**_data)
        self.db.add(user_in)
        self.db.commit()
        self.db.refresh(user_in)

        return user_in

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter_by(email=email).first()

    @staticmethod
    async def authenticate(email: str, password: str):

        with SessionLocal.begin() as session:
            user = session.query(User).filter_by(email=email).first()
            session.close()

        if not user:
            return None
        if not JWT.verify_password(plain_password=password, hashed_password=str(user.hashed_password)):
            return None

        return user

    @staticmethod
    async def find_by_id(id: str):
        session = SessionLocal()
        user = session.query(User).filter_by(user_id=id).first()
        session.close()

        if not user:
            return None

        return user
