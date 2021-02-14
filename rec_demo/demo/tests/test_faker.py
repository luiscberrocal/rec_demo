from test_plus import TestCase

from ..faker import create_clients, create_broker, create_companies
from ...real_estate.models import Client, Broker, Company
from ...users.tests.factories import SimpleUserFactory


class TestFaker(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = SimpleUserFactory.create()

    def test_create_clients(self):
        clients = create_clients()
        self.assertEqual(len(clients), 6)
        for client in clients:
            self.assertIsNotNone(client['id'])
            self.assertEqual(client['created'], True)
        self.assertEqual(Client.objects.filter(client_type=Client.JURIDICAL_TYPE).count(), 1)
        self.assertEqual(Client.objects.filter(client_type=Client.NATURAL_TYPE).count(), 5)
        self.assertEqual(Client.objects.filter(created_by__isnull=True).count(), 0)

    def test_create_broker(self):
        brokers = create_broker()
        self.assertEqual(len(brokers), 6)
        for broker in brokers:
            self.assertIsNotNone(broker['id'])
            self.assertEqual(broker['created'], True)
        self.assertEqual(Broker.objects.filter(broker_type=Broker.JURIDICAL_TYPE).count(), 1)
        self.assertEqual(Broker.objects.filter(broker_type=Broker.NATURAL_TYPE).count(), 5)
        self.assertEqual(Broker.objects.filter(created_by__isnull=True).count(), 0)

    def test_create_broker_with_delete(self):
        create_broker()
        self.assertEqual(Broker.objects.count(), 6)
        brokers = create_broker(delete=True)
        self.assertEqual(len(brokers), 6)
        for broker in brokers:
            self.assertIsNotNone(broker['id'])
            self.assertEqual(broker['created'], True)
        self.assertEqual(Broker.objects.filter(broker_type=Broker.JURIDICAL_TYPE).count(), 1)
        self.assertEqual(Broker.objects.filter(broker_type=Broker.NATURAL_TYPE).count(), 5)
        self.assertEqual(Broker.objects.filter(created_by__isnull=True).count(), 0)

    def test_create_companies(self):
        companies = create_companies()
        self.assertEqual(len(companies), 4)
        for broker in companies:
            self.assertIsNotNone(broker['id'])
            self.assertEqual(broker['created'], True)
        self.assertEqual(Company.objects.count(), 4)
