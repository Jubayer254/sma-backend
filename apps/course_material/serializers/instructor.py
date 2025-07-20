from rest_framework import serializers
from django.contrib.auth import get_user_model
from course_material.models.instructor import Instructor

User = get_user_model()

class InstructorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = ["id", "full_name", "user_id", "bio", "expertise", "profile_image"]

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username