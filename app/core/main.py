from app.api.router import api_router
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

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
    async def app_init():
        """initialize the crucial functions"""
        db_client = AsyncIOMotorClient("mongodb://127.0.0.1:27017/butena").fodoist()

        await init_beanie(
            database=db_client,
            document_models= [
                User,
                Todo
            ]
        )

    app.include_router(router=api_router, prefix="/api")

    return app
