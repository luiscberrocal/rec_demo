# from django.conf import settings
# from django.test import SimpleTestCase, TestCase
#
#
# class TestSettings(SimpleTestCase):
#
#     def test_read_settings(self):
#         #self.assertEqual(settings.DJANGO_SETTINGS_MODULE, '')
#         self.assertEqual(settings.TEST_RUNNER, 'alpha_clinic.core.tests.runner.EMRDiscoverRunner')
#         self.assertEqual(settings.ENVIRONMENT_NAME, 'TEST')
#         self.assertEqual(settings.USE_S3, True)
#         if settings.USE_S3:
#             self.assertEqual(settings.MEDIA_URL, 'https://emr-practice-staging-bucket.s3.amazonaws.com/media/')
#         else:
#             self.assertEqual(settings.MEDIA_URL, '/media/')
#
#
#
