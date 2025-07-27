from django import forms
from course_material.models.course import Course
import os
from django.core.exceptions import ValidationError

class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean_demo_video_url(self):
        url = self.cleaned_data.get("demo_video_url", "")
        if url:
            _, ext = os.path.splitext(url.lower())
            allowed_extensions = ['.mp4', '.mkv', '.mov', '.avi', '.webm']
            if ext not in allowed_extensions:
                raise ValidationError(f"Only {allowed_extensions} are allowed. Found: {ext}")
        return url
