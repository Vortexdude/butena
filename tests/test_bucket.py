import boto3
import botocore
from app.settings import conf
s3 = boto3.resource('s3')


def test_bucket_exist():
    try:
        s3.head_object(Bucket=conf.BUCKET_NAME, Key='website/')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            assert False

        if e.response['Error']['Code'] == 403:
            assert "Cant access the bucket"
