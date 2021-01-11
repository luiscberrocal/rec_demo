from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.
from model_utils.models import TimeStampedModel

from .managers import AccountManager
from ..core.models import Auditable


class Account(Auditable, TimeStampedModel):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    def add_credit(self, amount, **kwargs):
        credit_data = {'amount': amount}
        today = timezone.now().date()
        credit_data['date'] = kwargs.get('date', today)
        credit_data['comments'] = kwargs.get('comments', None)
        credit_data['related_debit'] = kwargs.get('related_debit', None)
        # credit_data['type'] = kwargs.get('type', Credit.)
        credit_data['account'] = self
        return Credit.objects.create(**credit_data)

    def add_debit(self, amount, **kwargs):
        debit_data = {'amount': amount}
        today = timezone.now().date()
        debit_data['date'] = kwargs.get('date', today)
        debit_data['comments'] = kwargs.get('comments', None)
        debit_data['related_debit'] = kwargs.get('related_debit', None)
        debit_data['type'] = kwargs.get('type', Debit.OTHER_TYPE)
        debit_data['account'] = self
        return Debit.objects.create(**debit_data)


class Debit(Auditable, TimeStampedModel):
    OTHER_TYPE = 'OTHER'
    DOWN_PAYMENT_TYPE = 'DOWN_PAYMENT'
    LEGAL_TYPE = 'LEGAL'
    TAX_TYPE = 'TAX'
    TYPE_CHOICES = (
        (OTHER_TYPE, _('Other')),
        (DOWN_PAYMENT_TYPE, _('Down payment')),
        (LEGAL_TYPE, _('Legal')),
        (TAX_TYPE, _('Tax')),
    )
    date = models.DateField(_("Date"))
    account = models.ForeignKey(Account, related_name='debits', on_delete=models.CASCADE,
                                verbose_name=_('Account'))
    type = models.CharField(_('Type'), max_length=12, choices=TYPE_CHOICES, default=OTHER_TYPE)
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2)
    comments = models.CharField(_('Comments'), max_length=60, null=True, blank=True)
    objects = AccountManager

    def __str__(self):
        return f'{self.amount.name} {self.amount}'


class Credit(Auditable, TimeStampedModel):
    date = models.DateField(_("Date"))
    account = models.ForeignKey(Account, related_name='credits', on_delete=models.CASCADE,
                                verbose_name=_('Account'))
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2)
    related_debit = models.ForeignKey(Debit, related_name='credits', verbose_name=_('Related debit'),
                                      on_delete=models.CASCADE, null=True, blank=True)
    comments = models.CharField(_('Comments'), max_length=60, null=True, blank=True)

    def __str__(self):
        return f'{self.amount.name} {self.amount}'
