from fastapi import APIRouter, Depends
from .service import CloudOperations, AwsKit, DatabaseOperation
from .schema import Deployment
from app.api.auth.depends import get_current_user
from app.core.db.engine import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create_deployment")
async def create(data: Deployment, user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = user['user_id']
    user_name = user['user_name']
    deployment_id = await DatabaseOperation(db).add(user_id)

    if not deployment_id:
        return {"Status", "Error with database"}

    operation = CloudOperations(user_name=user_name, deployment_id=deployment_id, **data.dict())
    response = await operation.create()
    response['deployment_id'] = deployment_id

    return response


@router.post("/remove")
def remove_site(deployment_id: str, user=Depends(get_current_user)):
    return AwsKit(data=user).delete_deployment(deployment_id)
