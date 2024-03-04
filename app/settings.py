from app.core.config import Settings
import logging
import sys

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# stream_handler = logging.StreamHandler(sys.stdout)
# log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
# stream_handler.setFormatter(log_formatter)
# logger.addHandler(stream_handler)


class Config(Settings):
    """Project configuration
    :param API_PORT: port where the application runs
    :param API_HOST: host for the server like - 0.0.0.0
    :param API_ENV: dev
    :param API_VERSION: 1.0
    :param WORKER_COUNT: 1
    :param SERVER_RELOAD: True
    :param JWT_SECRET_KEY: nothing_special
    :param JWT_REFRESH_SECRET_KEY: very_special
    :param ALGORITHM: HS256
    :param TEMP_DIR: /tmp/git
    :param BUCKET_NAME: butena-public
    :param BUCKET_ZONE: ap-south-1
    :param API_TITLE: Butena
    :param DESCRIPTION: "Fast api starter"
    :param DOC_URL: /api/doc
    :param REDOC_URL: /api/redoc/
    :return: True if file was uploaded, else False
    """

    ACCESS_TOKEN_EXPIRE_MINUTES: str = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: str = 60 * 24 * 7  # 7 days


# logger.info(f"Using the configuration for {conf.API_TITLE}")


conf = Config()
