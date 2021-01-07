# //contract=lowercaseAndDash(MODEL)
# //contract=snakeCase(MODEL)
from test_plus import TestCase

from .factories import ContractFactory, ClientFactory
from ..forms import ContractForm
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
        clients = ClientFactory.create_batch(3)
        i = 0
        for client in clients:
            client_field = ContractForm.CLIENT_PATTERN.format(i)
            is_principal_field = ContractForm.IS_PRINCIPAL_PATTERN.format(i)
            contract_dict[client_field] = client.id
            if i == 0:
                contract_dict[is_principal_field] = 'on'
            i += 1

        with self.login(self.app_user):
            response = self.post('real_estate:create-contract', data=contract_dict)
            self.response_302(response)

        self.assertEqual(Contract.objects.count(), 1)
        contract = Contract.objects.first()
        self.assertEqual(contract.contract_clients.filter(is_principal=True).count(), 1)
        self.assertEqual(contract.contract_clients.count(), 3)

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
