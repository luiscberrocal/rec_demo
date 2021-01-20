from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Account, TransactionType
from ..core.mixins import AuditableFormMixin
from ..real_estate.models import Contract


class AccountForm(AuditableFormMixin, forms.ModelForm):
    TRANSACTION_PATTERN = 'cr_db_transaction_{}_{}'

    contract = forms.ModelChoiceField(queryset=Contract.objects.all(), label=_('Contract'))

    class Meta:
        model = Account
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        extras = kwargs.get('extras', 1)
        super(AccountForm, self).__init__(*args, **kwargs)
        transaction_type_qs = TransactionType.objects.all()
        self.transaction_fields = dict()
        i = 0
        self.transaction_fields[i] = self._build_transaction_fields(i, transaction_type_qs)

    def _build_transaction_fields(self, i, transaction_type_qs, **kwargs):
        field_names = list()
        # Transaction type
        field_name = self.TRANSACTION_PATTERN.format('type', i)
        choices = (
            (None, '---------'),
            ('DBT', _('Debit')),
            ('CDT', _('Credit'))
        )
        self.fields[field_name] = forms.ChoiceField(choices=choices, label=_('Type'))
        field_names.append(field_name)
        # date
        field_name = self.TRANSACTION_PATTERN.format('date', i)
        self.fields[field_name] = forms.DateField(label=_('Date'))
        field_names.append(field_name)
        # amount
        field_name = self.TRANSACTION_PATTERN.format('amount', i)
        self.fields[field_name] = forms.DateField(label=_('Amount'))
        field_names.append(field_name)
        # transaction_type
        field_name = self.TRANSACTION_PATTERN.format('transaction_type', i)
        self.fields[field_name] = forms.ModelChoiceField(queryset=transaction_type_qs, label=_('Transaction Type'))
        field_names.append(field_name)
        # comments
        field_name = self.TRANSACTION_PATTERN.format('comments', i)
        self.fields[field_name] = forms.CharField(max_length=60, label=_('Comments'), required=False)
        field_names.append(field_name)
        # due_date
        field_name = self.TRANSACTION_PATTERN.format('due_date', i)
        self.fields[field_name] = forms.DateField(label=_('Due date'))
        field_names.append(field_name)
        # related_debit
        field_name = self.TRANSACTION_PATTERN.format('related_debit', i)
        self.fields[field_name] = forms.ChoiceField(label=_('Related debit'))
        field_names.append(field_name)

        return field_names

    def get_transaction_fields(self):
        for key in self.transaction_fields.keys():
            fields = [self[x] for x in self.transaction_fields[key]]
            yield key, *fields
