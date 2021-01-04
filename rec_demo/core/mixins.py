import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rolepermissions.roles import assign_role

from .exceptions import EMRPracticeCoreException


class AuditableViewMixin(object, ):
    def form_valid(self, form, ):
        if not form.instance.created_by:
            form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super(AuditableViewMixin, self).form_valid(form)




