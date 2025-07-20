from sma_backend.settings import BASE_DIR
import environ

# Read .env file existing at the same directory as this file.
env = environ.Env()
environ.Env.read_env()

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

MINIO_ENDPOINT = env('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = env('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = env('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = env('MINIO_BUCKET_NAME')
USE_HTTPS = env('USE_HTTPS')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY   # Change as per your setup
AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY  # Change as per your setup
AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET_NAME # Change as per your setup
AWS_S3_ENDPOINT_URL = MINIO_ENDPOINT  # or wherever your MinIO is running
AWS_S3_USE_SSL = USE_HTTPS # Set to True if using HTTPS
AWS_S3_FILE_OVERWRITE = env('AWS_S3_FILE_OVERWRITE') # Set to False to avoid overwriting files with the same name
AWS_DEFAULT_ACL = env('AWS_DEFAULT_ACL')  # Set to None to avoid ACL issues