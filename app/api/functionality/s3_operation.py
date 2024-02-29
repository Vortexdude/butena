from botocore.exceptions import ClientError
import boto3


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
