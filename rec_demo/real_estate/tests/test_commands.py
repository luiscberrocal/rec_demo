from django.core.management import call_command
from django_test_tools.mixins import TestCommandMixin
from test_plus import TestCase

from ..models import RealEstateSpace, RealEstateProject


class TestCreateFakeCommand(TestCommandMixin, TestCase):

    def test_create(self):
        call_command('create_fake', stdout=self.content, stderr=self.error_content)
        results = self.get_results()
        self.assertEqual(RealEstateProject.objects.count(), 6)
        self.assertEqual(RealEstateSpace.objects.filter(space_type=RealEstateSpace.LIVING_SPACE).count(), 214)
        self.assertEqual(RealEstateSpace.objects.filter(project__name='PH Rossini',
                                                        space_type=RealEstateSpace.LIVING_SPACE).count(), 60)
        self.assertEqual(RealEstateSpace.objects.filter(space_type=RealEstateSpace.STORAGE_SPACE).count(), 25)
        self.assertEqual(RealEstateSpace.objects.filter(space_type=RealEstateSpace.PARKING_SPACE).count(), 35)
        self.assertEqual(len(results), 7)
