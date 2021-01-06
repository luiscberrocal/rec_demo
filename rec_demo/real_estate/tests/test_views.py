#//contract=lowercaseAndDash(MODEL)
#//contract=snakeCase(MODEL)
from test_plus import TestCase

from .factories import ContractFactory
from ..models import Contract
from ...core.utils import model_to_json_dict
from ...users.tests.factories import SimpleUserFactory


class TestContractCreateView(TestCase):

    def setUp(self) -> None:
        self.app_user = SimpleUserFactory.create()

    def test_post(self):
        contract = ContractFactory.create(created_by=self.app_user)
        contract_dict = model_to_json_dict(contract)
        contract_dict.pop('id')
        contract.delete()

        with self.login(self.app_user):
            response = self.post('real_estate:create-contract', data=contract_dict)
            self.response_302(response)

        self.assertEqual(Contract.objects.count(), 1)

    def test_get(self):
        contract = ContractFactory.create(created_by=self.app_user)
        contract.delete()

        with self.login(self.app_user):
            response = self.get('real_estate:create-contract')
            self.response_200(response)


class TestContractUpdateView(TestCase):

    def setUp(self) -> None:
        self.app_user = SimpleUserFactory.create()

    def test_get(self):
        contract = ContractFactory.create(created_by=self.app_user)

        with self.login(self.app_user):
            response = self.post('real_estate:update-contract', pk=contract.pk)
            self.response_200(response)

    # def test_post_update_attribute(self):
    #     contract = ContractFactory.create(created_by=self.app_user)
    #
    #     contract_dict = model_to_dict(contract)
    #     contract_dict['attribute'] = att_value $FIXME
    #
    #     with self.login(self.app_user):
    #         response = self.post('real_estate:update-contract', pk=contract.pk, data=contract_dict)
    #         self.response_302(response)
    #
    #     self.assertEqual(Contract.objects.count(), 1)
    #
    #     db_contract = Contract.objects.get(id=contract.id)
    #     self.assertEqual(db_contract.attribute, contract_dict['attribute'])
