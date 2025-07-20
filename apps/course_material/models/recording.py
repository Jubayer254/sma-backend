from django.db import models
from course_material.models.base_model import BaseModel
from course_material.models.course import Batch
from course_material.minio_backend import MinioStorage
from django.core.validators import FileExtensionValidator

# 👇 Define the upload path function
def upload_to_recording_path(instance, filename):
    if instance.batch_id:
        return f'recordings/Batch {instance.batch_id}/{filename}'
    return f'recordings/unknown/{filename}'

class Recording(BaseModel):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='recordings')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    class_date = models.DateField(help_text="Date of the class this recording is for")
    recording_file = models.FileField(
        storage=MinioStorage(),  # ✅ Uses MinIO
        upload_to=upload_to_recording_path,  # ✅ Now dynamic and correct
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv'])]
    )

    def __str__(self):
        return f"{self.batch} - {self.title} ({self.class_date})"

    class Meta:
        db_table = 'recordings'
        ordering = ['-class_date', '-created_at']
        verbose_name = "4. Recording"
        verbose_name_plural = "4. Recordings"
