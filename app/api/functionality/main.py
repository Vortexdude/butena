from fastapi import APIRouter, Depends
from .service import CloudOperations
from .schema import Deployment
from app.api.auth.depends import get_current_user
from app.core.db.engine import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create_deployment")
async def create(data: Deployment, user=Depends(get_current_user), db: Session = Depends(get_db)):
    operation = CloudOperations(db, user)
    response = await operation.create_deployment(**data.dict())

    return response


@router.post("/remove")
async def remove_site(deployment_id: str | int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    operation = CloudOperations(db, user)
    response = await operation.delete_deployment(deployment_id)

    return response
