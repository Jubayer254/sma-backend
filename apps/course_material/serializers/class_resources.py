from rest_framework import serializers
from course_material.models.class_resources import ClassResource

class ClassResourceSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = ClassResource
        fields = ['id', 'title', 'description', 'class_date', 'external_link', 'download_url']

    def get_download_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/v1/proxy/resource/{obj.id}/')
