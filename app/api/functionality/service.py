from git import Repo
import os
from sqlalchemy.orm import Session
from app.settings import conf
from app.core.utils import FileOperations
from app.core.db.models import Deployment
from .s3_operation import BaseS3Operation
from fastapi.exceptions import HTTPException
from fastapi import status


KEY = "website/{user_name}/{deployment}"
BUCKET_NAME = conf.BUCKET_NAME
ZONE = conf.BUCKET_ZONE
CLONE_DIR = conf.TEMP_DIR


class DatabaseOperation(BaseS3Operation):

    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    def add(self, user_id) -> str | int:
        dep = Deployment(
            user_id=user_id,
            bucket=BUCKET_NAME,
            zone=ZONE
        )
        self.db.add(dep)
        self.db.commit()
        self.db.refresh(dep)

        return dep.id

    def delete(self, id: str, user_id: str):
        _deployments = self.db.query(Deployment).filter_by(user_id=user_id).filter_by(id=id).first()
        if _deployments:
            self.db.query(Deployment).filter_by(id=id).delete()
            return True

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "No deployment found"
            }
        )

    def find_by_id(self, id: str):
        return self.db.query(Deployment).filter_by(id=id).first()


class CloudOperations(DatabaseOperation):
    def __init__(self, db: Session, user: dict):
        super().__init__(db=db)
        self.bucket_name = BUCKET_NAME
        self.user_name = user['user_name']
        self.user_id = user['user_id']
        self.bucket_files = []

    async def create_deployment(self, github_url, repo_type):

        deployment_id = DatabaseOperation(self.db).add(self.user_id)

        if not deployment_id:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error with the database side"
            )

        user_namespace = str(os.path.join(CLONE_DIR, self.user_name))
        FileOperations.delete_all_files(user_namespace)
        Repo.clone_from(github_url, user_namespace)
        files = FileOperations.list_files(user_namespace)  # get all the files names as a list in a dir
        key = KEY.format(user_name=self.user_name, deployment=deployment_id)
        for file in files:
            s3_key = key + '/' + f'{file}'  # key location for the s3 bucket
            local_file_path = os.path.join(user_namespace, file)  # for get the full local path /tmp/git/username/files
            self.upload_file(bucket=BUCKET_NAME, file_name=local_file_path, key=s3_key)  # uploading to s3
            self.bucket_files.append(file)  # uploaded to s3

        FileOperations.cleanup(user_namespace)  # cleanup

        if 'index.html' in self.bucket_files:
            full_url = f"https://{BUCKET_NAME}.s3.{ZONE}.amazonaws.com/{key}/index.html"
        else:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="No file found in the bucket"
            )

        return {
            "status": "done",
            "deployment_id": deployment_id,
            "url": full_url
        }

    async def delete_deployment(self, deployment_id):
        response = self.delete(id=deployment_id, user_id=self.user_id)
        if not response:
            pass
        key = KEY.format(user_name=self.user_name, deployment=deployment_id)
        # key = f"website/{self.user_name}/{deployment_id}"
        files = self.list_files(bucket_name=BUCKET_NAME, key=key)

        if not files:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="No file found in the bucket"
            )

        for file in files:
            self.delete_file(bucket=BUCKET_NAME, key=file)

        return {"Status": f"Deployment {deployment_id} Deleted Successfully!"}
