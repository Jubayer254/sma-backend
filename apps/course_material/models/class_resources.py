from django.db import models
from course_material.models.base_model import BaseModel
from course_material.minio_backend import MinioStorage
from course_material.models.course import Batch
from django.core.validators import FileExtensionValidator

# ✅ Helper to use batch ID in file path
def upload_to_batch_path(instance, filename):
    if instance.batch_id:
        return f'resources/Batch {instance.batch_id}/{filename}'
    return f'resources/unknown/{filename}'

class ClassResource(BaseModel):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    class_date = models.DateField(blank=True, null=True, help_text="Leave blank for general batch resources")

    file = models.FileField(
        storage=MinioStorage(),
        upload_to=upload_to_batch_path,  # ✅ This is the fix
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=[
                'pdf', 'docx', 'pptx', 'txt', 'csv', 'xlsx', 'jpg', 'jpeg', 'png'
            ])
        ]
    )
    external_link = models.URLField(max_length=500, blank=True)

    def __str__(self):
        if self.class_date:
            return f"{self.batch} - {self.title} ({self.class_date})"
        return f"{self.batch} - {self.title} (General)"

    class Meta:
        db_table = 'class_resources'
        ordering = ['class_date', 'created_at']
        verbose_name = "5. Class Resource"
        verbose_name_plural = "5. Class Resources"
