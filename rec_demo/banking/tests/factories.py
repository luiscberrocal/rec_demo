from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from ..models import TransactionType, Account
from ..utils import get_or_create_transaction_types, divide_in_payments_with_dates


class AccountFactory(object):

    @classmethod
    def create_account_for_apartment(cls, *args, **kwargs):
        account_name = args[0]
        app_user = args[1]
        price = kwargs.get('price', Decimal('125000.00'))
        put_apart_payment = kwargs.get('put_apart_payment', Decimal('500.00'))
        down_payment_percentage = kwargs.get('down_payment_percentage', Decimal('0.15'))
        down_payment = kwargs.get('down_payment', price * down_payment_percentage)
        number_of_splits = kwargs.get('number_of_splits', 6)
        start_down_payments = kwargs.get('start_down_payments', timezone.now().date() + timedelta(days=30))

        loan_amount = price - down_payment
        down_payment_to_split = down_payment - put_apart_payment
        payments = divide_in_payments_with_dates(down_payment_to_split, number_of_splits, start_down_payments, )

        # app_user = SimpleUserFactory.create()
        get_or_create_transaction_types()

        down = TransactionType.objects.get(short_name='DOWN')
        loan = TransactionType.objects.get(short_name='LOAN')
        payment_type = TransactionType.objects.get(short_name='PAYMENT')

        account = Account.objects.create(name=account_name, created_by=app_user)
        account.add_debit(loan_amount, loan, created_by=app_user)
        debit = account.add_debit(put_apart_payment, down, created_by=app_user)
        account.add_credit(put_apart_payment, payment_type, created_by=app_user, related_debit=debit)

        for payment in payments:
            account.add_debit(payment['amount'], down, due_date=payment['date'])
        return account
