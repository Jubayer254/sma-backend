from django.contrib import admin
from course_material.models.instructor import Instructor
from course_material.admin_reg.user_action_log_mixin import AuditFieldsAdminMixin
from course_material.admin_reg.admin_entries.common_exclude import COMMON_EXCLUDE

@admin.register(Instructor)
class InstructorAdmin(AuditFieldsAdminMixin, admin.ModelAdmin):
    list_display = ('user', 'expertise')
    search_fields = (
        'user__username', 'user__email', 'user__first_name', 'user__last_name', 'expertise'
    )
    autocomplete_fields = ('user',)
    exclude = COMMON_EXCLUDE
