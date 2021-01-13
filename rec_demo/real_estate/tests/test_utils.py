from test_plus import TestCase

from ..utils import get_or_create_sales_types


class Testget_or_create_sales_types(TestCase):

    def test_get_or_create_sales_types(self):
        sales_types = get_or_create_sales_types()
        self.assertEqual(len(sales_types), 3)
        for sales_type in sales_types:
            self.assertEqual(sales_type['created'], True)
