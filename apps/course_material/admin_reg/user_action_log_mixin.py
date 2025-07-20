class AuditFieldsAdminMixin:
    def save_model(self, request, obj, form, change):
        if not change and not getattr(obj, 'created_by', None):
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if not obj.pk and not getattr(obj, 'created_by', None):
                obj.created_by = request.user
            obj.updated_by = request.user
            obj.save()
        formset.save_m2m()