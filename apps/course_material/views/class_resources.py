from rest_framework import permissions, generics
from course_material.models.class_resources import ClassResource
from course_material.serializers.class_resources import ClassResourceSerializer

class ResourceListView(generics.ListAPIView):
    serializer_class = ClassResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ClassResource.objects.filter(batch__enrollments__student=self.request.user)