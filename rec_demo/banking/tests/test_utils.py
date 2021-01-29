from datetime import date
from decimal import Decimal, getcontext

from django.test import SimpleTestCase

from ..forms import AccountForm
from ..utils import divide_in_payments, divide_in_payments_with_dates, get_index_and_field_name


class Test_divide_in_payments(SimpleTestCase):

    def test_divide_in_payments(self):
        amount = Decimal('1000.25')
        number = 7
        payments = divide_in_payments(amount, number)
        self.assertEqual(len(payments), 7)
        self.assertEqual(payments[6], Decimal('142.91'))
        self.assertEqual(payments[0], Decimal('142.89'))
        calculated_total = Decimal('0.00')
        for payment in payments:
            calculated_total += payment

        self.assertEqual(amount, calculated_total)

    def test_divide_in_payments_rounding(self):
        amount = Decimal('1233.25')
        number = 9
        rounding = '1'
        payments = divide_in_payments(amount, number, rounding=rounding)
        self.assertEqual(len(payments), 9)

        calculated_total = Decimal('0.00')
        for payment in payments:
            calculated_total += payment

        self.assertEqual(amount, calculated_total)
        self.assertEqual(payments[0], Decimal('137.00'))
        self.assertEqual(payments[number - 1], Decimal('137.25'))

    def test_divide_in_payments_mod_issue(self):
        amount = Decimal('18250.00')
        number = 6
        payments = divide_in_payments(amount, number)
        self.assertEqual(len(payments), 6)

        calculated_total = Decimal('0.00')
        for payment in payments:
            calculated_total += payment

        self.assertEqual(amount, calculated_total)
        self.assertEqual(payments[0], Decimal('3041.67'))
        self.assertEqual(payments[number - 1], Decimal('3041.65'))

    def test_divide_in_payments_with_dates(self):
        amount = Decimal('12433.27')
        number = 6
        start_date = date(2020, 11, 3)
        payments = divide_in_payments_with_dates(amount, number, start_date)
        self.assertEqual(len(payments), number)

        calculated_total = Decimal('0.00')
        for payment in payments:
            calculated_total += payment['amount']

        self.assertEqual(amount, calculated_total)
        self.assertEqual(payments[0]['amount'], Decimal('2072.21'))
        self.assertEqual(payments[0]['date'], start_date)
        self.assertEqual(payments[number - 1]['amount'], Decimal('2072.22'))
        self.assertEqual(payments[number - 1]['date'], date(2021, 4, 3))

    def test_rounding(self):
        decimal_context = getcontext()
        original_precision = decimal_context.prec
        decimal_context.prec = 16
        total = Decimal("18250")
        amount = Decimal("3041.67")
        rem = total % amount
        print(rem)
        div = total / amount
        srtring_div = str(div)
        decimal_part = srtring_div.split('.')[1]
        dp_dec = Decimal(decimal_part)
        rem2 = dp_dec * total
        print(rem2)
        decimal_context.prec = original_precision
        rem3 = total % amount
        print(rem3)

    def test_get_index_and_field_name(self):
        field_name = AccountForm.TRANSACTION_PATTERN.format('due_date', 0)
        result = get_index_and_field_name(field_name)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'due_date')
        self.assertEqual(result[2], '0')
