from app.api.router import api_router
from fastapi import FastAPI
from app.settings import conf
from app.core.db.engine import init_db


def get_app() -> FastAPI:
    """
    Get FastAPI application.
    This is the main constructor of an application.
    :return: application.
    """
    app = FastAPI(
        title=conf.API_TITLE,
        description=conf.DESCRIPTION,
        version=conf.API_VERSION,
        docs_url=conf.DOC_URL,
        redoc_url=conf.REDOC_URL,
        openapi_url="/api/openapi.json",
    )

    init_db()
    app.include_router(router=api_router, prefix=f"/api/{conf.API_VERSION}")

    return app
