from app.api.router import api_router
from fastapi import FastAPI
from app.core.db import beanie_db
from beanie import init_beanie
from app.api.auth.model import User as UserModel
from app.api.functionality.model import Deployment as DeploymentModel


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="Butena",
        description="FastAPI Starter Project",
        version="1.0",
        docs_url="/api/docs/",
        redoc_url="/api/redoc/",
        openapi_url="/api/openapi.json",
    )

    @app.on_event("startup")
    async def app_init():
        await init_beanie(
            database=beanie_db,
            document_models=[UserModel, DeploymentModel]
        )

    app.include_router(router=api_router, prefix="/api")

    return app
