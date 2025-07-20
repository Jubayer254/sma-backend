from rest_framework import serializers
from course_material.models.course import Course, Batch
from course_material.serializers.instructor import InstructorSerializer
from course_material.models.course import CourseDetail

class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetail
        fields = ['id', 'title', 'order', 'content', 'created_at', 'updated_at']
        
class CourseSerializer(serializers.ModelSerializer):
    course_details = CourseDetailSerializer(source='details', many=True)  # ✅ use related_name
    demo_video_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        exclude = ['demo_video']  # exclude raw file field

    def get_demo_video_url(self, obj):
        request = self.context.get('request')
        if not obj.demo_video:
            return None
        # build absolute URL for your public demo video streaming endpoint
        return request.build_absolute_uri(f"/api/courses/{obj.id}/demo-video/")

class BatchSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Batch
        fields = "__all__"