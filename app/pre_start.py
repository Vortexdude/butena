import logging
from app.core.db.engine import init_db

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


def init():
    try:
        init_db()
    except Exception as e:
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
