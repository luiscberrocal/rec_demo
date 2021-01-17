from decimal import Decimal

from django.forms.models import model_to_dict
from django.test import TestCase

from .factories import CompanyFactory, RealEstateProjectFactory, RealEstateSpaceFactory, ClientFactory, BrokerFactory, \
    ContractFactory, ContractClientFactory, ContractBrokerFactory
from ..models import Company, RealEstateProject, RealEstateSpace, Client, Broker, Contract, ContractClient, \
    ContractBroker
from ..utils import get_or_create_sales_types


class TestCaseCompany(TestCase):

    def test_create(self):
        """
        Test the creation of a Company model using a factory
        """
        company = CompanyFactory.create()
        self.assertEqual(Company.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Company models using a factory
        """
        companys = CompanyFactory.create_batch(5)
        self.assertEqual(Company.objects.count(), 5)
        self.assertEqual(len(companys), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of Company server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        company = CompanyFactory.create()
        company_dict = model_to_dict(company)
        self.assertEqual(len(company_dict.keys()), 7)

    def test_attribute_content(self):
        """
        Test that all attributes of Company server have content. This test will break if an attributes name is changed.
        """
        company = CompanyFactory.create()
        self.assertIsNotNone(company.id)
        self.assertIsNotNone(company.created)
        self.assertIsNotNone(company.modified)
        self.assertIsNotNone(company.created_by)
        self.assertIsNotNone(company.modified_by)
        self.assertIsNotNone(company.name)
        self.assertIsNotNone(company.short_name)
        self.assertIsNotNone(company.logo)


class TestCaseRealEstateProject(TestCase):

    def test_create(self):
        """
        Test the creation of a RealEstateProject model using a factory
        """
        real_estate_project = RealEstateProjectFactory.create_with_spaces(4, apartment_per_floor=2)
        self.assertEqual(RealEstateProject.objects.count(), 1)
        self.assertEqual(real_estate_project.real_estate_spaces.count(), 8)

    def test_create_batch(self):
        """
        Test the creation of 5 RealEstateProject models using a factory
        """
        real_estate_projects = RealEstateProjectFactory.create_batch(5)
        self.assertEqual(RealEstateProject.objects.count(), 5)
        self.assertEqual(len(real_estate_projects), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of RealEstateProject server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        real_estate_project = RealEstateProjectFactory.create()
        real_estate_project_dict = model_to_dict(real_estate_project)
        self.assertEqual(len(real_estate_project_dict.keys()), 8)

    def test_attribute_content(self):
        """
        Test that all attributes of RealEstateProject server have content. This test will break if an attributes name is changed.
        """
        real_estate_project = RealEstateProjectFactory.create()
        self.assertIsNotNone(real_estate_project.id)
        self.assertIsNotNone(real_estate_project.created)
        self.assertIsNotNone(real_estate_project.modified)
        self.assertIsNotNone(real_estate_project.created_by)
        self.assertIsNotNone(real_estate_project.modified_by)
        self.assertIsNotNone(real_estate_project.name)
        self.assertIsNotNone(real_estate_project.short_name)
        self.assertIsNotNone(real_estate_project.company)
        self.assertIsNotNone(real_estate_project.logo)


class TestCaseRealEstateSpace(TestCase):

    def test_create(self):
        """
        Test the creation of a RealEstateSpace model using a factory
        """
        real_estate_space = RealEstateSpaceFactory.create()
        self.assertEqual(RealEstateSpace.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 RealEstateSpace models using a factory
        """
        real_estate_spaces = RealEstateSpaceFactory.create_batch(5)
        self.assertEqual(RealEstateSpace.objects.count(), 5)
        self.assertEqual(len(real_estate_spaces), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of RealEstateSpace server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        real_estate_space = RealEstateSpaceFactory.create()
        real_estate_space_dict = model_to_dict(real_estate_space)
        self.assertEqual(len(real_estate_space_dict.keys()), 9)

    def test_attribute_content(self):
        """
        Test that all attributes of RealEstateSpace server have content. This test will break if an attributes name is changed.
        """
        real_estate_space = RealEstateSpaceFactory.create()
        self.assertIsNotNone(real_estate_space.id)
        self.assertIsNotNone(real_estate_space.created)
        self.assertIsNotNone(real_estate_space.modified)
        self.assertIsNotNone(real_estate_space.created_by)
        self.assertIsNotNone(real_estate_space.modified_by)
        self.assertIsNotNone(real_estate_space.project)
        self.assertIsNotNone(real_estate_space.name)
        self.assertIsNotNone(real_estate_space.space_type)
        self.assertIsNotNone(real_estate_space.area)
        self.assertIsNotNone(real_estate_space.price)
        self.assertIsNone(real_estate_space.contract)


class TestCaseClient(TestCase):

    def test_create(self):
        """
        Test the creation of a Client model using a factory
        """
        client = ClientFactory.create()
        self.assertEqual(Client.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Client models using a factory
        """
        clients = ClientFactory.create_batch(5)
        self.assertEqual(Client.objects.count(), 5)
        self.assertEqual(len(clients), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of Client server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        client = ClientFactory.create()
        client_dict = model_to_dict(client)
        self.assertEqual(len(client_dict.keys()), 14)

    def test_attribute_content(self):
        """
        Test that all attributes of Client server have content. This test will break if an attributes name is changed.
        """
        client = ClientFactory.create()
        self.assertIsNotNone(client.id)
        self.assertIsNotNone(client.created)
        self.assertIsNotNone(client.modified)
        self.assertIsNotNone(client.first_name)
        self.assertIsNone(client.middle_name)
        self.assertIsNotNone(client.last_name)
        self.assertIsNotNone(client.sex)
        self.assertIsNotNone(client.national_id)
        self.assertIsNotNone(client.national_id_type)
        self.assertIsNotNone(client.country_for_id)
        self.assertIsNotNone(client.picture)
        self.assertIsNotNone(client.date_of_birth)
        self.assertIsNotNone(client.created_by)
        self.assertIsNotNone(client.modified_by)
        self.assertIsNotNone(client.full_name)
        self.assertIsNotNone(client.client_type)


class TestCaseBroker(TestCase):

    def test_create(self):
        """
        Test the creation of a Broker model using a factory
        """
        broker = BrokerFactory.create()
        self.assertEqual(Broker.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Broker models using a factory
        """
        brokers = BrokerFactory.create_batch(5)
        self.assertEqual(Broker.objects.count(), 5)
        self.assertEqual(len(brokers), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of Broker server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        broker = BrokerFactory.create()
        broker_dict = model_to_dict(broker)
        self.assertEqual(len(broker_dict.keys()), 14)

    def test_attribute_content(self):
        """
        Test that all attributes of Broker server have content. This test will break if an attributes name is changed.
        """
        broker = BrokerFactory.create()
        self.assertIsNotNone(broker.id)
        self.assertIsNotNone(broker.created)
        self.assertIsNotNone(broker.modified)
        self.assertIsNotNone(broker.first_name)
        self.assertIsNone(broker.middle_name)
        self.assertIsNotNone(broker.last_name)
        self.assertIsNotNone(broker.sex)
        self.assertIsNotNone(broker.national_id)
        self.assertIsNotNone(broker.national_id_type)
        self.assertIsNotNone(broker.country_for_id)
        self.assertIsNotNone(broker.picture)
        self.assertIsNotNone(broker.date_of_birth)
        self.assertIsNotNone(broker.created_by)
        self.assertIsNotNone(broker.modified_by)
        self.assertIsNotNone(broker.full_name)
        self.assertIsNotNone(broker.broker_type)


class TestCaseContract(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_or_create_sales_types()

        cls.project = RealEstateProjectFactory.create_with_spaces(6, 4,
                                                                  areas=[Decimal('100.00'), Decimal('100.00'),
                                                                         Decimal('75.00'), Decimal('75.00')])
        cls.user = cls.project.created_by
        cls.contract_client = ClientFactory.create(created_by=cls.user)
        cls.broker = BrokerFactory.create(created_by=cls.user)


    def test_create(self):
        """
        Test the creation of a Contract model using a factory
        """
        contract = ContractFactory.create()
        self.assertEqual(Contract.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Contract models using a factory
        """
        contracts = ContractFactory.create_batch(5)
        self.assertEqual(Contract.objects.count(), 5)
        self.assertEqual(len(contracts), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of Contract server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        contract = ContractFactory.create()
        contract_dict = model_to_dict(contract)
        self.assertEqual(len(contract_dict.keys()), 10)

    def test_attribute_content(self):
        """
        Test that all attributes of Contract server have content. This test will break if an attributes name is changed.
        """
        contract = ContractFactory.create()
        self.assertIsNotNone(contract.id)
        self.assertIsNotNone(contract.created)
        self.assertIsNotNone(contract.modified)
        self.assertIsNotNone(contract.created_by)
        self.assertIsNotNone(contract.modified_by)
        self.assertIsNotNone(contract.date)
        self.assertIsNotNone(contract.project)

    def test_create_with_account(self):
        real_estate_space = self.project.real_estate_spaces.first()
        contract = ContractFactory(project=real_estate_space.project,
                                   created_by=self.user, broker=self.broker)
        self.assertEqual(Contract.objects.count(), 1)
        contract.add_space(real_estate_space)
        contract.add_client(self.contract_client)
        self.assertEqual(contract.real_estate_spaces.count(), 1)
        self.assertEqual(contract.contract_clients.count(), 1)




class TestCaseContractClient(TestCase):

    def test_create(self):
        """
        Test the creation of a ContractClient model using a factory
        """
        contract_client = ContractClientFactory.create()
        self.assertEqual(ContractClient.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 ContractClient models using a factory
        """
        contract_clients = ContractClientFactory.create_batch(5)
        self.assertEqual(ContractClient.objects.count(), 5)
        self.assertEqual(len(contract_clients), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of ContractClient server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        contract_client = ContractClientFactory.create()
        contract_client_dict = model_to_dict(contract_client)
        self.assertEqual(len(contract_client_dict.keys()), 6)

    def test_attribute_content(self):
        """
        Test that all attributes of ContractClient server have content. This test will break if an attributes name is changed.
        """
        contract_client = ContractClientFactory.create()
        self.assertIsNotNone(contract_client.id)
        self.assertIsNotNone(contract_client.created)
        self.assertIsNotNone(contract_client.modified)
        self.assertIsNotNone(contract_client.created_by)
        self.assertIsNotNone(contract_client.modified_by)
        self.assertIsNotNone(contract_client.client)
        self.assertIsNotNone(contract_client.contract)
        self.assertIsNotNone(contract_client.is_principal)


class TestCaseContractBroker(TestCase):

    def test_create(self):
        """
        Test the creation of a ContractBroker model using a factory
        """
        contract_broker = ContractBrokerFactory.create()
        self.assertEqual(ContractBroker.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 ContractBroker models using a factory
        """
        contract_brokers = ContractBrokerFactory.create_batch(5)
        self.assertEqual(ContractBroker.objects.count(), 5)
        self.assertEqual(len(contract_brokers), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of ContractBroker server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        contract_broker = ContractBrokerFactory.create()
        contract_broker_dict = model_to_dict(contract_broker)
        self.assertEqual(len(contract_broker_dict.keys()), 6)

    def test_attribute_content(self):
        """
        Test that all attributes of ContractBroker server have content. This test will break if an attributes name is changed.
        """
        contract_broker = ContractBrokerFactory.create()
        self.assertIsNotNone(contract_broker.id)
        self.assertIsNotNone(contract_broker.created)
        self.assertIsNotNone(contract_broker.modified)
        self.assertIsNotNone(contract_broker.created_by)
        self.assertIsNotNone(contract_broker.modified_by)
        self.assertIsNotNone(contract_broker.broker)
        self.assertIsNotNone(contract_broker.contract)
        self.assertIsNotNone(contract_broker.is_active)
