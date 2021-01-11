from django.db import models
from django.db.models import OuterRef, Subquery, Sum, F
from django.utils import timezone

from .models import Credit, Debit


class AccountManager(models.Manager):

    def get_with_balance(self):
        balance_credits = Credit.objects.filter(
            account=OuterRef('pk')).values('account_id').annotate(sum_credits=Sum('amount'))
        balance_debits = Debit.objects.filter(
            account=OuterRef('pk')).values('account_id').annotate(sum_debits=Sum('amount'))

        balance = self.annotate(
            credit_sum=Subquery(balance_credits.values('sum_credits')),
            debit_sum=Subquery(balance_debits.values('sum_debits')),
            balance=F('credit_sum') - F('debit_sum')
        ).values_list('name', 'balance')
        return balance




