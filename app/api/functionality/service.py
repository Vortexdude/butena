from git import Repo
import os
import shutil
import glob
import boto3
from botocore.exceptions import ClientError
from app.settings import conf
from app.core.db.models import Deployment
from sqlalchemy.orm import Session


class DatabaseOperation:

    def __init__(self, db: Session):
        self.db = db
        self.bucket_name = conf.BUCKET_NAME
        self.zone = conf.BUCKET_ZONE

    async def add(self, user_id):
        data = {
            "user_id": user_id,
            "bucket": self.bucket_name,
            "zone": self.zone
        }
        dep = Deployment(**data)
        self.db.add(dep)
        self.db.commit()
        self.db.refresh(dep)

        return dep.id

    async def delete_record(self, id: str, user_id: str):
        _deployments = await self.db.query(Deployment).filter_by(user_id=user_id).filter_by(id=id).first()
        if not _deployments:
            return {"Status": "No Deployment found in the database"}

        response = self.db.query(Deployment).filter_by(id=id).delete()
        print(response)
        return {"Status": "Deployment Deleted Successfully!"}

    def find_by_id(self, id: str):
        return self.db.query(Deployment).filter_by(id=id).first()


class CloudOperations:
    def __init__(self, deployment_id, user_name, github_url, repo_type):
        self.aws_service = 's3'
        self.bucket_name = conf.BUCKET_NAME
        self.github_url = github_url
        self.repo_type = repo_type
        self.user_name = user_name
        self.deployment_id = deployment_id
        self.clone_dir = os.path.join(conf.TEMP_DIR, str(self.user_name))
        self.client = boto3.client(self.aws_service)
        self.zone = conf.BUCKET_ZONE
        self.uploaded_file = []

    async def create(self):
        if not self._clone():
            print("Error while cloning the repo.. ")
            return {"status": "Error while cloning the repo.. "}

        if not self._file_operations():
            print("Error while doing file operations... ")
            return {"status": "Error while cloning the repo.. "}

        if 'index.html' in self.uploaded_file:
            full_url = f"https://{self.bucket_name}.{self.aws_service}.{self.zone}.amazonaws.com/website/{self.user_name}/{self.deployment_id}/index.html"
        else:
            full_url = "Cant find the index file in the repo"

        return {
            "status": "done",
            "url": full_url
        }

    def _clone(self):
        if os.path.isdir(self.clone_dir):
            print("clone directory already exist.")
            print(f"Removing ... {self.clone_dir}")
            shutil.rmtree(self.clone_dir)

        Repo.clone_from(self.github_url, self.clone_dir)
        return True

    def _file_operations(self) -> bool:
        key = ''
        static_files = glob.glob(f"{self.clone_dir}/*")
        relative_paths = [os.path.relpath(file_path, self.clone_dir) for file_path in static_files]

        # uploading files to s3
        for file in relative_paths:
            self.uploaded_file.append(file)
            key = f"website/{self.user_name}/{self.deployment_id}/{file}"
            self._upload_file(file, key)

        # cleanup . .
        shutil.rmtree(self.clone_dir)
        return True

    def _upload_file(self, file_name, key, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            _file_path = os.path.join(self.clone_dir, file_name)
            with open(_file_path, 'rb') as f:
                contents = f.read()

            response = self.client.put_object(
                Body=bytes(contents),
                Bucket=self.bucket_name,
                Key=key,
                ContentType='text/html',
                ContentDisposition='inline'
            )
            print(f"Uploading file {file_name} ...")

        except ClientError as e:
            print(e)
            return False
        return True


class AwsKit:
    def __init__(self, service='s3', data: dict = None, **kwargs):

        self.bucket_name = conf.BUCKET_NAME
        self.client = boto3.client(service)
        self.user_id = data['user_id']
        self.user_name = data['user_name']

    def _list_objects(self, deployment_id: str) -> list:
        files = []
        key = f"website/{self.user_name}/{deployment_id}"
        try:
            response = self.client.list_objects(Bucket=self.bucket_name, Prefix=key)
            for item in response['Contents']:
                files.append(item['Key'])
        except ClientError as e:
            raise e

        return files
        # https://butena-public.s3.ap-south-1.amazonaws.com/website/e3c7551f-b/index.html

    def delete_deployment(self, deployment_id):
        files = self._list_objects(deployment_id)
        if not files:
            return {"Status": "No files are there"}

        for file in files:
            self._delete_object(file)
            # website/e3c7551f-b/index.html

        return {"Status": f"Deployment {deployment_id} Deleted Successfully!"}

    def _delete_object(self, file):
        self.client.delete_object(Bucket=self.bucket_name, Key=file)
