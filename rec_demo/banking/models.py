from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.
from model_utils.models import TimeStampedModel

from .managers import AccountManager
from ..core.models import Auditable


class Account(Auditable, TimeStampedModel):
    name = models.CharField(max_length=32)
    objects = AccountManager()

    def __str__(self):
        return self.name

    def add_credit(self, amount, transaction_type, **kwargs):
        credit_data = {'amount': amount, 'type': Transaction.CREDIT_TYPE}
        today = timezone.now().date()
        credit_data['date'] = kwargs.get('date', today)
        credit_data['comments'] = kwargs.get('comments', None)
        credit_data['related_debit'] = kwargs.get('related_debit', None)
        credit_data['transaction_type'] = transaction_type
        credit_data['account'] = self
        return Transaction.objects.create(**credit_data)

    def add_debit(self, amount, transaction_type, **kwargs):
        if amount > Decimal('0.00'):
            amount *= Decimal('-1.00')
        debit_data = {'amount': amount, 'type': Transaction.DEBIT_TYPE}
        today = timezone.now().date()
        debit_data['date'] = kwargs.get('date', today)
        debit_data['due_date'] = kwargs.get('due_date', None)
        debit_data['comments'] = kwargs.get('comments', None)
        debit_data['transaction_type'] = transaction_type
        debit_data['account'] = self
        return Transaction.objects.create(**debit_data)

    def _add_transaction(self, t_type, amount, transaction_type, **kwargs):
        today = timezone.now().date()
        transaction_data = dict()
        if t_type == Transaction.DEBIT_TYPE:
            transaction_data['due_date'] = kwargs.get('due_date', None)
            if amount > Decimal('0.00'):
                amount *= Decimal('-1.00')
        else:
            transaction_data['related_debit'] = kwargs.get('related_debit', None)

        transaction_data['type'] = t_type
        transaction_data['amount'] = amount
        transaction_data['date'] = kwargs.get('date', today)

        transaction_data['comments'] = kwargs.get('comments', None)
        transaction_data['transaction_type'] = transaction_type
        transaction_data['account'] = self
        return Transaction.objects.create(**transaction_data)





class TransactionType(Auditable, TimeStampedModel):
    ALLOWED_FOR_ALL = 'ALL'
    ALLOWED_FOR_CREDIT = 'CRT'
    ALLOWED_FOR_DEBIT = 'DBT'
    ALLOWED_FOR_CHOICES = (
        (ALLOWED_FOR_DEBIT, _('Debit transactions')),
        (ALLOWED_FOR_ALL, _('All transactions')),
        (ALLOWED_FOR_CREDIT, _('Credit transactions')),
    )
    name = models.CharField(_('Name'), max_length=50)
    short_name = models.CharField(_('Short name'), max_length=20, unique=True)
    allowed_for = models.CharField(_("Allowed for"), max_length=3, default=ALLOWED_FOR_DEBIT)

    def __str__(self):
        return f'{self.name} ({self.allowed_for})'

    class Meta:
        ordering = ('name',)


class Debit(Auditable, TimeStampedModel):
    date = models.DateField(_("Date"))
    account = models.ForeignKey(Account, related_name='debits', on_delete=models.CASCADE,
                                verbose_name=_('Account'))
    transaction_type = models.ForeignKey(TransactionType, related_name='debits', on_delete=models.PROTECT,
                                         verbose_name=_('Type'))
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2)
    comments = models.CharField(_('Comments'), max_length=60, null=True, blank=True)
    due_date = models.DateField(_("Due date"), null=True, blank=True)

    def __str__(self):
        return f'{self.account.name} {self.amount}'

    def get_status(self):
        credit_total = self.credits.all().aggregate(Sum('amount'))['amount__sum']
        balance = credit_total - self.amount
        if balance != Decimal('0.00'):
            return _('UNPAID')
        latest_date = self.credits.latest('date').date
        if latest_date <= self.due_date:
            return _('PAID ON TIME')
        else:
            return _('PAID LATE')


class Credit(Auditable, TimeStampedModel):
    date = models.DateField(_("Date"))
    account = models.ForeignKey(Account, related_name='credits', on_delete=models.CASCADE,
                                verbose_name=_('Account'))
    transaction_type = models.ForeignKey(TransactionType, related_name='credits', on_delete=models.PROTECT,
                                         verbose_name=_('Type'))
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2)
    related_debit = models.ForeignKey(Debit, related_name='credits', verbose_name=_('Related debit'),
                                      on_delete=models.CASCADE, null=True, blank=True)
    comments = models.CharField(_('Comments'), max_length=60, null=True, blank=True)

    def __str__(self):
        return f'{self.amount.name} {self.amount}'


class Transaction(Auditable, TimeStampedModel):
    CREDIT_TYPE = 'C'
    DEBIT_TYPE = 'D'
    TYPE_CHOICES =(
        (CREDIT_TYPE, _('Credit')),
        (DEBIT_TYPE, _('Debit')),
    )
    type = models.CharField(_('Type'), max_length=1)
    date = models.DateField(_("Date"))
    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE,
                                verbose_name=_('Account'))
    transaction_type = models.ForeignKey(TransactionType, related_name='transactions', on_delete=models.PROTECT,
                                         verbose_name=_('Type'))
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2)
    comments = models.CharField(_('Comments'), max_length=60, null=True, blank=True)
    due_date = models.DateField(_("Due date"), null=True, blank=True)
    related_debit = models.ForeignKey('self', related_name='credits', verbose_name=_('Related debit'),
                                      on_delete=models.CASCADE, null=True, blank=True)

    def get_status(self):
        if self.type == self.DEBIT_TYPE:
            # noinspection DuplicatedCode
            credit_total = self.credits.all().aggregate(Sum('amount'))['amount__sum']
            balance = credit_total + self.amount
            if balance != Decimal('0.00'):
                return _('UNPAID')
            latest_date = self.credits.latest('date').date
            if latest_date <= self.due_date:
                return _('PAID ON TIME')
            else:
                return _('PAID LATE')
        else:
            return None

    def __str__(self):
        return f'{self.account.name} {self.amount}'

    class Meta:
        ordering = ('date',)
