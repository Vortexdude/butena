from app.api.router import api_router
from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
from app.core.db.engine import init_db
# from app.pages.template_router import router as template_router

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

    init_db()

    # app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(router=api_router, prefix="/api")
    # app.include_router(router=template_router)

    return app
