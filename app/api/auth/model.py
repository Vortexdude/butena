from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db.engine import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean
)


class Users(Base):
    __tablename__ = "Users"

    id = mapped_column(Integer, primary_key=True)
    email = Column(String(225), nullable=False, unique=True)
    user_id: Mapped[str]
    first_name = Column(String(225), nullable=True)
    last_name = Column(String(225), nullable=True)
    username = Column(String(225), nullable=False)
    superuser = Column(Boolean, default=False)
    hashed_password = Column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __repr__(self):
        return f"User <{self.email}>"

    def __init__(
            self,
            email=None,
            user_id=None,
            first_name=None,
            last_name=None,
            username=None,
            superuser=None,
            hashed_password=None,
            created_at=None
    ):
        self.email = email
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.superuser = superuser
        self.hashed_password = hashed_password
        self.created_at = created_at

