from fastapi.routing import APIRouter
from app.api.auth.main import router as root_router
from app.api.functionality.main import router as cloud_operations


api_router = APIRouter()
api_router.include_router(root_router, prefix="/users", tags=['user'])
api_router.include_router(cloud_operations, prefix="/operations", tags=['cloud_operations'])
