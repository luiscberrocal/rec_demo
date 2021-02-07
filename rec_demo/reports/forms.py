from django import forms
from django.utils.translation import gettext_lazy as _

from ..core.mixins import AuditableFormMixin


class ReportForm(forms.Form):
    type = forms.CharField(label=_('Type'), max_length=30)
