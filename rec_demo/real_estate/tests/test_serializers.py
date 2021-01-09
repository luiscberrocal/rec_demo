from django.forms import model_to_dict
from test_plus import TestCase

from ..api.serializers import RealEstateSpaceSerializer
from .factories import RealEstateSpaceFactory, RealEstateProjectFactory
from ..models import RealEstateSpace
from ...users.tests.factories import SimpleUserFactory


class TestRealEstateSpaceSerializer(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.app_user = SimpleUserFactory.create()
        cls.project = RealEstateProjectFactory.create_with_spaces(4, created_by=cls.app_user)

    def test_expected_fields(self):
        """
        This test verifies what fields are expected when serializing a RealEstateSpace
        using a RealEstateSpaceSerializer.
        """
        real_estate_space = RealEstateSpace.objects.first()
        serializer = RealEstateSpaceSerializer(instance=real_estate_space)
        real_estate_space_data = serializer.data
        real_estate_space_data_keys = ['id', 'project', 'name', 'space_type', 'area', 'price', 'contract', 'created',
                                       'modified', 'created_by', 'modified_by', ]
        self.assertEqual(set(real_estate_space_data.keys()), set(real_estate_space_data_keys))

    # def test_creation(self):
    #     """
    #     This test verifies that the serializer can create a RealEstateSpace in the database.
    #     """
    #     # Create a RealEstateSpace object to serialize
    #     real_estate_space = RealEstateSpaceFactory.create()
    #
    #     # Convert the model to dictionary
    #     real_estate_space_dict = model_to_dict(real_estate_space)
    #     # Delete the object from the database
    #     real_estate_space.delete()
    #     # Eliminate the primary key (id) from the dictionary
    #     real_estate_space_dict.pop('id')
    #
    #     serializer = RealEstateSpaceSerializer(data=real_estate_space_dict)
    #     self.assertTrue(serializer.is_valid())
    #     serializer.save()
    #     self.assertEqual(RealEstateSpace.objects.count(), 1)

    # def test_update_name(self):
    #     real_estate_space = RealEstateSpaceFactory.create(name='OLD NAME')
    #
    #     real_estate_space_dict = model_to_dict(real_estate_space)
    #
    #     real_estate_space_dict['name'] = 'NEW NAME'
    #
    #     serializer = RealEstateSpaceSerializer(data=real_estate_space_dict, instance=real_estate_space)
    #     self.assertTrue(serializer.is_valid())
    #     serializer.save()
    #     self.assertEqual(RealEstateSpace.objects.filter(name='NEW NAME').count(), 1)
    #
    # def test_serialize_many(self):
    #     RealEstateSpaceFactory.create_batch(10)
    #     real_estate_spaces = RealEstateSpace.objects.all()
    #     serializer = RealEstateSpaceSerializer(real_estate_spaces, many=True)
    #
    #     real_estate_space_data_many = serializer.data
    #
    #     # write_assertions(real_estate_space_data_many, 'real_estate_space_data_many', type_only=True)
    #     self.fail('Not implemented')