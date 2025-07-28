from django.db import models
from course_material.models.base_model import BaseModel
from course_material.models.instructor import Instructor
from datetime import timedelta, date
from urllib.parse import urlparse, unquote

class Course(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)

    demo_video_url = models.URLField(
        help_text="MinIO browser link (e.g. http://localhost:9001/browser/spark/...)",
        blank=True,
        null=True,
    )
    demo_video_object_key = models.CharField(max_length=500, blank=True, help_text="Auto-filled from demo_video_url")

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.demo_video_url:
            parsed = urlparse(self.demo_video_url)
            key_part = parsed.path.split('/browser/spark/')[-1]
            self.demo_video_object_key = unquote(key_part)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'courses'
        ordering = ['-created_at']
        verbose_name = "2. Course"
        verbose_name_plural = "2. Courses"


class CourseDetail(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255, help_text="E.g. Syllabus, Course Outline, Objectives")
    content = models.TextField(help_text="Detailed description or content for this section")
    order = models.PositiveIntegerField(default=0, help_text="Order for display sorting")

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        db_table = "course_details"
        ordering = ['order']
        verbose_name = "Course Detail"
        verbose_name_plural = "Course Details"

class Batch(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    instructors = models.ManyToManyField(Instructor, related_name='courses')
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.Boolean = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    class_time = models.TimeField()
    zoom_link = models.URLField(max_length=500)
    zoom_meeting_id = models.CharField(max_length=50, blank=True)
    zoom_passcode = models.CharField(max_length=20, blank=True)
    max_students = models.PositiveIntegerField(default=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.title} - {self.name}"

    def get_class_days_display(self):
        days = []
        if self.monday: days.append('Monday')
        if self.tuesday: days.append('Tuesday')
        if self.wednesday: days.append('Wednesday')
        if self.thursday: days.append('Thursday')
        if self.friday: days.append('Friday')
        if self.saturday: days.append('Saturday')
        if self.sunday: days.append('Sunday')
        return ", ".join(days)

    def get_selected_weekdays(self):
        days = []
        if self.monday: days.append('monday')
        if self.tuesday: days.append('tuesday')
        if self.wednesday: days.append('wednesday')
        if self.thursday: days.append('thursday')
        if self.friday: days.append('friday')
        if self.saturday: days.append('saturday')
        if self.sunday: days.append('sunday')
        return days

    def generate_class_dates(self):
        dates = []
        current_date = self.start_date
        weekday_mapping = {
            0: self.monday,
            1: self.tuesday,
            2: self.wednesday,
            3: self.thursday,
            4: self.friday,
            5: self.saturday,
            6: self.sunday,
        }
        while current_date <= self.end_date:
            if weekday_mapping.get(current_date.weekday(), False):
                dates.append(current_date)
            current_date += timedelta(days=1)
        return dates

    def get_next_class_date(self):
        today = date.today()
        for class_date in self.generate_class_dates():
            if class_date >= today:
                return class_date
        return None

    def get_total_classes(self):
        return len(self.generate_class_dates())

    class Meta:
        db_table = 'batches'
        ordering = ['start_date']
        verbose_name = "3. Batch"
        verbose_name_plural = "3. Batches"