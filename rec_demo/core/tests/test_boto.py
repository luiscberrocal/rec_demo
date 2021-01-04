# import logging
# import os
# import tempfile
#
# import boto3
# from botocore import errorfactory
# from django.conf import settings
# from django.test import SimpleTestCase
# from django_test_tools.file_utils import temporary_file, hash_file
#
# logger = logging.getLogger(__name__)
#
#
# class TestBotoUpload(SimpleTestCase):
#
#     def setUp(self) -> None:
#         logger.debug(f'environment: {settings.ENVIRONMENT_NAME}')
#         logger.debug(f'Use S3: {settings.USE_S3}')
#         session = boto3.Session(
#             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#         )
#         self.s3_client = session.client('s3')
#
#     @temporary_file('.txt', delete_on_exit=True)
#     def test_upload(self):
#         source_filename = '../../requirements/base.txt'
#         source_hash = hash_file(source_filename)
#         bucket = settings.AWS_STORAGE_BUCKET_NAME
#         object_name = 'base_req.txt'
#         output_filename = self.test_upload.filename
#
#         self.s3_client.upload_file(source_filename, bucket, object_name)
#
#         self.s3_client.download_file(bucket, object_name, output_filename)
#
#         output_hash = hash_file(output_filename)
#         res = self.s3_client.get_object_acl( Bucket=bucket,Key=object_name)
#         print(res)
#         self.s3_client.delete_object(Bucket=bucket, Key=object_name)
#         self.assertEqual(output_hash, source_hash)
#         self.assertTrue(os.path.exists(output_filename))
#         try:
#             self.s3_client.get_object_acl(Bucket=bucket, Key=object_name )
#             self.fail('Should have raised a NoSuchKey exception')
#         except Exception:
#             pass
#         print(res)
#
#     def test_upload_new_file(self):
#         object_name = 'test_upload_new_file.txt'
#         bucket = settings.AWS_STORAGE_BUCKET_NAME
#         expiring_time = 600
#
#         with tempfile.NamedTemporaryFile() as temp:
#             source_filename = temp.name + '.txt'
#             with open(source_filename, 'w') as txt_file:
#                 txt_file.write('Hello world')
#
#             self.s3_client.upload_file(source_filename, bucket, object_name)
#             url = self.s3_client.generate_presigned_url('get_object',
#                                                         Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
#                                                                 'Key': object_name}, ExpiresIn=expiring_time)
#             # print(f'URL: {url}')
#         self.assertTrue('https://emr-practice-staging-bucket.s3.amazonaws.com/test_upload_new_file.txt' in url)
#         self.s3_client.delete_object(Bucket=bucket, Key=object_name)
