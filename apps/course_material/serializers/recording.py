from rest_framework import serializers
from course_material.models.recording import Recording

class RecordingSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Recording
        exclude = ['recording_file']

    def get_download_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f"/api/recordings/{obj.id}/download/")