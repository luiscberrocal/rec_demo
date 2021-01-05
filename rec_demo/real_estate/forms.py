from django import forms

from .models import Company, Contract, ContractClient, Client
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

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        contract_clients = ContractClient.objects.filter(
            contract=self.instance
        )
        for i in range(len(contract_clients) + 1):
            field_name = 'contract_client_client_%s' % (i,)
            qs = Client.objects.all()
            self.fields[field_name] = forms.ModelChoiceField(qs, required=False, )
            try:
                self.initial[field_name] = contract_clients[i].client
            except IndexError:
                self.initial[field_name] = None
                # create an extra blank field
                field_name = 'contract_client_contract_%s' % (i + 1,)
                self.fields[field_name] = forms.ModelChoiceField(qs, required=False, )


    class Meta:
        model = Contract
        fields = ('date', 'project')
