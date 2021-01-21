from decimal import Decimal

from django.db import models
from django.db.models import OuterRef, Subquery, Sum, F
from django.db.models.functions import Coalesce


class AccountManager(models.Manager):

    def get_with_balance(self):
        from .models import Credit, Debit
        balance_credits = Credit.objects.filter(
            account=OuterRef('pk')).values('account_id').annotate(sum_credits=Sum('amount'))
        balance_debits = Debit.objects.filter(
            account=OuterRef('pk')).values('account_id').annotate(sum_debits=Sum('amount'))

        balance = self.annotate(
            credit_sum=Coalesce(Subquery(balance_credits.values('sum_credits')), Decimal('0.00')),
            debit_sum=Coalesce(Subquery(balance_debits.values('sum_debits')), Decimal('0.00')),
            balance=F('credit_sum') - F('debit_sum')
        ).values_list('name', 'balance')
        return balance

    def with_totals(self):
        from .models import Transaction
        balance_credits = Transaction.objects.filter(
            account=OuterRef('pk'), type=Transaction.CREDIT_TYPE
        ).values('account_id').annotate(sum_credits=Sum('amount'))

        balance_debits = Transaction.objects.filter(
            account=OuterRef('pk'), type=Transaction.DEBIT_TYPE
        ).values('account_id').annotate(sum_debits=Sum('amount'))

        balance = self.annotate(
            credit_sum=Coalesce(Subquery(balance_credits.values('sum_credits')), Decimal('0.00')),
            debit_sum=Coalesce(Subquery(balance_debits.values('sum_debits')), Decimal('0.00')),
            balance=F('credit_sum') + F('debit_sum')
        ) #.values_list('name', 'balance')
        return balance
