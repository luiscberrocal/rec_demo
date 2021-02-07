class AuditableViewMixin(object, ):
    def get_form_kwargs(self):
        kwargs = super(AuditableViewMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AdminAuditableMixin(object):
    readonly_fields = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class AuditableFormMixin(object):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AuditableFormMixin, self).__init__(*args, **kwargs)

    def clean(self):
        clean_data = super(AuditableFormMixin, self).clean()
        if hasattr(self, 'instance'):
            if self.instance.id is None:
                clean_data['created_by'] = self.user
            clean_data['modified_by'] = self.user
        return clean_data
