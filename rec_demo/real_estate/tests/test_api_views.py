from test_plus import TestCase

from .factories import RealEstateProjectFactory
from ...users.tests.factories import SimpleUserFactory


class TestRealEstateSpaceListAPIView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.app_user = SimpleUserFactory.create()
        cls.project = RealEstateProjectFactory.create_with_spaces(4, created_by=cls.app_user)

    def test_get(self):
        with self.login(self.app_user):
            response = self.get('real_estate_api:list-real-estate-space')
            self.response_200(response)
            results = response.data
            self.assertEqual(len(results), 16)

    def test_get_filtered(self):
        with self.login(self.app_user):
            project = RealEstateProjectFactory.create_with_spaces(2, apartment_per_floor=3,
                                                                  created_by=self.app_user, name='PH La Suerte')
            response = self.get('real_estate_api:list-real-estate-space-by-project', project_id=project.id) #data={'project_id': project.id})
            self.response_200(response)
            results = response.data
            self.assertEqual(len(results), 6)

    def test_get_no_login(self):
        response = self.get('real_estate_api:list-real-estate-space')
        self.response_403(response)

# class TestRealEstateSpaceDetailAPIView(JWTTestMixin, TestCase):
#
#     def test_get(self):
#         real-estate-space = RealEstateSpaceFactory.create()
#
#         url = reverse('real_estate:detail-real-estate-space', kwargs={'pk': real-estate-space.pk})
#         user = SimpleUserFactory.create()
#
#         response = self.get_with_token(url, user)
#
#         self.response_200(response)
#         real-estate-space_data = response.data
#
#         write_assertions(real-estate-space_data, 'real-estate-space_data', type_only=True)
#
#     def test_get_invalid_pk(self):
#         url = reverse('real_estate:detail-real-estate-space', kwargs={'pk': 1000000})
#         user = SimpleUserFactory.create()
#
#         response = self.get_with_token(url, user)
#
#         self.response_404(response)
#         real-estate-space_invalid_data = response.data
#
#         write_assertions(real-estate-space_invalid_data, 'real-estate-space_invalid_data', type_only=False)
#
#     def test_put(self):
#         real-estate-space = RealEstateSpaceFactory.create()
#
#         url = reverse('real_estate:update-real-estate-space', kwargs={'pk': real-estate-space.pk})
#         user = SimpleUserFactory.create()
#         real-estate-space_data = model_to_dict(real-estate-space)
#         real-estate-space_data[''] = 'VERY_NEW_VALUE' #FIXME Change something
#         response = self.put_with_token(url, user, data=real-estate-space_data)
#
#         self.response_200(response)
#         real-estate-space_put_data = response.data
#
#         write_assertions(real-estate-space_put_data, 'real-estate-space_put_data', type_only=True)
#
#         self.assertEqual(real-estate-space_put_data[''], 'VERY_NEW_VALUE') #FIXME Compare the data that changed
#
#     def test_delete(self):
#         real-estate-space = RealEstateSpaceFactory.create()
#
#         url = reverse('real_estate:delete-real-estate-space', kwargs={'pk': real-estate-space.pk})
#         user = SimpleUserFactory.create()
#
#         response = self.delete_with_token(url, user)
#
#         self.response_204(response)
#
#         self.assertEqual(RealEstateSpace.objects.count(), 0)
#
# class TestRealEstateSpaceCreateAPIView(JWTTestMixin, TestCase):
#
#     def test_post(self):
#         real-estate-space = RealEstateSpaceFactory.create()
#
#         real-estate-space_dict = model_to_dict(real-estate-space)
#         real-estate-space.delete()
#         real-estate-space_dict.pop('id')
#
#         url = reverse('real_estate:create-real-estate-space')
#
#         user = SimpleUserFactory.create()
#
#         response = self.post_with_token(url, user, data=real-estate-space_dict)
#
#         self.response_201(response)
#         real-estate-space_post_data = response.data
#
#         self.assertEqual(RealEstateSpace.objects.count(), 1)
#         write_assertions(real-estate-space_post_data, 'real-estate-space_post_data', type_only=True)
