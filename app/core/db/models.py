from .engine import Base
from datetime import datetime
from typing import Optional
from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(30))
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    user_name: Mapped[Optional[str]]
    hashed_password: Mapped[str] = mapped_column(String(256))
    enabled: Mapped[Optional[bool]] = False
    super_user: Mapped[Optional[bool]] = False
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<USER  {self.user_id}>"


class Deployment(Base):
    __tablename__ = 'deployments'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[str] = mapped_column(String(256))
    bucket: Mapped[str] = mapped_column(String(40))
    zone: Mapped[str] = mapped_column(String(15))

    def __repr__(self):
        return f"Deployment id {self.id}"
