from django.db import models
from course_material.models.course import Batch
from course_material.models.base_model import BaseModel
from urllib.parse import urlparse, unquote
from django.conf import settings
from course_material.minio_backend import get_s3_client

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

    def __str__(self):
        return f"{self.batch} - {self.title}"

    class Meta:
        verbose_name = '4. Recording'
        verbose_name_plural = '4. Recordings'