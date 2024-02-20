from app.lib.utils import Conf


class Config(Conf):
    MONGO_DB_CLIENT = f"mongodb://{Conf.HOST}:{Conf.PORT}"
