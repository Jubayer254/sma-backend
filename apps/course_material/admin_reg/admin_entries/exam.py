from django.contrib import admin
from course_material.models.exam import Exam
from course_material.admin_reg.admin_entries.inlines import QuestionInline
from course_material.admin_reg.user_action_log_mixin import AuditFieldsAdminMixin
from course_material.admin_reg.admin_entries.common_exclude import COMMON_EXCLUDE
from course_material.admin_reg.custom_form import ExamAdminForm
import nested_admin

@admin.register(Exam)
class ExamAdmin(AuditFieldsAdminMixin, nested_admin.NestedModelAdmin):
    form = ExamAdminForm
    list_display = ('title', 'batch', 'start_datetime', 'end_datetime')
    list_filter = ('batch',)
    search_fields = ('title', 'batch__name', 'batch__course__title')
    autocomplete_fields = ('batch',)
    inlines = [QuestionInline]
    exclude = COMMON_EXCLUDE