from django import forms

from .models import Company


class CompanyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CompanyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Company
        fields = (
            'name',
            'short_name',
            'logo'
        )

    def clean(self):
        clean_data = super(CompanyForm, self).clean()
        if self.instance is None:
            clean_data['created_by'] = self.user
        clean_data['updated_by'] = self.user
        return clean_data


