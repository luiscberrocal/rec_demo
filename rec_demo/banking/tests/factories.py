from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from ..forms import AccountForm
from ..models import TransactionType, Account
from ..utils import get_or_create_transaction_types, divide_in_payments_with_dates
from ...core.utils import clean_dict


class AccountFactory(object):

    @classmethod
    def create_account_for_apartment(cls, *args, **kwargs):
        account_name = args[0]
        app_user = args[1]
        contract = kwargs.get('contract', None)
        price = kwargs.get('price', contract.total_amount or Decimal('125000.00'))
        put_apart_payment = kwargs.get('put_apart_payment', None)
        down_payment_percentage = kwargs.get('down_payment_percentage', Decimal('0.15'))
        down_payment = kwargs.get('down_payment', price * down_payment_percentage)
        number_of_splits = kwargs.get('number_of_splits', 6)
        start_down_payments = kwargs.get('start_down_payments', timezone.now().date() + timedelta(days=30))

        loan_amount = price - down_payment
        if put_apart_payment is None:
            down_payment_to_split = down_payment
        else:
            down_payment_to_split = down_payment - put_apart_payment
        payments = divide_in_payments_with_dates(down_payment_to_split, number_of_splits, start_down_payments, )

        # app_user = SimpleUserFactory.create()
        get_or_create_transaction_types()

        down = TransactionType.objects.get(short_name='DOWN')
        loan = TransactionType.objects.get(short_name='LOAN')
        payment_type = TransactionType.objects.get(short_name='PAYMENT')

        account = Account.objects.create(name=account_name, created_by=app_user)
        account.add_debit(loan_amount, loan, created_by=app_user)

        if put_apart_payment is not None:
            debit = account.add_debit(put_apart_payment, down, created_by=app_user)
            account.add_credit(put_apart_payment, payment_type, created_by=app_user, related_debit=debit)

        for payment in payments:
            account.add_debit(payment['amount'], down, due_date=payment['date'])
        return account

    @classmethod
    def build_transaction_form_data(cls, account, clean_for='form'):
        index = 0
        pattern = AccountForm.TRANSACTION_PATTERN
        fields = ['type', 'date', 'account', 'transaction_type', 'amount', 'comments',
                  'due_date', 'related_debit',]# 'created', 'modified', 'created_by', 'modified_by']
        data_dict = dict()
        for transaction in account.transactions.all():
            for field in fields:
                field_name = pattern.format(field, index)
                data_dict[field_name] = getattr(transaction, field)
            index += 1
        clean_data_dict = clean_dict(data_dict, clean_for=clean_for)
        return clean_data_dict
