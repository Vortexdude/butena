from fastapi import APIRouter, Depends
from .service import CloudOperations, AwsKit
from .schema import Deployment
from app.api.auth.depends import get_current_user

router = APIRouter()


@router.post("/")
async def create(data: Deployment, user=Depends(get_current_user)):
    operation = CloudOperations(user_id=user['user_id'], **data.__dict__)
    return await operation.launch()


@router.post("/remove")
def remove_site(user=Depends(get_current_user)):
    return AwsKit(user_id=user['user_id']).delete_deployment()
