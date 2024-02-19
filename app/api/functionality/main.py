from fastapi import APIRouter
from .service import CloudOperations
from .schema import Deployment

router = APIRouter()


@router.post("/")
async def create(data: Deployment):
    operation = CloudOperations(**data.__dict__)
    return await operation.launch()
