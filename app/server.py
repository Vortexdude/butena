import uvicorn
from settings import conf, logger


def main() -> None:
    """Entrypoint"""

    uvicorn.run(
        "core.main:get_app",
        workers=conf.WORKER_COUNT,
        host=conf.API_HOST,
        port=conf.API_PORT,
        reload=conf.SERVER_RELOAD,
        factory=True,
    )


if __name__ == "__main__":
    logger.info("Starting the server")
    main()
