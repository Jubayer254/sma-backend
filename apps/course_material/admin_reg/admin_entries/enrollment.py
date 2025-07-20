from django.contrib import admin
from course_material.admin_reg.user_action_log_mixin import AuditFieldsAdminMixin
from course_material.admin_reg.admin_entries.common_exclude import COMMON_EXCLUDE
from course_material.models.enrollment import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(AuditFieldsAdminMixin, admin.ModelAdmin):
    list_display = ('student', 'batch', 'payment_status', 'enrollment_date')
    list_filter = ('payment_status', 'batch')
    search_fields = (
        'student__username', 'student__email', 'student__first_name', 'student__last_name',
        'batch__name', 'batch__course__title'
    )
    autocomplete_fields = ('student', 'batch')
    exclude = COMMON_EXCLUDE
