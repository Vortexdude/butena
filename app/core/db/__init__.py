from sqlalchemy import create_engine
from settings import Config
from sqlalchemy.orm import Session
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)

    def add_user(self, user_create):
        with Session(self.engine) as session:
            user = User(name=user_create.name, fullname=user_create.fullname)
            session.add(user)
            session.commit()
