from storages.backends.s3boto3 import S3Boto3Storage
import boto3
from django.conf import settings
from botocore.config import Config

MINIO_ENDPOINT_URL = settings.MINIO_ENDPOINT
MINIO_ACCESS_KEY = settings.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = settings.MINIO_SECRET_KEY
MINIO_BUCKET_NAME = settings.MINIO_BUCKET_NAME

class MinioStorage(S3Boto3Storage):
    bucket_name = 'spark'
    custom_domain = False

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=MINIO_ENDPOINT_URL,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )
