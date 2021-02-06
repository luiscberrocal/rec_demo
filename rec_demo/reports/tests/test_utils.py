import os

from django.test import TestCase

from ..utils import generate_transaction_report
from ...banking.tests.factories import AccountFactory
from ...real_estate.tests.factories import ClientFactory, ContractFactory


class TestGenerateTransactionReport(TestCase):
    @classmethod
    def setUpTestData(cls):
        contract = ContractFactory.create()
        AccountFactory.create_account_for_apartment(f'Account {contract.id}', contract.created_by, contract=contract)

    def test_simple_write_local(self):
        filename = generate_transaction_report(location='LOCAL')
        self.assertTrue(os.path.exists(filename))

    def test_simple_write_s3(self):
        filename = generate_transaction_report(location='S3', expiration_time=3000)
        print(filename)


