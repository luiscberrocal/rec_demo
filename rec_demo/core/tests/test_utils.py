from time import sleep

import boto3
from django.conf import settings
from django.test import SimpleTestCase

from rec_demo.core.utils import file_exists_on_s3


class TestFileExistsOnS3(SimpleTestCase):
    def setUp(self) -> None:
        # logger.debug(f'Use S3: {settings.USE_S3}')
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.s3_client = session.client('s3')

    def test_file_exists_on_s3_true(self):
        source_filename = '../../requirements/base.txt'
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        object_name = 'base_req_test_file_exists_on_s3_true.txt'
        self.s3_client.upload_file(source_filename, bucket, object_name)
        sleep(2)
        result = file_exists_on_s3(object_name, bucket, s3_client=self.s3_client)
        self.assertTrue(result)
        self.s3_client.delete_object(Bucket=bucket, Key=object_name)
        result = file_exists_on_s3(object_name, bucket, s3_client=self.s3_client)
        sleep(2)
        self.assertFalse(result)
