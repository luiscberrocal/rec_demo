from datetime import date

from test_plus import TestCase

from ..models import Account, TransactionType
from ..utils import get_or_create_transaction_types
from ...users.tests.factories import SimpleUserFactory


class TransactionListAPIViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.app_user = SimpleUserFactory.create()
        get_or_create_transaction_types()

        down = TransactionType.objects.get(short_name='DOWN')
        loan = TransactionType.objects.get(short_name='LOAN')
        cls.account = Account.objects.create(name='New account')
        cls.account.add_debit('125,000.00', loan)
        start_month = 1
        for i in range(5):
            cls.account.add_debit('1500', down, due_date=date(2021, start_month, 1))
            start_month += 1

        cls.account2 = Account.objects.create(name='New account2')
        cls.account2.add_debit('245,000.00', loan)
        start_month = 1
        for i in range(6):
            cls.account2.add_debit('4500', down, due_date=date(2021, start_month, 1))
            start_month += 1

    def test_list_transaction(self):
        with self.login(self.app_user):
            response = self.get('banking_api:list-transaction')
            self.response_200(response)
            results = response.data
            self.assertEqual(len(results), 13)
