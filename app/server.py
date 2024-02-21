import uvicorn
from settings import Config


def main() -> None:
    """Entrypoint"""

    uvicorn.run(
        "core.main:get_app",
        workers=Config.WORKER_COUNT,
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.RELOAD,
        factory=True,
    )


if __name__ == "__main__":
    main()
