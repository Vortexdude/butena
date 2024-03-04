from .schema import UserCreation
from app.core.db.models import User
from app.core.utils import JWT
from sqlalchemy.orm import Session
from app.core.db.engine import SessionLocal
from app.exceptions import UserException, StatusCode
from typing import Dict, Union


class UserService:

    def __init__(self, db: Session) -> None:
        """
        Constructor for UserService.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db: Session = db

    async def create(self, data: UserCreation) -> User:
        """
        Create a new user.

        Args:
            data (UserCreation): User creation data.

        Returns:
            User: Created user.
        """
        _data: Dict[str, str] = data.dict()
        user = self.find_by_email(email=_data['email'])
        if user:
            raise UserException(status_code=StatusCode.CONFLICT_409)

        _data['hashed_password'] = JWT.get_password_hash(_data['password'])
        _data.pop('password')

        user_in = User(**_data)
        self.db.add(user_in)
        self.db.commit()
        self.db.refresh(user_in)

        return user_in

    def find_by_email(self, email: str) -> Union[User, None]:
        """
        Find a user by email.

        Args:
            email (str): User email.

        Returns:
            Union[User, None]: User if found, None otherwise.
        """
        return self.db.query(User).filter_by(email=email).first()

    @staticmethod
    async def authenticate(email: str, password: str) -> Union[User, None]:
        """
        Authenticate a user.

        Args:
            email (str): User email.
            password (str): User password.

        Returns:
            Union[User, None]: User if authenticated, None otherwise.
        """
        with SessionLocal.begin() as session:
            user = session.query(User).filter_by(email=email).first()
            session.close()

        if not user:
            return None
        if not JWT.verify_password(plain_password=password, hashed_password=str(user.hashed_password)):
            return None

        return user

    @staticmethod
    async def find_by_id(id: str) -> Union[User, None]:
        """
        Find a user by ID.

        Args:
            id (str): User ID.

        Returns:
            Union[User, None]: User if found, None otherwise.
        """
        session = SessionLocal()
        user = session.query(User).filter_by(user_id=id).first()
        session.close()
        return user
