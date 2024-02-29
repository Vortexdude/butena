from git import Repo
import os
import shutil
import glob
import boto3
from botocore.exceptions import ClientError
from app.settings import conf
from app.core.db.models import Deployment
from sqlalchemy.orm import Session

KEY = "website/{user_name}/{deployment}"
BUCKET_NAME = conf.BUCKET_NAME
ZONE = conf.BUCKET_ZONE
CLONE_DIR = conf.TEMP_DIR


class FileOperations:

    def __init__(self):
        pass

    @staticmethod
    def list_files(abs_dir: str) -> list:
        static_files = glob.glob(f"{abs_dir}/*")
        return [os.path.relpath(file_path, abs_dir) for file_path in static_files]

    @staticmethod
    def delete_all_files(abs_path: str):
        if os.path.isdir(abs_path):
            print(f"Removing ... {abs_path}")
            shutil.rmtree(abs_path)


class BaseS3Operation:
    def __init__(self):
        self.client = boto3.client('s3')

    def list_files(self, bucket_name: str, key: str) -> list | None:
        files = []
        try:
            response = self.client.list_objects(Bucket=bucket_name, Prefix=key)
            if 'Contents' not in response:
                return

            for item in response['Contents']:
                files.append(item['Key'])

        except ClientError as e:
            raise e

        return files

    def upload_file(self, bucket, file_name, key) -> bool:

        try:
            with open(file_name, 'rb') as f:
                contents = f.read()

            response = self.client.put_object(
                Body=bytes(contents),
                Bucket=bucket,
                Key=key,
                ContentType='text/html',
                ContentDisposition='inline'
            )
            print(f"Uploading file {file_name} ...")

        except ClientError as e:
            print(e)
            return False
        return True

    def delete_file(self, bucket: str, key: str):
        try:
            self.client.delete_object(Bucket=bucket, Key=key)
            return True

        except ClientError as e:
            raise e


class DatabaseOperation:

    def __init__(self, db: Session):
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
        print(_deployments)
        if not _deployments:
            return {"db_status": "No Deployment found in the database", 'operation_status': False}

        response = self.db.query(Deployment).filter_by(id=id).delete()

        return {"db_status": "Deployment Deleted Successfully!", 'operation_status': True}

    def find_by_id(self, id: str):
        return self.db.query(Deployment).filter_by(id=id).first()


class CloudOperations(BaseS3Operation, DatabaseOperation):
    def __init__(self, db: Session, user: dict):
        super().__init__()
        self.db = db
        self.bucket_name = conf.BUCKET_NAME
        self.user_name = user['user_name']
        self.user_id = user['user_id']
        self.bucket_files = []

    async def create_deployment(self, github_url, repo_type):

        deployment_id = DatabaseOperation(self.db).add(self.user_id)

        if not deployment_id:
            return {"Status", "Error with database"}

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
        shutil.rmtree(user_namespace)  # cleanup

        if 'index.html' in self.bucket_files:
            full_url = f"https://{BUCKET_NAME}.s3.{ZONE}.amazonaws.com/{key}/index.html"
        else:
            full_url = "Cant find the index file in the repo"

        return {
            "status": "done",
            "deployment_id": deployment_id,
            "url": full_url
        }

    async def delete_deployment(self, deployment_id):
        response = self.delete(id=deployment_id, user_id=self.user_id)
        if not response['operation_status']:
            return response['db_status']

        key = KEY.format(user_name=self.user_name, deployment=deployment_id)
        # key = f"website/{self.user_name}/{deployment_id}"
        files = self.list_files(bucket_name=BUCKET_NAME, key=key)

        if not files:
            return {"Status": "No files found in bucket"}

        for file in files:
            self.delete_file(bucket=BUCKET_NAME, key=file)

        response['deployment_status'] = f"Deployment {deployment_id} Deleted Successfully!"

        return response
