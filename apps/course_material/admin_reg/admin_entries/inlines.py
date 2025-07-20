import nested_admin
from course_material.models.exam import Question, Answer
from django.contrib import admin
from course_material.models.course import CourseDetail

COMMON_EXCLUDE = ('created_by', 'updated_by')

class AnswerInline(nested_admin.NestedStackedInline):  # ✅ switched to stacked
    model = Answer
    extra = 1
    exclude = COMMON_EXCLUDE
    fieldsets = (
        (None, {'fields': ('answer_text', 'is_correct')}),
    )


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInline]
    extra = 1
    exclude = COMMON_EXCLUDE

class CourseDetailInline(admin.StackedInline):
    model = CourseDetail
    extra = 1
    exclude = COMMON_EXCLUDE
    ordering = ['order']
    fieldsets = (
        (None, {'fields': ('title', 'order', 'content')}),
    )
