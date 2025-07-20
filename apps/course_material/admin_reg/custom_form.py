from django import forms
from course_material.admin_reg.time_widget import AMPMTimeField, SplitDateTimeAMPMField
from course_material.models.course import Batch
from course_material.models.exam import Exam

class BatchAdminForm(forms.ModelForm):
    class_time = AMPMTimeField(label="Class Time")

    class Meta:
        model = Batch
        fields = '__all__'


class ExamAdminForm(forms.ModelForm):
    start_datetime = SplitDateTimeAMPMField(label="Start Date and Time")
    end_datetime = SplitDateTimeAMPMField(label="End Date and Time")

    class Meta:
        model = Exam
        fields = '__all__'
