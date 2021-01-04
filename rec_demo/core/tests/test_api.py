from django.urls import reverse
from rest_framework.test import APIClient
from test_plus import TestCase


class TestCoreAPI(TestCase):

    def test_app_data(self):
        url = reverse('app_data')
        client = APIClient()
        response = client.get(url)
        app_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertRegex(app_data.get('version'), r'\d+\.\d+\.\d+')
        self.assertEqual(app_data['name'], 'REC Demo')
        self.assertEqual(app_data['copyright'], '2021 (c) EMR Consultants')
        self.assertEqual(len(app_data.keys()), 3)

