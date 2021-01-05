from django import forms
from django.utils.translation import ugettext_lazy as _
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
        extras = kwargs.get('extras', 1)
        super(ContractForm, self).__init__(*args, **kwargs)
        contract_clients = ContractClient.objects.filter(
            contract=self.instance
        )
        i = 0
        qs = Client.objects.all()
        for contract_client in contract_clients:
            field_name = f'contract_client_client_{i}'
            self.fields[field_name] = forms.ModelChoiceField(qs, required=False,label= _('Client') )
            self.initial[field_name] = contract_client.client
            field_name = f'contract_client_is_principal_{i}'
            self.fields[field_name] = forms.BooleanField(required=False,label= _('Is principal') )
            self.initial[field_name] = contract_client.is_principal
            i += 1
        for k in range(extras):
            field_name = f'contract_client_client_{i}'
            self.fields[field_name] = forms.ModelChoiceField(qs, required=False, label= _('Client'))
            self.initial[field_name] = None
            field_name = f'contract_client_is_principal_{i}'
            self.fields[field_name] = forms.BooleanField(required=False, label= _('Is principal'))
            self.initial[field_name] = False
            i += 1

        # for i in range(len(contract_clients) + 1):
        #     field_name = 'contract_client_client_%s' % (i,)
        #     qs = Client.objects.all()
        #     self.fields[field_name] = forms.ModelChoiceField(qs, required=False, )
        #     try:
        #         self.initial[field_name] = contract_clients[i].client
        #     except IndexError:
        #         self.initial[field_name] = None
        #         # create an extra blank field
        #         field_name = 'contract_client_contract_%s' % (i + 1,)
        #         self.fields[field_name] = forms.ModelChoiceField(qs, required=False, )

    class Meta:
        model = Contract
        fields = ('date', 'project')
