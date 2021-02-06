from django.core.management.base import BaseCommand
from slugify import slugify

from ...models import RealEstateProject, Company
from ...utils import create_spaces
from ....users.models import User


class Command(BaseCommand):
    help = "Create fake data."

    def add_arguments(self, parser):
        pass
        # parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        reset_projects = options.get('reset_projects', True)
        reset_company = options.get('reset_company', False)
        current_user = User.objects.first()
        company = self._create_company(current_user, reset_company)
        project_data = dict()
        project_data['Rossini'] = {'name': 'PH Rossini', 'floors': 15,
                                   'areas': ['105', '105', '95', '95'],
                                   'created_by': current_user,
                                   'company': company,
                                   'parkings': 10,
                                   'storage': 5}
        project_data['Carla'] = {'name': 'PH Carla', 'floors': 10,
                                 'areas': ['60', '60', '75'],
                                 'created_by': current_user,
                                 'company': company,
                                 'parkings': 5,
                                 'storage': 0}
        project_data['Tania'] = {'name': 'PH Tania', 'floors': 50,
                                 'areas': ['420', '420', ],
                                 'created_by': current_user,
                                 'company': company,
                                 'parkings': 20,
                                 'storage': 20}

        project_data['Eduardo'] = {'name': 'PH Eduardo', 'floors': 4,
                                   'areas': ['66', '66', ],
                                   'created_by': current_user,
                                   'company': company,
                                   'parkings': 0,
                                   'storage': 0}

        project_data['Ariadna'] = {'name': 'PH Ariadna', 'floors': 4,
                                   'areas': ['76', '76', ],
                                   'created_by': current_user,
                                   'company': company,
                                   'parkings': 0,
                                   'storage': 0}
        project_data['Kenia'] = {'name': 'PH Kenia', 'floors': 4,
                                 'areas': ['76', '76', ],
                                 'created_by': current_user,
                                 'company': company,
                                 'parkings': 0,
                                 'storage': 0}

        for name in project_data.keys():
            floors = project_data[name].pop('floors')
            create = False
            try:
                project = RealEstateProject.objects.get(name=project_data[name]['name'])
                if reset_projects:
                    project.delete()
                    create = True
            except RealEstateProject.DoesNotExist:
                create = True
            if create:
                project = RealEstateProject.objects.create(name=project_data[name]['name'],
                                                           short_name= slugify(project_data[name]['name']),
                                                           company=company)
                create_spaces(project, floors, **project_data[name])
                self.stdout.write(f'Project {project}: {project.real_estate_spaces.count()}')

    def _create_company(self, current_user, reset_company):
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
            company = Company.objects.create(name=company_name, created_by=current_user)
            self.stdout.write(f'Created {company.name} ({company.id})')
        return company
