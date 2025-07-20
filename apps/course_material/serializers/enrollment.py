from rest_framework import serializers
from course_material.models.enrollment import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'batch', 'payment_status', 'enrollment_date']
        read_only_fields = ['enrollment_date']  # Leave out 'payment_status'