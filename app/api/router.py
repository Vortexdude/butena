from fastapi.routing import APIRouter
from app.api.auth.main import router as root_router
from app.api.functionality.main import router as cloud_operations
from app.api.auth.jwt import auth_router

api_router = APIRouter()

@api_router.get("/health")
def health():
    return {"message": "You are live"}


api_router.include_router(root_router, prefix="/users", tags=['user'])
api_router.include_router(cloud_operations, prefix="/operations", tags=['cloud_operations'])
api_router.include_router(auth_router, prefix="/auth", tags=['auth'])
