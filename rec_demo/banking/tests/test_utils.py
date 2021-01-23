from datetime import date
from decimal import Decimal

from django.test import SimpleTestCase

from ..utils import divide_in_payments, divide_in_payments_with_dates


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
