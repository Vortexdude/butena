from app.core.db.engine import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class User(Base):
    __tablename__ = "users"

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    user_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    enabled = Column(Boolean, nullable=True, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    def __repr__(self) -> str:
        return f"<USER  {self.user_id}>"


    def insert(self):
        pass