from decimal import Decimal

from test_plus import TestCase

from .factories import AccountFactory
from ..models import Account
from ...users.tests.factories import SimpleUserFactory


class TestAccountFactory(TestCase):

    def test_create_account_for_apartment(self):
        name = 'Account 1'
        user = SimpleUserFactory.create()
        account = AccountFactory.create_account_for_apartment(name, user, put_apart_payment=Decimal('500.00'))
        db_account = Account.objects.with_totals().get(pk=account.pk)
        self.assertEqual(db_account.balance, Decimal('-124500'))
        self.assertEqual(db_account.credit_sum, Decimal('500'))
        self.assertEqual(db_account.debit_sum, Decimal('-125000'))
        self.assertEqual(db_account.transactions.count(), 9)

    def test_create_account_for_apartment_simple(self):
        name = 'Account 1'
        user = SimpleUserFactory.create()
        account = AccountFactory.create_account_for_apartment(name, user, price=Decimal('275000.00'),
                                                              number_of_splits=1)
        db_account = Account.objects.with_totals().get(pk=account.pk)
        self.assertEqual(db_account.balance, Decimal('-275000'))
        self.assertEqual(db_account.debit_sum, Decimal('-275000'))
        self.assertEqual(db_account.credit_sum, Decimal('0.00'))
        self.assertEqual(db_account.transactions.count(), 2)
