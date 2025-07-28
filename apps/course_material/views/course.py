from rest_framework import viewsets, permissions
from course_material.models.course import Course, Batch
from course_material.serializers.course import CourseSerializer, BatchSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class BatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Batch.objects.filter(is_active=True)
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Batch.objects.filter(enrollments__student=self.request.user)