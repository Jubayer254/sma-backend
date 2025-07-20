from rest_framework import generics, permissions
from course_material.models.exam import Exam, Question, Answer
from course_material.serializers.exam import ExamSerializer, QuestionSerializer, AnswerSerializer
from course_material.models.class_resources import ClassResource
from course_material.serializers.class_resources import ClassResourceSerializer

class ResourceListView(generics.ListAPIView):
    serializer_class = ClassResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ClassResource.objects.filter(batch__enrollments__student=self.request.user)

class ExamListView(generics.ListAPIView):
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Exam.objects.filter(batch__enrollments__student=self.request.user)

class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Question.objects.filter(exam_id=self.kwargs['exam_id'])

class AnswerListView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Answer.objects.filter(question_id=self.kwargs['question_id'])