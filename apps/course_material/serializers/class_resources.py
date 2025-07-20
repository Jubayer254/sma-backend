from rest_framework import serializers
from course_material.models.class_resources import ClassResource

class ClassResourceSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = ClassResource
        exclude = ['file']

    def get_download_url(self, obj):
        if not obj.file:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(f"/api/resources/{obj.id}/download/")