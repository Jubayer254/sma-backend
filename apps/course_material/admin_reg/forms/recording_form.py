import os
from django import forms
from django.core.exceptions import ValidationError
from course_material.models.recording import Recording

class RecordingForm(forms.ModelForm):
    class Meta:
        model = Recording
        fields = '__all__'

    def clean_minio_browser_url(self):
        url = self.cleaned_data.get("minio_browser_url", "")
        if url:
            key_part = url.split('/browser/spark/')[-1]
            _, ext = os.path.splitext(key_part.lower())

            allowed_extensions = ['.mp4', '.mkv', '.mov', '.avi', '.webm']
            if ext not in allowed_extensions:
                raise ValidationError(f"Only video files are allowed. Found extension: {ext}")

        return url
