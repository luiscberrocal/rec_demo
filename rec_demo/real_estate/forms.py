import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Company, Contract, ContractClient, Client, RealEstateSpace
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
    CLIENT_PATTERN = 'contract_client_client_{}'
    IS_PRINCIPAL_PATTERN = 'contract_client_is_principal_{}'
    BROKER_PATTERN = 'contract_broker_broker_{}'
    BROKER_IS_ACTIVE_PATTERN = 'contract_broker_is_active_{}'
    REAL_ESTATE_SPACE_PATTERN = 'real_estate_space_{}'

    def __init__(self, *args, **kwargs):
        extras = kwargs.get('extras', 1)
        super(ContractForm, self).__init__(*args, **kwargs)
        self._build_client_fields(extras, kwargs)
        self._build_real_estate_fields(extras, kwargs)

    def _build_real_estate_fields(self, extras, kwargs):
        self.real_estate_space_fields = dict()
        i = 0
        if self.instance.id is not None:
            real_estate_spaces = RealEstateSpace.objects.filter(contract=self.instance)
            self.estate_spaces_fields = dict()
            #qs = RealEstateSpace.objects.filter(contract__isnull=True, project=self.instance.project)
            qs = RealEstateSpace.objects.filter(project=self.instance.project)
            for real_estate_space in real_estate_spaces:
                self._add_real_estate_space_field(i, qs, real_estate_space)
                i += 1
        else:
            qs = RealEstateSpace.objects.filter(contract__isnull=True)

        if kwargs.get('data'):
            regexp = re.compile(ContractForm.REAL_ESTATE_SPACE_PATTERN[:-2] + r'(\d+)')
            for field_name in kwargs['data'].keys():
                match = regexp.match(field_name)
                if match:
                    new_index = int(match.group(1))
                    if new_index > i:
                        i = new_index
                    self._add_real_estate_space_field(i, qs)

        for k in range(extras):
            self._add_real_estate_space_field(i, qs)
            i += 1

    def _add_real_estate_space_field(self, i, qs, real_estate_space=None):
        self.real_estate_space_fields[i] = list()
        field_name = self.REAL_ESTATE_SPACE_PATTERN.format(i)
        self.fields[field_name] = forms.ModelChoiceField(qs, required=False, label=_('Real estate space'))
        if real_estate_space is not None:
            self.initial[field_name] = real_estate_space
        self.real_estate_space_fields[i].append(field_name)

    def _build_client_fields(self, extras, kwargs):
        contract_clients = ContractClient.objects.filter(contract=self.instance)
        self.client_fields = dict()
        i = 0
        qs = Client.objects.all()
        for contract_client in contract_clients:
            self.client_fields[i] = list()
            field_name = f'contract_client_client_{i}'
            self.fields[field_name] = forms.ModelChoiceField(qs, required=False, label=_('Client'))
            self.initial[field_name] = contract_client.client
            self.client_fields[i].append(field_name)
            field_name = f'contract_client_is_principal_{i}'
            self.fields[field_name] = forms.BooleanField(required=False, label=_('Is principal'))
            self.initial[field_name] = contract_client.is_principal
            self.client_fields[i].append(field_name)
            i += 1
        if kwargs.get('data'):
            client_regexp = re.compile(r'contract_client_client_(\d+)')
            is_principal_regexp = re.compile(r'contract_client_is_principal_(\d+)')
            for data_key in kwargs['data'].keys():
                match = client_regexp.match(data_key)
                if match:
                    new_index = int(match.group(1))
                    if new_index > i:
                        i = new_index
                    self.fields[data_key] = forms.ModelChoiceField(qs, required=False, label=_('Client'))

                match = is_principal_regexp.match(data_key)
                if match:
                    new_index = int(match.group(1))
                    if new_index > i:
                        i = new_index
                    self.fields[data_key] = forms.BooleanField(required=False, label=_('Is principal'))
        for k in range(extras):
            self.client_fields[i] = list()
            field_name = f'contract_client_client_{i}'
            self.fields[field_name] = forms.ModelChoiceField(qs, required=False, label=_('Client'))
            self.initial[field_name] = None
            self.client_fields[i].append(field_name)
            field_name = f'contract_client_is_principal_{i}'
            self.fields[field_name] = forms.BooleanField(required=False, label=_('Is principal'))
            self.initial[field_name] = False
            self.client_fields[i].append(field_name)
            i += 1

    class Meta:
        model = Contract
        fields = ('date', 'project')

    def clean(self):
        cleaned_data = super(ContractForm, self).clean()
        cleaned_data["clients"] = self._clean_client_fields(cleaned_data)
        cleaned_data["real_estate_spaces"] = self._clean_real_estate_spaces_fields(cleaned_data)

        return cleaned_data

    def _clean_real_estate_spaces_fields(self, cleaned_data):
        real_estate_spaces = list()
        real_estate_spaces_fields = set()
        i = 0
        while cleaned_data.get(self.REAL_ESTATE_SPACE_PATTERN.format(i)):
            field_name = self.REAL_ESTATE_SPACE_PATTERN.format(i)

            if field_name in real_estate_spaces_fields:
                self.add_error(field_name, 'Duplicate')
            else:
                real_estate_spaces_fields.add(field_name)
                real_estate_spaces.append(cleaned_data[field_name])
            i += 1
        return real_estate_spaces

    def _clean_client_fields(self, cleaned_data):
        clients = list()
        client_fields = set()
        i = 0
        client_field_name = f'contract_client_client_{i}'
        is_principal_field_name = f'contract_client_is_principal_{i}'
        while cleaned_data.get(client_field_name):
            client_data = dict()
            client_data['client'] = cleaned_data[client_field_name]
            client_data['is_principal'] = cleaned_data.get(is_principal_field_name, False)
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
        return clients

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

            qs = RealEstateSpace.objects.filter(contract=instance)
            if qs.count() != 0:
                qs.update(contract=None)
            real_estate_space_data = dict()
            real_estate_space_list = list()
            real_estate_space_data['contract'] = instance
            real_estate_space_data['modified_by'] = self.user
            for real_estate_space in self.cleaned_data['real_estate_spaces']:
                real_estate_space_list.append(real_estate_space.id)

            RealEstateSpace.objects.filter(pk__in=real_estate_space_list).update(**real_estate_space_data)

        return instance

    def get_client_fields(self):
        for key in self.client_fields.keys():
            yield key, self[self.client_fields[key][0]], self[self.client_fields[key][1]]

    def get_real_estate_space_fields(self):
        for position in self.real_estate_space_fields.keys():
            yield position, self[self.real_estate_space_fields[position][0]]
