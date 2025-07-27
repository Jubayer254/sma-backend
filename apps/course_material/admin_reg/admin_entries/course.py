from django.contrib import admin
from course_material.models.course import Course, Batch
from course_material.admin_reg.user_action_log_mixin import AuditFieldsAdminMixin
from course_material.admin_reg.admin_entries.common_exclude import COMMON_EXCLUDE
from course_material.admin_reg.custom_form import BatchAdminForm
from course_material.admin_reg.admin_entries.inlines import CourseDetailInline
from course_material.admin_reg.forms.course_form import CourseAdminForm

@admin.register(Course)
class CourseAdmin(AuditFieldsAdminMixin, admin.ModelAdmin):
    form = CourseAdminForm  # ✅ Use custom form here
    inlines = [CourseDetailInline]
    list_display = ('title', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    readonly_fields = ('demo_video_object_key',)
    exclude = COMMON_EXCLUDE



@admin.register(Batch)
class BatchAdmin(AuditFieldsAdminMixin, admin.ModelAdmin):
    form = BatchAdminForm
    list_display = ('name', 'course', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'course')
    search_fields = ('name', 'course__title', 'course__description')
    autocomplete_fields = ('course',)
    exclude = COMMON_EXCLUDE

    # ✅ This improves the instructor field UI
    filter_horizontal = ('instructors',)
