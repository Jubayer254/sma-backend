# course_material/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from course_material.views.class_resources import ResourceListView
from course_material.views.exam import ExamListView, QuestionListView, AnswerListView
from course_material.views.recording import RecordingListView
from course_material.views.course import CourseViewSet, BatchViewSet
from course_material.views.enrollment import MyEnrollmentViewSet

router = DefaultRouter()
router.register("courses", CourseViewSet, basename="course")
router.register("batches", BatchViewSet, basename="batch")
router.register("enrollments", MyEnrollmentViewSet, basename="enrollment")

urlpatterns = [
    path("", include(router.urls)),
    path("recordings/", RecordingListView.as_view(), name="recordings"),
    path("resources/", ResourceListView.as_view(), name="resources"),
    path("exams/", ExamListView.as_view(), name="exams"),
    path("exams/<int:exam_id>/questions/", QuestionListView.as_view(), name="exam-questions"),
    path("questions/<int:question_id>/answers/", AnswerListView.as_view(), name="question-answers"),
]