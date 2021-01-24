from datetime import date
from decimal import Decimal

from django.utils.translation import gettext_lazy as _

from .exceptions import BankingException
from .forms import AccountForm
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
    payments = list()
    if number <= 1:
        payments.append(amount)
        return payments
    rounding = kwargs.get('rounding', '1.00')

    payment = (amount / Decimal(str(number))).quantize(Decimal(rounding))

    total = Decimal('0.00')
    for i in range(number):
        payments.append(payment)
        total += payment
    diff = amount - total
    if diff_to_last:
        payments[number - 1] += diff
    else:
        payments[0] += diff

    if True:
        total = Decimal('0.00')
        for payment in payments:
            total += payment
        if total != amount:
            raise BankingException(
                _(f'Error in split. The sum ({total}) should be equal to amount ({amount}). Check decimal presicion.'))
    return payments


def get_next_month_date(current_date, delta=1):
    year = current_date.year
    month = current_date.month
    day = current_date.day
    next_month = month + delta
    if 12 < next_month <= 24:
        year += 1
        next_month -= 12
    elif next_month > 24:
        raise BankingException('Only one year delta is supported')
    return date(year, next_month, day)


def divide_in_payments_with_dates(amount, number, start_date, diff_to_last=True, **kwargs):
    if number <= 0:
        raise BankingException('Number of splits need to be equal to or higher than 1')
    payments_only = divide_in_payments(amount, number, diff_to_last, **kwargs)
    payments = list()
    current_date = start_date
    for i in range(number):
        payments.append({'date': current_date, 'amount': payments_only[i]})
        current_date = get_next_month_date(current_date)
    return payments


def get_index_and_field_name(field_name, regexp=AccountForm.TRANSACTION_REGEXP):
    match = regexp.match(field_name)
    match_found = False
    parsed_field_name =  None
    parsed_index = None
    if match:
        match_found = True
        parsed_field_name = match.group(1)
        parsed_index = match.group(2)
    return match_found, parsed_field_name, parsed_index

