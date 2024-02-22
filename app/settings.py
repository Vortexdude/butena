from app.lib.utils import Configuration


class Config(Configuration):
    """Project configuration
    :param API_PORT: port where the application runs
    :param API_HOST: host for the server like - 0.0.0.0
    :param API_ENV: dev
    :param API_VERSION: 1.0
    :param WORKER_COUNT: 1
    :param SERVER_RELOAD: True
    :param MONGO_DB_HOST: 127.0.0.1
    :param MONGO_DB_PORT: 27017
    :param MONGO_DATABASE: butena
    :param MONGO_USERNAME: ''
    :param MONGO_PASSWORD: ''
    :param JWT_SECRET_KEY: nothing_special
    :param JWT_REFRESH_SECRET_KEY: very_special
    :param ALGORITHM: HS256
    :param TEMP_DIR: /tmp/git
    :param BUCKET_NAME: butena-public
    :param ZONE: ap-south-1
    :return: True if file was uploaded, else False
    """

    pass

