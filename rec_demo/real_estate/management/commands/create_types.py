from django.core.management.base import BaseCommand

from ...utils import get_or_create_sales_types
from ....banking.utils import get_or_create_transaction_types


class Command(BaseCommand):
    help = "Create types data."

    def add_arguments(self, parser):
        pass
        # parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        results = get_or_create_sales_types()
        self.stdout.write('--- Sales Types ---')
        for result in results:
            self.stdout.write(f'Created {result["created"]} {result["name"]}')

        self.stdout.write('--- Transaction Types ---')
        transaction_types = get_or_create_transaction_types()
        for transaction_type in transaction_types:
            self.stdout.write(f'Created: {transaction_type["created"]} {transaction_type["name"]}')
