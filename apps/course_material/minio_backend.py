from storages.backends.s3boto3 import S3Boto3Storage

class MinioStorage(S3Boto3Storage):
    bucket_name = 'spark'
    custom_domain = False
