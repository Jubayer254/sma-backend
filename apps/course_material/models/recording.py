from django.db import models
from course_material.models.course import Batch
from course_material.models.base_model import BaseModel
from urllib.parse import urlparse, unquote
from django.conf import settings
import boto3
from botocore.config import Config

class Recording(BaseModel):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='recordings')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    class_date = models.DateField()

    minio_browser_url = models.URLField(blank=True)
    object_key = models.CharField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        if self.minio_browser_url:
            parsed = urlparse(self.minio_browser_url)
            key_part = parsed.path.split('/browser/spark/')[-1]
            self.object_key = unquote(key_part)
        super().save(*args, **kwargs)

    def get_presigned_url(self, expires=3600):
        if not self.object_key:
            return None
        s3 = boto3.client(
            's3',
            endpoint_url=settings.MINIO_ENDPOINT,
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
        )
        try:
            return s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.MINIO_BUCKET_NAME, 'Key': self.object_key},
                ExpiresIn=expires,
                config=Config(signature_version='s3v4')
            )
        except Exception:
            return None

    def __str__(self):
        return f"{self.batch} - {self.title}"

    class Meta:
        verbose_name = '4. Recording'
        verbose_name_plural = '4. Recordings'