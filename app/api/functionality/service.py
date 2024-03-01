from git import Repo
import os
from sqlalchemy.orm import Session
from app.settings import conf
from app.core.utils import FileOperations
from app.core.db.models import Deployment
from app.exceptions import DatabaseException, StatusCode, FileException
from .s3_operation import BaseS3Operation
from typing import Union

DEPLOYMENT_KEY_FORMAT = "website/{user_name}/{deployment}"
BUCKET_NAME = conf.BUCKET_NAME
ZONE = conf.BUCKET_ZONE
CLONE_DIR = conf.TEMP_DIR


class DatabaseOperation(BaseS3Operation):
    """
        Handles database operations related to deployments.
    """

    def __init__(self, db: Session) -> None:
        """
        Constructor for DatabaseOperation.

        Args:
            db (Session): SQLAlchemy database session.
        """
        super().__init__()
        self.db = db

    def add(self, user_id: str) -> int:
        """
        Add a new deployment record to the database.

        Args:
            user_id (str): User ID.

        Returns:
            int: The ID of the added deployment.
        """

        dep = Deployment(
            user_id=user_id,
            bucket=BUCKET_NAME,
            zone=ZONE
        )
        self.db.add(dep)
        self.db.commit()
        self.db.refresh(dep)

        return dep.id

    def delete(self, id: str, user_id: str) -> bool:
        """
        Delete a deployment record from the database.

        Args:
            id (str): Deployment ID.
            user_id (str): User ID.

        Raises:
            DatabaseException: If the deployment is not found.
        """

        deployment = self.db.query(Deployment).filter_by(user_id=user_id, id=id).first()
        if deployment:
            self.db.query(Deployment).filter_by(id=id).delete()
            self.db.commit()
            return True

        raise DatabaseException(status_code=StatusCode.NOTFOUND_404)

    def find_by_id(self, id: str) -> Union[Deployment, None]:
        """
        Find a deployment record by ID.

        Args:
            id (str): Deployment ID.

        Returns:
            Deployment: The deployment record.
        """

        return self.db.query(Deployment).filter_by(id=id).first()


class CloudOperations(DatabaseOperation):
    """
    Handles cloud operations related to deployments.
    """

    def __init__(self, db: Session, user: dict):
        """
        Constructor for CloudOperations.

        Args:
            db (Session): SQLAlchemy database session.
            user (dict): User information.
        """

        super().__init__(db=db)
        self.bucket_name = BUCKET_NAME
        self.user_name = user['user_name']
        self.user_id = user['user_id']
        self.bucket_files = []

    async def create_deployment(self, github_url, repo_type):
        """
        Create a new deployment.

        Args:
            github_url (str): URL of the GitHub repository.
            repo_type (str): Type of repository.

        Returns:
            dict: Result of the deployment creation.
        """

        deployment_id = DatabaseOperation(self.db).add(self.user_id)

        if not deployment_id:
            raise DatabaseException(status_code=StatusCode.NOTFOUND_404)

        user_namespace = str(os.path.join(CLONE_DIR, self.user_name))
        FileOperations.delete_all_files(user_namespace)
        Repo.clone_from(github_url, user_namespace)
        files = FileOperations.list_files(user_namespace)  # get all the files names as a list in a dir
        key = DEPLOYMENT_KEY_FORMAT.format(user_name=self.user_name, deployment=deployment_id)
        for file in files:
            s3_key = key + '/' + f'{file}'  # key location for the s3 bucket
            local_file_path = os.path.join(user_namespace, file)  # for get the full local path /tmp/git/username/files
            self.upload_file(bucket=BUCKET_NAME, file_name=local_file_path, key=s3_key)  # uploading to s3
            self.bucket_files.append(file)  # uploaded to s3

        FileOperations.cleanup(user_namespace)  # cleanup

        if 'index.html' in self.bucket_files:
            full_url = f"https://{BUCKET_NAME}.s3.{ZONE}.amazonaws.com/{key}/index.html"
        else:
            raise DatabaseException(status_code=StatusCode.BAD_GATEWAY_502)

        return {
            "status": "done",
            "deployment_id": deployment_id,
            "url": full_url
        }

    async def delete_deployment(self, deployment_id):
        """
        Delete a deployment.

        Args:
            deployment_id (str): Deployment ID.

        Returns:
            dict: Result of the deployment deletion.
        """

        response = self.delete(id=deployment_id, user_id=self.user_id)
        if not response:
            pass
        key = DEPLOYMENT_KEY_FORMAT.format(user_name=self.user_name, deployment=deployment_id)
        files = self.list_files(bucket_name=BUCKET_NAME, key=key)

        if not files:
            raise FileException()

        for file in files:
            self.delete_file(bucket=BUCKET_NAME, key=file)

        return {"Status": f"Deployment {deployment_id} Deleted Successfully!"}
