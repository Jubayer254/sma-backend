from rest_framework import viewsets, permissions
from course_material.models.enrollment import Enrollment
from course_material.serializers.enrollment import EnrollmentSerializer

class MyEnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)