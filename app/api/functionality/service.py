from git import Repo
import os
import shutil
import glob
import boto3
from botocore.exceptions import ClientError


TEMP_DIR = "/tmp/git"
BUCKET_NAME = 'butena-public'
DEPLOYMENT_ID = 'nothing'

class CloudOperations:
    def __init__(self, user_id, github_url, repo_type):
        self.bucket_name = BUCKET_NAME
        self.github_url = github_url
        self.repo_type = repo_type
        self.user_id = user_id
        self.clone_dir = os.path.join(TEMP_DIR, str(self.user_id))
        self.client = boto3.client('s3')

    async def launch(self):
        self.clone()
        return {"Status": "Success"}

    def clone(self):
        if os.path.isdir(self.clone_dir):
            print("clone directory already exist.")
            print(f"Removing ... {self.clone_dir}")
            shutil.rmtree(self.clone_dir)

        try:
            Repo.clone_from(self.github_url, self.clone_dir)
            static_files = glob.glob(f"{self.clone_dir}/*")
            relative_paths = [os.path.relpath(file_path, self.clone_dir) for file_path in static_files]
            for file in relative_paths:
                self.upload_file(file)
        # except Exception:
        #     raise Exception(f"Cant able to clone the repo {self.github_url}")

    def upload_file(self, file_name, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            response = self.client.upload_file(file_name, self.bucket_name, object_name)
        except ClientError as e:
            print(e)
            return False
        return True
