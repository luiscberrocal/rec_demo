from django.core.management.base import BaseCommand

from ...models import RealEstateProject, Company
from ...tests.factories import RealEstateProjectFactory, CompanyFactory
from ...utils import get_or_create_sales_types
from ....users.models import User


class Command(BaseCommand):
    help = "Create fake data."

    def add_arguments(self, parser):
        pass
        # parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        results = get_or_create_sales_types()
        self.stdout.write('--- Sales Types ---')
        for result in results:
            self.stdout.write(f'Created {result["created"]} {result["name"]}')