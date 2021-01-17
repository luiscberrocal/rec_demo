from rec_demo.banking.exceptions import BankingException
from rec_demo.banking.models import TransactionType


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
