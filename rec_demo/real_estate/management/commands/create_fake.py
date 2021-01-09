from django.core.management.base import BaseCommand

from ...models import RealEstateProject, Company
from ...tests.factories import RealEstateProjectFactory, CompanyFactory
from ....users.models import User


class Command(BaseCommand):
    help = "Create fake data."

    def add_arguments(self, parser):
        pass
        # parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        reset_projects = options.get('reset_projects', True)
        reset_company = options.get('reset_company', False)

        names = ['Rossini', 'Carla', 'Tania', 'Eduardo', 'Ariadna', 'Kenia']
        current_user = User.objects.first()

        create_company = False
        company_name = 'Mandalorian Investments'
        try:
            company = Company.objects.get(name=company_name)
            if reset_company:
                company_name.delete()
                create_company = True
        except Company.DoesNotExist:
            create_company = True

        if create_company:
            company = CompanyFactory.create(name=company_name, created_by=current_user)
            self.stdout.write(f'Created {company.name} ({company.id})')

        for name in names:
            project_name = f'PH {name}'
            create = False
            try:
                project = RealEstateProject.objects.get(name=project_name)
                if reset_projects:
                    project.delete()
                    create = True
            except RealEstateProject.DoesNotExist:
                create = True
            if create:
                project = RealEstateProjectFactory.create_with_spaces(10, apartment_per_floor=4, company=company,
                                                                      created_by=current_user, name=project_name)
                self.stdout.write(f'Project {project}: {project.real_estate_spaces.count()}')
