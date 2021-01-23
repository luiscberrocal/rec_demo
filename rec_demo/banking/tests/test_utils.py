from decimal import Decimal

from django.test import SimpleTestCase

from ..utils import divide_in_payments


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
