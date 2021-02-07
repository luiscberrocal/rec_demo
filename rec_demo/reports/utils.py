import os
import tempfile

import boto3
from django.conf import settings
from django.utils import timezone

from .exceptions import ReportsException
from ..banking.models import Transaction
from ..banking.resources import TransactionResource


class Reporter(object):

    def __init__(self, *args, **kwargs):
        self.add_timestamp = kwargs.get('add_timestamp', True)
        if hasattr(settings, 'S3_REPORT_EXPIRATION_TIME') and not kwargs.get('expiration_time'):
            self.expiration_time = settings.S3_REPORT_EXPIRATION_TIME
        else:
            self.expiration_time = kwargs.get('expiration_time', None)

        self.target_folder = kwargs.get('report_folder', 'reports')
        self.output_folder = kwargs.get('output_folder', 'report-output')

    def _upload_to_s3(self, source_filename, object_name, **kwargs):
        expiring_time = kwargs.get('expiration_time', self.expiration_time)
        target_folder = kwargs.get('report_folder', self.target_folder)
        object_name = f'{target_folder}/{object_name}'

        bucket = settings.AWS_STORAGE_BUCKET_NAME
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        s3_client = session.client('s3')
        s3_client.upload_file(source_filename, bucket, object_name)
        if expiring_time is None:
            raise ReportsException('No expiration time')
        else:
            url = s3_client.generate_presigned_url('get_object', Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                                         'Key': object_name}, ExpiresIn=expiring_time)
        return url

    def _get_report_filename(self, base_filename, **kwargs):
        output_folder = kwargs.get('output_folder', self.output_folder)
        file_path = settings.ROOT_DIR / output_folder
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        return os.path.join(file_path, base_filename)

    def _add_timestamp(self, filename, position='start'):
        timestamp = timezone.localtime().strftime('%Y%m%d_%H%M%S')
        file_parts = os.path.splitext(filename)
        if position == 'end':
            return f'{file_parts[0]}_{timestamp}{file_parts[1]}'
        elif position == 'start':
            return f'{timestamp}_{file_parts[0]}{file_parts[1]}'
        else:
            raise ReportsException('Unsupported position')

    def write_report(self, queryset, resource, location='S3', **kwargs):
        base_filename = kwargs.get('filename', 'transactions.xlsx')
        dataset = resource.export(queryset=queryset)
        if location == 'LOCAL':
            if self.add_timestamp:
                base_filename = self._add_timestamp(base_filename)
            filename = self._get_report_filename(base_filename=base_filename)
            with open(filename, 'wb') as excel_file:
                excel_file.write(dataset.xlsx)
            # self.clean_up(filename, model_name)
            return {'filename': filename}
        elif location == 'S3':
            if self.add_timestamp:
                object_name = self._add_timestamp(base_filename)
            else:
                object_name = base_filename
            with tempfile.NamedTemporaryFile() as temp:
                filename = temp.name + '.xlsx'
                with open(filename, 'wb') as excel_file:
                    excel_file.write(dataset.xlsx)
                # self.clean_up(filename, model_name)
                url = self._upload_to_s3(filename, object_name)
            return {'url': url, 's3_object_name': object_name}
        else:
            msg = f'{location} is not a supported location for writing reports'
            raise ReportsException(msg)


def generate_transaction_report(**kwargs):
    location = kwargs.get('location')
    expiration_time = kwargs.get('expiration_time', None)
    qs = Transaction.objects.all()  # TODO Add setting for max number of records in report
    resource = TransactionResource()

    reporter = Reporter(expiration_time=expiration_time)
    result = reporter.write_report(qs, resource, location=location)

    return result
