from decimal import Decimal

from test_plus import TestCase

from .factories import AccountFactory
from ..models import Account
from ...users.tests.factories import SimpleUserFactory


class TestAccountFactory(TestCase):

    def test_create_account_for_apartment(self):
        name = 'Account 1'
        user = SimpleUserFactory.create()
        account = AccountFactory.create_account_for_apartment(name, user)
        db_account = Account.objects.with_totals().get(pk=account.pk)
        self.assertEqual(db_account.balance, Decimal('-124500'))
        self.assertEqual(db_account.credit_sum, Decimal('500'))
        self.assertEqual(db_account.debit_sum, Decimal('-125000'))
        self.assertEqual(db_account.transactions.count(), 9)

