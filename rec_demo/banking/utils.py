from datetime import date
from decimal import Decimal

from .exceptions import BankingException
from .models import TransactionType


def get_or_create_transaction_types():
    transaction_types = list()
    ## DEBITS
    transaction_types.append({'name': 'Abono incial', 'short_name': 'DOWN',
                              'allowed_for': TransactionType.ALLOWED_FOR_DEBIT, })
    transaction_types.append({'name': 'Préstamo hipotecario', 'short_name': 'LOAN',
                              'allowed_for': TransactionType.ALLOWED_FOR_DEBIT})
    transaction_types.append({'name': 'Fondo inicial de mantenimiento', 'short_name': 'MAINTENANCE',
                              'allowed_for': TransactionType.ALLOWED_FOR_DEBIT})
    transaction_types.append({'name': 'Minuta de cancelación', 'short_name': 'MINUTA',
                              'allowed_for': TransactionType.ALLOWED_FOR_DEBIT})
    transaction_types.append({'name': 'Gastos legales', 'short_name': 'LEGAL',
                              'allowed_for': TransactionType.ALLOWED_FOR_DEBIT})
    transaction_types.append({'name': 'Alza de materiales', 'short_name': 'MATERIALS',
                              'allowed_for': TransactionType.ALLOWED_FOR_DEBIT})
    ## ALL
    transaction_types.append({'name': 'Alza/baja de metraje', 'short_name': 'AREA',
                              'allowed_for': TransactionType.ALLOWED_FOR_ALL})
    transaction_types.append({'name': 'Corrección', 'short_name': 'CORRECTION',
                              'allowed_for': TransactionType.ALLOWED_FOR_ALL})
    transaction_types.append({'name': 'Otros', 'short_name': 'OTHER',
                              'allowed_for': TransactionType.ALLOWED_FOR_ALL})

    ## CREDITS
    transaction_types.append({'name': 'Pago', 'short_name': 'PAYMENT',
                              'allowed_for': TransactionType.ALLOWED_FOR_CREDIT})
    new_transaction_types = list()
    for transaction_type in transaction_types:
        count = TransactionType.objects.filter(short_name=transaction_type['short_name']).count()
        if count == 0:
            new_transaction_type = TransactionType(**transaction_type)
            new_transaction_types.append(new_transaction_type)
            transaction_type['created'] = True
        elif count == 1:
            transaction_type['created'] = False
        else:
            raise BankingException(f'Repeated transaction type exists {transaction_type["short_name"]}')

    TransactionType.objects.bulk_create(new_transaction_types)

    return transaction_types


def divide_in_payments(amount, number, diff_to_last=True, **kwargs):
    if number <= 1:
        return amount
    rounding = kwargs.get('rounding', '1.00')
    payment = (amount / Decimal(str(number))).quantize(Decimal(rounding))
    remainder = amount % payment
    payments = list()
    for i in range(number):
        payments.append(payment)
    if remainder != Decimal('0.00'):
        if diff_to_last:
            payments[number - 1] = payments[number - 1] + remainder
        else:
            payments[0] = payments[0] + remainder
    return payments


def get_next_month_date(current_date, delta=1):
    year = current_date.year
    month = current_date.month
    day = current_date.day
    next_month = month + delta
    if 12 < next_month <= 24:
        year += 1
        next_month -= 12
    return date(year, next_month, day)


def divide_in_payments_with_dates(amount, number, start_date, diff_to_last=True, **kwargs):
    payments_only = divide_in_payments(amount, number, diff_to_last, **kwargs)
    payments = list()
    current_date = start_date
    for i in range(number):
        payments.append({'date': current_date, 'amount': payments_only[i]})
        current_date = get_next_month_date(current_date)
    return payments

