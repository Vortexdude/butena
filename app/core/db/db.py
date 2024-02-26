# from sqlmodel import Session, select
# from api.auth.model import User, UserCreate
# from app.settings import Config
# from engine import create_db_and_table, engine
#
#
# def init_db(session: Session) -> None:
#     create_db_and_table()
#     user = session.exec(
#         select(User).where(User.email == Config.FIRST_SUPERUSER)
#     ).first()
#     if not user:
#         user_in = User(
#             email=Config.FIRST_SUPERUSER,
#             password=Config.FIRST_SUPERUSER_PASSWORD,
#             superuser=True
#         )
#         session = Session(engine)
#         session.add(user_in)
#         session.commit()
#         session.close()
