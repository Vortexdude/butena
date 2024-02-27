from git import Repo
import os
import shutil
import glob
import boto3
from botocore.exceptions import ClientError
from app.settings import Config


class CloudOperations:
    def __init__(self, user_id, github_url, repo_type):
        self.aws_service = 's3'
        self.bucket_name = Config.BUCKET_NAME
        self.github_url = github_url
        self.repo_type = repo_type
        self.user_id = user_id
        self.clone_dir = os.path.join(Config.TEMP_DIR, str(self.user_id))
        self.client = boto3.client(self.aws_service)
        self.zone = Config.ZONE
        self.uploaded_file = []

    async def launch(self):
        if not self._clone():
            print("Error while cloning the repo.. ")
            return {"status": "Error while cloning the repo.. "}

        if not self._file_operations():
            print("Error while doing file operations... ")
            return {"status": "Error while cloning the repo.. "}

        if 'index.html' in self.uploaded_file:
            full_url = f"https://{self.bucket_name}.{self.aws_service}.{Config.ZONE}.amazonaws.com/website/2bbf1c95-b/index.html"
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

    def _file_operations(self):
        static_files = glob.glob(f"{self.clone_dir}/*")
        relative_paths = [os.path.relpath(file_path, self.clone_dir) for file_path in static_files]

        # uploading files to s3
        for file in relative_paths:
            self.uploaded_file.append(file)
            self._upload_file(file)

        # cleanup . .
        shutil.rmtree(self.clone_dir)
        return True

    def _upload_file(self, file_name, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        key = f"website/{str(self.user_id)[:10]}/{file_name}"

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
