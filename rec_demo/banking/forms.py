from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Account, TransactionType
from ..core.mixins import AuditableFormMixin
from ..real_estate.models import Contract


class AccountForm(AuditableFormMixin, forms.ModelForm):
    TRANSACTION_PATTERN = 'transaction_{}_{}'

    contract = forms.ModelChoiceField(queryset=Contract.objects.all(), label=_('Contract'))

    class Meta:
        model = Account
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        extras = kwargs.get('extras', 1)
        super(AccountForm, self).__init__(*args, **kwargs)
        transaction_type_qs = TransactionType.objects.all()
        self._build_transaction_fields(0, transaction_type_qs)

    def _build_transaction_fields(self, i, transaction_type_qs, **kwargs):

        # Transaction type
        field_name = self.TRANSACTION_PATTERN.format('type', i)
        choices = (
            ('DBT', _('Debit')),
            ('CDT', _('Credit'))
        )
        self.fields[field_name] = forms.ChoiceField(choices=choices, label=_('Type'))
        # date
        field_name = self.TRANSACTION_PATTERN.format('date', i)
        self.fields[field_name] = forms.DateField(label=_('Date'))
        # amount
        field_name = self.TRANSACTION_PATTERN.format('amount', i)
        self.fields[field_name] = forms.DateField(label=_('Amount'))
        # transaction_type
        field_name = self.TRANSACTION_PATTERN.format('transaction_type', i)
        self.fields[field_name] = forms.ModelChoiceField(queryset=transaction_type_qs, label=_('Transaction Type'))
        # comments
        field_name = self.TRANSACTION_PATTERN.format('comments', i)
        self.fields[field_name] = forms.CharField(max_length=60, label=_('Comments'), required=False)
        # due_date
        field_name = self.TRANSACTION_PATTERN.format('due_date', i)
        self.fields[field_name] = forms.DateField(label=_('Due date'))



