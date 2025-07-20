from django.contrib import admin
from course_material.models.recording import Recording
from course_material.admin_reg.user_action_log_mixin import AuditFieldsAdminMixin
from course_material.admin_reg.admin_entries.common_exclude import COMMON_EXCLUDE

@admin.register(Recording)
class RecordingAdmin(AuditFieldsAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'batch', 'class_date')
    list_filter = ('batch', 'class_date')
    search_fields = ('title', 'batch__name', 'batch__course__title')
    autocomplete_fields = ('batch',)
    exclude = COMMON_EXCLUDE