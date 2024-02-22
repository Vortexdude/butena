import uvicorn
from settings import Config


def main() -> None:
    """Entrypoint"""

    uvicorn.run(
        "core.main:get_app",
        workers=Config.WORKER_COUNT,
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=Config.SERVER_RELOAD,
        factory=True,
    )


if __name__ == "__main__":
    main()