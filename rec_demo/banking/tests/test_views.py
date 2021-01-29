from decimal import Decimal

from django.forms import model_to_dict
from test_plus import TestCase

from .factories import AccountFactory
from ..models import Account
from ..utils import get_or_create_transaction_types
from ...core.utils import clean_dict
from ...real_estate.tests.factories import RealEstateProjectFactory, ClientFactory, BrokerFactory, ContractFactory
from ...real_estate.utils import get_or_create_sales_types
from ...users.tests.factories import SimpleUserFactory


class TestAccountCreateView(TestCase):

    @classmethod
    def setUpTestData(cls):
        get_or_create_sales_types()
        get_or_create_transaction_types()
        cls.user = SimpleUserFactory.create()
        cls.project = RealEstateProjectFactory.create_with_spaces(6, 4, created_by=cls.user,
                                                                  areas=[Decimal('100.00'), Decimal('100.00'),
                                                                         Decimal('75.00'), Decimal('75.00')])

        cls.main_account = AccountFactory.create_account_for_apartment('Main account', cls.user)

        cls.contract_client = ClientFactory.create(created_by=cls.user)
        cls.broker = BrokerFactory.create(created_by=cls.user)
        real_estate_space = cls.project.real_estate_spaces.first()
        cls.contract = ContractFactory(project=real_estate_space.project,
                                       created_by=cls.user, broker=cls.broker)

    def test_clean(self):
        account = AccountFactory.create_account_for_apartment('Main account 2', self.user, price=Decimal('275000.00'),
                                                              number_of_splits=1)
        model_data = model_to_dict(account)
        model_data.pop('id')
        # model_data.pop('created_by')
        # model_data.pop('modified_by')
        form_data = dict()
        form_data['user'] = self.user
        form_data['data'] = AccountFactory.build_transaction_form_data(account)
        form_data['data'] = {**form_data['data'], **model_data}
        # form_data['data'] = model_data
        form_data['data']['contract'] = self.contract.id

        account.delete()

    def test_get_create_account(self):
        with self.login(self.user):
            response = self.get('banking:create-account')
            self.response_200(response)

    def test_create_account(self):
        account = AccountFactory.create_account_for_apartment('Main Account Create', self.user,
                                                              price=Decimal('275000.00'),
                                                              number_of_splits=1)
        account_dict = model_to_dict(account)
        account_dict= clean_dict(account_dict, clean_for='all')
        account_dict.pop('id')

        transaction_data = AccountFactory.build_transaction_form_data(account, clean_for='all')
        account.delete()
        account_dict = {**account_dict, **transaction_data}
        # form_data['data'] = model_data
        account_dict['contract'] = self.contract.id
        with self.login(self.user):
            response = self.post('banking:create-account', data=account_dict)
            self.response_302(response)
        self.assertEqual(Account.objects.filter(name='Main Account Create').count(), 1)
