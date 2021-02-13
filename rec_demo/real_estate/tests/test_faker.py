from test_plus import TestCase

from ..faker import create_clients
from  ..models import Client


class TestFaker(TestCase):

    def test_create_clients(self):
        clients = create_clients()
        self.assertEqual(len(clients), 6)
        for client in clients:
            self.assertIsNotNone(client['id'])
            self.assertEqual(client['created'], True)
        self.assertEqual(Client.objects.filter(client_type=Client.JURIDICAL_TYPE).count(), 1)
        self.assertEqual(Client.objects.filter(client_type=Client.NATURAL_TYPE).count(), 5)
