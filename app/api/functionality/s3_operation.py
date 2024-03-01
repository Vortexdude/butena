from botocore.exceptions import ClientError
import boto3
from typing import List


class BaseS3Operation:
    """
    Base class for S3 operations.
    """

    def __init__(self):
        """
        Constructor to initialize S3 client.
        """

        self.client = boto3.client('s3')

    def list_files(self, bucket_name: str, key: str) -> List[str] | None:
        """
        List files in an S3 bucket with a given key prefix.

        Args:
            bucket_name (str): S3 bucket name.
            key (str): Prefix key in the bucket.

        Returns:
            List[str] | None: List of file keys or None if no files found.
        """

        files = []
        try:
            response = self.client.list_objects(Bucket=bucket_name, Prefix=key)
            if 'Contents' not in response:
                return None

            for item in response['Contents']:
                files.append(item['Key'])

        except ClientError as e:
            raise e

        return files

    def upload_file(self, bucket: str, file_name: str, key: str) -> bool:
        """
        Upload a file to an S3 bucket.

        Args:
            bucket (str): S3 bucket name.
            file_name (str): Local file name to be uploaded.
            key (str): Key in the S3 bucket.

        Returns:
            bool: True if upload is successful, False otherwise.
        """

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
        """
         Delete a file from an S3 bucket.

         Args:
             bucket (str): S3 bucket name.
             key (str): Key of the file to be deleted.

         Returns:
             bool: True if deletion is successful, False otherwise.
         """

        try:
            self.client.delete_object(Bucket=bucket, Key=key)
            return True

        except ClientError as e:
            raise e
