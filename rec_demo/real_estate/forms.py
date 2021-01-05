from django import forms

from .models import Company
from ..core.mixins import AuditableFormMixin


class CompanyForm(AuditableFormMixin, forms.ModelForm):
    class Meta:
        model = Company
        fields = (
            'name',
            'short_name',
            'logo'
        )


class ContractForm(AuditableFormMixin, forms.ModelForm):
    class Meta:
        fields = ('date', 'project')
