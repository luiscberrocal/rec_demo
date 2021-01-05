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
            self.fields[field_name] = forms.ModelChoiceField(qs, required=False, label=_('Client'))
            self.initial[field_name] = contract_client.client
            field_name = f'contract_client_is_principal_{i}'
            self.fields[field_name] = forms.BooleanField(required=False, label=_('Is principal'))
            self.initial[field_name] = contract_client.is_principal
            i += 1
        for k in range(extras):
            field_name = f'contract_client_client_{i}'
            self.fields[field_name] = forms.ModelChoiceField(qs, required=False, label=_('Client'))
            self.initial[field_name] = None
            field_name = f'contract_client_is_principal_{i}'
            self.fields[field_name] = forms.BooleanField(required=False, label=_('Is principal'))
            self.initial[field_name] = False
            i += 1

    class Meta:
        model = Contract
        fields = ('date', 'project')

    def clean(self):
        cleaned_data = super(ContractForm, self).clean()
        clients = list()
        client_fields = set()
        i = 0
        client_field_name = f'contract_client_client_{i}'
        is_principal_field_name = f'contract_client_is_principal_{i}'
        while cleaned_data.get(client_field_name):
            client_data = dict()
            client_data['client'] = cleaned_data[client_field_name]
            client_data['is_principal'] = cleaned_data[is_principal_field_name]
            if client_field_name in client_fields:
                self.add_error(client_field_name, 'Duplicate')
            elif is_principal_field_name in client_fields:
                self.add_error(is_principal_field_name, 'Duplicate')
            else:
                client_fields.add(client_field_name)
                client_fields.add(is_principal_field_name)
                clients.append(client_data)
            i += 1
            client_field_name = f'contract_client_client_{i}'
            is_principal_field_name = f'contract_client_is_principal_{i}'

        cleaned_data["clients"] = clients
        return cleaned_data

    def save(self, commit=True):
        instance = super(ContractForm, self).save(commit=False)

        if commit:
            instance.save()
            qs = ContractClient.objects.filter(contract=instance)
            if qs.count() != 0:
                qs.delete()
            for client_data in self.cleaned_data["clients"]:
                client_data['contract'] = instance
                client_data['created_by'] = self.user
                client_data['modified_by'] = self.user
                ContractClient.objects.create(**client_data)
        return instance

    # def save(self, commit=True):
    #     contract = super(ContractForm, self).save(commit=False)
    #     #contract.date = self.cleaned_data["date"]
    #     #contract.project = self.cleaned_data["project"]
    #     if commit:
    #         contract.save()
    #         ContractClient.objects.filter(contract=contract).delete()
    #         for client_data in self.cleaned_data["clients"]:
    #             client_data['contract'] = contract
    #             ContractClient.objects.create(**client_data)
    #     return contract