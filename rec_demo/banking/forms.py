import logging
import re

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Account, TransactionType, Transaction
from ..core.mixins import AuditableFormMixin
from ..real_estate.models import Contract

logger = logging.getLogger(__name__)


class AccountForm3(forms.ModelForm):
    TRANSACTION_PATTERN = 'cr_db_transaction_{}_{}'
    TRANSACTION_REGEXP = re.compile(r"cr_db_transaction_([a-z\_]+)_(\d+)")

    class Meta:
        model = Account
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        extras = kwargs.get('extras', 1)
        super(AccountForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        return cleaned_data


class AccountForm(AuditableFormMixin, forms.ModelForm):
    TRANSACTION_PATTERN = 'cr_db_transaction_{}_{}'
    TRANSACTION_REGEXP = re.compile(r"cr_db_transaction_([a-z\_]+)_(\d+)")

    class Meta:
        model = Account
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        extras = kwargs.get('extras', 1)
        super(AccountForm, self).__init__(*args, **kwargs)
        transaction_type_qs = TransactionType.objects.all()
        self.fields['contract'] = forms.ModelChoiceField(queryset=Contract.objects.all(),
                                                         label=_('Contract'))

        self.transaction_fields = dict()
        i = 0
        if self.instance.id is not None:
            transactions = self.instance.transactions.all()
            for transaction in transactions:
                self.transaction_fields[i] = self._build_transaction_fields(i, transaction_type_qs,
                                                                            transaction=transaction)
                i += 1
        if kwargs.get('data'):
            indexes = list()
            for field_name in kwargs['data'].keys():
                match = self.TRANSACTION_REGEXP.match(field_name)
                if match:
                    i = int(match.group(2))
                    if i not in indexes:
                        # print(f'transaction fields {i}')
                        self.transaction_fields[i] = self._build_transaction_fields(i, transaction_type_qs)
                    indexes.append(i)

        for k in range(extras):
            self.transaction_fields[i] = self._build_transaction_fields(i, transaction_type_qs)
            i += 1

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        transactions_dict = dict()
        transactions = list()
        c = 1
        for indexed_field_name in cleaned_data.keys():
            match = self.TRANSACTION_REGEXP.match(indexed_field_name)
            if match:
                #logger.debug(f'{c}. Matched field name {indexed_field_name}')
                field_name = match.group(1)
                index = match.group(2)
                if not transactions_dict.get(index):
                    transactions_dict[index] = dict()
                if field_name == 'related_debit':
                    if cleaned_data[indexed_field_name] == '':
                        cleaned_data[indexed_field_name] = None
                    else:
                        try:
                            tr = Transaction.objects.get(pk=cleaned_data[indexed_field_name])
                            cleaned_data[indexed_field_name] = tr
                        except TransactionType.DoesNotExist:
                            self.add_error(indexed_field_name, 'Transaction does not exist')

                if field_name == 'pk' and cleaned_data[indexed_field_name] == '':
                    cleaned_data[indexed_field_name] = None

                transactions_dict[index][field_name] = cleaned_data[indexed_field_name]
            else:
                logger.debug(f'{c} Not matched field name {indexed_field_name}')
            c += 1
        for key in transactions_dict.keys():
            transactions_data = transactions_dict[key]
            transactions.append(Transaction(**transactions_data))
        cleaned_data['transactions'] = transactions
        return cleaned_data

    def save(self, commit=True):
        instance = super(AccountForm, self).save(commit=False)

        if commit:
            instance.save()
            self.cleaned_data['contract'].account = instance
            self.cleaned_data['contract'].save()
            qs = instance.transactions
            if qs.count() != 0:
                qs.delete()
            for transaction in self.cleaned_data['transactions']:
                transaction.account = instance
            Transaction.objects.bulk_create(self.cleaned_data['transactions'])
        return instance

    def _build_transaction_fields(self, i, transaction_type_qs, **kwargs):
        transaction = kwargs.get('transaction', None)
        field_names = list()
        # Primary key
        # -----------------------------------------------------------
        field_name = self.TRANSACTION_PATTERN.format('pk', i)
        self.fields[field_name] = forms.CharField(label=_('pk'), required=False, widget=forms.HiddenInput())
        if transaction is not None:
            self.initial[field_name] = transaction.pk
        field_names.append(field_name)
        # Debit or credit
        # -----------------------------------------------------------
        field_name = self.TRANSACTION_PATTERN.format('type', i)
        choices = (
            (None, '---------'),
            (Transaction.DEBIT_TYPE, _('Debit')),
            (Transaction.CREDIT_TYPE, _('Credit'))
        )
        self.fields[field_name] = forms.ChoiceField(choices=choices, label=_('Type'), required=False)
        if transaction is not None:
            self.initial[field_name] = transaction.type
        field_names.append(field_name)
        # date
        # -----------------------------------------------------------
        field_name = self.TRANSACTION_PATTERN.format('date', i)
        self.fields[field_name] = forms.DateField(label=_('Date'), required=False)
        if transaction is not None:
            self.initial[field_name] = transaction.date
        field_names.append(field_name)
        # amount
        # -----------------------------------------------------------
        field_name = self.TRANSACTION_PATTERN.format('amount', i)
        self.fields[field_name] = forms.DecimalField(label=_('Amount'), max_digits=12, decimal_places=2,
                                                     required=False)
        if transaction is not None:
            self.initial[field_name] = transaction.amount
        field_names.append(field_name)
        # transaction_type
        # -----------------------------------------------------------
        field_name = self.TRANSACTION_PATTERN.format('transaction_type', i)
        self.fields[field_name] = forms.ModelChoiceField(queryset=transaction_type_qs,
                                                         label=_('Transaction Type'), required=False)
        if transaction is not None:
            self.initial[field_name] = transaction.transaction_type
        field_names.append(field_name)
        # comments
        # -----------------------------------------------------------
        field_name = self.TRANSACTION_PATTERN.format('comments', i)
        self.fields[field_name] = forms.CharField(max_length=60, label=_('Comments'), required=False)
        if transaction is not None:
            self.initial[field_name] = transaction.comments
        field_names.append(field_name)
        # due_date
        # -----------------------------------------------------------
        field_name = self.TRANSACTION_PATTERN.format('due_date', i)
        self.fields[field_name] = forms.DateField(label=_('Due date'), required=False)
        if transaction is not None:
            self.initial[field_name] = transaction.due_date
        field_names.append(field_name)
        # related_debit
        # -----------------------------------------------------------
        field_name = self.TRANSACTION_PATTERN.format('related_debit', i)
        self.fields[field_name] = forms.ChoiceField(label=_('Related debit'), required=False)
        if transaction is not None:
            self.initial[field_name] = transaction.related_debit
        field_names.append(field_name)

        return field_names

    def get_transaction_fields(self):
        for key in self.transaction_fields.keys():
            fields = [self[x] for x in self.transaction_fields[key]]
            yield key, *fields
