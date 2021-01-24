from decimal import Decimal

from django.forms import model_to_dict
from test_plus import TestCase

from .factories import AccountFactory
from ..forms import AccountForm
from ..models import Account
from ..utils import get_or_create_transaction_types
from ...real_estate.tests.factories import RealEstateProjectFactory, ClientFactory, BrokerFactory, ContractFactory
from ...real_estate.utils import get_or_create_sales_types


class TestAccountForm(TestCase):
    @classmethod
    def setUpTestData(cls):

        get_or_create_sales_types()
        get_or_create_transaction_types()

        cls.project = RealEstateProjectFactory.create_with_spaces(6, 4,
                                                                  areas=[Decimal('100.00'), Decimal('100.00'),
                                                                         Decimal('75.00'), Decimal('75.00')])
        cls.user = cls.project.created_by
        cls.main_account = AccountFactory.create_account_for_apartment('Main account', cls.user)

        cls.contract_client = ClientFactory.create(created_by=cls.user)
        cls.broker = BrokerFactory.create(created_by=cls.user)
        real_estate_space = cls.project.real_estate_spaces.first()
        cls.contract = ContractFactory(project=real_estate_space.project,
                                       created_by=cls.user, broker=cls.broker)

    def test_clean(self):

        account = AccountFactory.create_account_for_apartment('Main account', self.user, price=Decimal('275000.00'),
                                                              number_of_splits=1)
        model_data = model_to_dict(account)
        model_data.pop('id')
        #model_data.pop('created_by')
        #model_data.pop('modified_by')
        form_data = dict()
        form_data['user'] = self.user
        form_data['data'] = AccountFactory.build_transaction_form_data(account)
        form_data['data'] = {**form_data['data'], **model_data}
        #form_data['data'] = model_data
        #form_data['data']['contract'] = self.contract

        account.delete()

        form = AccountForm(**form_data)
        form.full_clean()
        if form.is_valid():
            account = form.save()
        else:
            self.fail('Not valid')

        self.assertIsNotNone(account.id)
        self.assertEqual(account.transactions.count(), 2)
