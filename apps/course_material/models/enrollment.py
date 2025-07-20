from django.db import models
from course_material.models.base_model import BaseModel
from django.contrib.auth import get_user_model
from course_material.models.course import Batch

User = get_user_model()

class Enrollment(BaseModel):

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.batch}"

    class Meta:
        db_table = 'enrollments'
        unique_together = ['student', 'batch']
        ordering = ['-enrollment_date']
        verbose_name = "7. Enrollment"
        verbose_name_plural = "7. Enrollments"