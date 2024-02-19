import uvicorn
from settings import Conf


def main() -> None:
    """Entrypoint"""

    uvicorn.run(
        "core.main:get_app",
        workers=Conf.WORKER_COUNT,
        host=Conf.HOST,
        port=Conf.PORT,
        reload=Conf.RELOAD,
        factory=True,
    )


if __name__ == "__main__":
    main()
