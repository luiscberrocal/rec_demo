from django.test import TestCase

from ..utils import generate_transaction_report
from ...banking.tests.factories import AccountFactory
from ...real_estate.tests.factories import ClientFactory, ContractFactory


class TestGenerateTransactionReport(TestCase):

    def test_simple_write(self):
        contract = ContractFactory.create()
        AccountFactory.create_account_for_apartment(f'Account {contract.id}', contract.created_by, contract=contract)
        filename = generate_transaction_report(location='LOCAL')
        print(filename)

