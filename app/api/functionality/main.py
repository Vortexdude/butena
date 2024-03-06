from fastapi import APIRouter, Depends
from .service import CloudOperations
from .schema import Deployment
from app.api.auth.depends import get_current_user
from app.core.db.engine import get_db
from app.api.functionality.s3_operation import aws_dependency
from sqlalchemy.orm import Session
from typing import Union, Dict

router = APIRouter()


@router.post("/create_deployment")
async def create(data: Deployment,
                 user: Dict[str, str] = Depends(get_current_user),
                 db: Session = Depends(get_db),
                 dependency_result: bool = Depends(aws_dependency)
                 ) -> Dict[str, Union[str, int]]:
    """
    Endpoint to create a new deployment.

    Args:
        data (Deployment): Deployment data from the request body.
        user (Dict[str, str]): Current user information.
        db (Session): SQLAlchemy database session.
        dependency_result (bool): validate the aws credentials are still there or not
    Returns:
        dict: Result of the deployment creation.
    """
    operation = CloudOperations(db, user)
    try:
        response = await operation.create_deployment(**data.dict())
        return response
    except Exception as e:
        raise e


@router.post("/remove")
async def remove_site(deployment_id: Union[str, int],
                      user: Dict[str, str] = Depends(get_current_user),
                      db: Session = Depends(get_db),
                      dependency_result: bool = Depends(aws_dependency)
                      ) -> Dict[str, str]:
    """
    Endpoint to remove a deployment.

    Args:
        deployment_id (Union[str, int]): ID of the deployment to be removed.
        user (Dict[str, str]): Current user information.
        db (Session): SQLAlchemy database session.
        dependency_result (bool): validate the aws credentials are still there or not
    Returns:
        dict: Result of the deployment removal.
    """
    operation = CloudOperations(db, user)
    try:
        response = await operation.delete_deployment(deployment_id)
        return response
    except Exception as e:
        raise e


@router.get("/my_deployments")
async def list_deployments(
        user: Dict[str, str] = Depends(get_current_user),
        db: Session = Depends(get_db),
        dependency_result: bool = Depends(aws_dependency)
):
    """
    Endpoint to list all deployment.

    Args:
        user (Dict[str, str]): Current user information.
        db (Session): SQLAlchemy database session.
        dependency_result (bool): validate the aws credentials are still there or not
    Returns:
        List: List of deployments under the logged user.
    """
    operation = CloudOperations(db=db, user=user)
    return operation.list_deployments()
