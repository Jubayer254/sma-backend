from rest_framework import serializers
from course_material.models.course import Course, Batch
from course_material.models.course import CourseDetail

class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetail
        fields = ['id', 'title', 'order', 'content', 'created_at', 'updated_at']

class CourseSerializer(serializers.ModelSerializer):
    course_details = CourseDetailSerializer(source='details', many=True)
    demo_video_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        exclude = ['demo_video_object_key']

    def get_demo_video_url(self, obj):
        return obj.get_presigned_demo_video_url()


class BatchSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Batch
        fields = "__all__"