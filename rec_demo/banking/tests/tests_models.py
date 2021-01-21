from datetime import timedelta, date
from decimal import Decimal

from django.db.models import OuterRef, Subquery, F, Sum
from django.utils import timezone
from test_plus import TestCase

from ..models import Account, Credit, Debit, TransactionType
from ..utils import get_or_create_transaction_types


class TestAccount(TestCase):
    # https://mixedquantum.blogspot.com/2017/08/django-tips-3-subquery-expressions.html

    def setUp(self) -> None:
        get_or_create_transaction_types()
        ## Debit transaction
        self.down_payment_transaction_type = TransactionType.objects.get(short_name='DOWN')
        self.payment_transaction_type = TransactionType.objects.get(short_name='PAYMENT')

        self.accounts = dict()
        self.accounts['fox'] = Account.objects.create(name='FOX')
        self.accounts['dog'] = Account.objects.create(name='DOG')
        self.accounts['snake'] = Account.objects.create(name='SNAKE')
        """
        # Credits
        +----------------+-----------------+
        | account_name   |   credit_amount |
        |----------------+-----------------|
        | FOX            |           100.0 |
        | SNAKE          |            50.0 |
        | SNAKE          |            20.0 |
        | DOG            |           300.0 |
        +----------------+-----------------+
        """

        today = timezone.now().date()
        yesterday = timezone.now().date() - timedelta(days=1)
        Credit.objects.create(account=self.accounts['fox'], amount=Decimal('100.0'), date=today,
                              transaction_type=self.payment_transaction_type)
        Credit.objects.create(account=self.accounts['snake'], amount=Decimal('50.0'), date=today,
                              transaction_type=self.payment_transaction_type)
        Credit.objects.create(account=self.accounts['snake'], amount=Decimal('20.0'), date=today,
                              transaction_type=self.payment_transaction_type)
        Credit.objects.create(account=self.accounts['dog'], amount=Decimal('300.0'), date=today,
                              transaction_type=self.payment_transaction_type)
        """
        # Debits
        +----------------+----------------+
        | account_name   |   dedit_amount |
        |----------------+----------------|
        | FOX            |           40.0 |
        | SNAKE          |           30.0 |
        | DOG            |           12.0 |
        | DOG            |           23.0 |
        +----------------+----------------+
        """

        Debit.objects.create(account=self.accounts['fox'],
                             amount=Decimal('40.0'), date=yesterday, transaction_type=self.down_payment_transaction_type)
        Debit.objects.create(account=self.accounts['snake'], amount=Decimal('30.0'), date=today,
                             transaction_type=self.down_payment_transaction_type)
        Debit.objects.create(account=self.accounts['dog'], amount=Decimal('12.0'), date=today,
                             transaction_type=self.down_payment_transaction_type)
        Debit.objects.create(account=self.accounts['dog'], amount=Decimal('23.0'), date=today,
                             transaction_type=self.down_payment_transaction_type)

    def test_sum(self):
        credits = Credit.objects.filter(
            account=OuterRef('pk')).values('account_id').annotate(sum_credits=Sum('amount'))
        debits = Debit.objects.filter(
            account=OuterRef('pk')).values('account_id').annotate(sum_debits=Sum('amount'))

        balances = Account.objects.annotate(
            credit_sum=Subquery(credits.values('sum_credits')),
            debit_sum=Subquery(debits.values('sum_debits')),
            balance=F('credit_sum') - F('debit_sum')
        ).values_list('name', 'balance')

        self.assertEqual(balances[0], ('FOX', Decimal('60.0')))
        self.assertEqual(balances[2], ('SNAKE', Decimal('40.0')))
        self.assertEqual(balances[1], ('DOG', Decimal('265.0')))

    def test_sum2(self):
        today = timezone.now().date()
        Debit.objects.create(account=self.accounts['fox'], transaction_type=self.down_payment_transaction_type,
                             amount=Decimal('20.75'), date=today)
        credits = Credit.objects.filter(
            account=OuterRef('pk')).values('account_id').annotate(sum_credits=Sum('amount'))
        debits = Debit.objects.filter(
            account=OuterRef('pk')).values('account_id').annotate(sum_debits=Sum('amount'))

        fox_balance = Account.objects.annotate(
            credit_sum=Subquery(credits.values('sum_credits')),
            debit_sum=Subquery(debits.values('sum_debits')),
            balance=F('credit_sum') - F('debit_sum')
        ).values_list('name', 'balance').get(name__exact='FOX')

        self.assertEqual(fox_balance, ('FOX', Decimal('39.25')))

    def test_add_credit(self):
        name = 'PH Victorial Hills 15A'

        account = Account.objects.create(name=name)
        account.add_debit(Decimal('108000'), transaction_type=self.down_payment_transaction_type)
        account.add_debit(Decimal('12000'), transaction_type=self.down_payment_transaction_type)
        # account.add_credit(Decimal('0.00'))

        account = Account.objects.with_totals().get(pk=account.id)
        self.assertEqual(account.name, name)
        self.assertEqual(account.balance, Decimal('-120000'))

    def test_get_status(self):
        name = 'PH Victorial Hills 15A'

        account = Account.objects.create(name=name)
        due_date = date(2020, 1, 1)
        debit = account.add_debit(Decimal('10000'), transaction_type=self.down_payment_transaction_type, due_date=due_date)
        account.add_credit(Decimal('1000.00'), transaction_type=self.down_payment_transaction_type, related_debit=debit)
        account.add_credit(Decimal('1000.00'), transaction_type=self.down_payment_transaction_type, related_debit=debit)
        status = debit.get_status()
        self.assertEqual(status, 'UNPAID')

    def test_get_status_paid_late(self):
        name = 'PH Victorial Hills 15A'
        account = Account.objects.create(name=name)
        due_date = date(2020, 1, 1)
        debit = account.add_debit(Decimal('10000.00'), transaction_type=self.down_payment_transaction_type,
                                  due_date=due_date)
        credit = account.add_credit(Decimal('10000.00'), transaction_type=self.payment_transaction_type,
                                    related_debit=debit)
        status = debit.get_status()
        self.assertEqual(status, 'PAID LATE')

    def test_get_status_paid_on_time(self):
        name = 'PH Victorial Hills 15A'
        account = Account.objects.create(name=name)
        due_date = date(2020, 1, 1)
        debit = account.add_debit(Decimal('1000.00'), transaction_type=self.down_payment_transaction_type, due_date=due_date)
        credit = account.add_credit(Decimal('1000.00'), transaction_type=self.payment_transaction_type,
                                    related_debit=debit, date=due_date)
        status = debit.get_status()
        self.assertEqual(status, 'PAID ON TIME')

    def test_get_status_paid_late_multiple_credits(self):
        name = 'PH Victorial Hills 15A'
        account = Account.objects.create(name=name)
        due_date = date(2020, 1, 1)
        debit = account.add_debit(Decimal('1000.00'), transaction_type=self.down_payment_transaction_type, due_date=due_date)
        account.add_credit(Decimal('500.00'), transaction_type=self.payment_transaction_type, related_debit=debit,
                           date=due_date)
        account.add_credit(Decimal('500.00'), transaction_type=self.payment_transaction_type, related_debit=debit)
        status = debit.get_status()
        self.assertEqual(status, 'PAID LATE')
