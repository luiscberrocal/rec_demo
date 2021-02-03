from django.test import TestCase

from ..utils import generate_client_report
from ...real_estate.tests.factories import ClientFactory


class TestGenerateClientReport(TestCase):

    def test_simple_write(self):
        ClientFactory.create_batch(5)
        filename = generate_client_report()

