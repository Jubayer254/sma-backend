from rest_framework import serializers
from course_material.models.course import Course, Batch
from course_material.models.course import CourseDetail

class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetail
        fields = ['id', 'title', 'order', 'content', 'created_at', 'updated_at']

class CourseSerializer(serializers.ModelSerializer):
    course_details = CourseDetailSerializer(source='details', many=True)
    demo_video_proxy_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        exclude = ['demo_video_object_key', 'demo_video_url']

    def get_demo_video_proxy_url(self, obj):
        request = self.context.get('request')
        if not obj.demo_video_object_key:
            return None
        # Construct proxy URL for demo video streaming
        return request.build_absolute_uri(f'/api/v1/proxy/demo-video/{obj.id}/')


class BatchSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Batch
        fields = "__all__"