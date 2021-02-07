import os

import requests
from django.test import TestCase
from django_test_tools.file_utils import temporary_file

from ..utils import generate_transaction_report
from ...banking.tests.factories import AccountFactory
from ...real_estate.tests.factories import ClientFactory, ContractFactory


class TestGenerateTransactionReport(TestCase):
    @classmethod
    def setUpTestData(cls):
        contract = ContractFactory.create()
        AccountFactory.create_account_for_apartment(f'Account {contract.id}', contract.created_by, contract=contract)

    def test_simple_write_local(self):
        result = generate_transaction_report(location='LOCAL')
        self.assertTrue(os.path.exists(result['filename']))

    @temporary_file('xlsx', delete_on_exit=True)
    def test_simple_write_s3(self):
        filename = self.test_simple_write_s3.filename
        result = generate_transaction_report(location='S3', expiration_time=3000)
        r = requests.get(result['url'])

        with open(filename, 'wb') as f:
            f.write(r.content)
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(r.status_code, 200)


