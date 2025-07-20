from rest_framework import generics, permissions
from course_material.models.recording import Recording
from course_material.serializers.recording import RecordingSerializer

class RecordingListView(generics.ListAPIView):
    serializer_class = RecordingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recording.objects.filter(batch__enrollments__student=self.request.user)