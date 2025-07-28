from rest_framework import serializers
from course_material.models.recording import Recording

class RecordingSerializer(serializers.ModelSerializer):
    stream_url = serializers.SerializerMethodField()

    class Meta:
        model = Recording
        fields = ['id', 'title', 'description', 'class_date', 'stream_url']

    def get_stream_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/v1/proxy/recording/{obj.id}/')
