from test_plus import TestCase

from ..faker import create_clients, create_broker
from ...real_estate.models import Client, Broker


class TestFaker(TestCase):

    def test_create_clients(self):
        clients = create_clients()
        self.assertEqual(len(clients), 6)
        for client in clients:
            self.assertIsNotNone(client['id'])
            self.assertEqual(client['created'], True)
        self.assertEqual(Client.objects.filter(client_type=Client.JURIDICAL_TYPE).count(), 1)
        self.assertEqual(Client.objects.filter(client_type=Client.NATURAL_TYPE).count(), 5)

    def test_create_broker(self):
        brokers = create_broker()
        self.assertEqual(len(brokers), 6)
        for broker in brokers:
            self.assertIsNotNone(broker['id'])
            self.assertEqual(broker['created'], True)
        self.assertEqual(Broker.objects.filter(broker_type=Broker.JURIDICAL_TYPE).count(), 1)
        self.assertEqual(Broker.objects.filter(broker_type=Broker.NATURAL_TYPE).count(), 5)

