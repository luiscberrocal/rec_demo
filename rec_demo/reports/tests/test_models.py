from time import sleep

from test_plus import TestCase

from ..models import Report
from ..utils import generate_transaction_report
from ...core.utils import file_exists_on_s3
from ...users.tests.factories import SimpleUserFactory


class TestReport(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = SimpleUserFactory.create()
        report_config = {'location': 'S3', 'expiration_time': 3000,
                         'base_filename': 'test_transactions.xlsx'}  ###TODO Set in settings
        result = generate_transaction_report(**report_config)
        task_id = '99999'
        report_data = dict()
        report_data['name'] = 'TEST'
        report_data['task_id'] = task_id
        report_data['metadata'] = {'config': report_config, 'task_result': result}
        report_data['created_by'] = user
        report_data['modified_by'] = None

        cls.report = Report.objects.create(**report_data)

    def test_delete_signal(self):
        object_name = self.report.get_s3_object_name()
        self.assertIsNotNone(object_name)
        print(object_name)
        sleep(2)
        exists = file_exists_on_s3(object_name)
        self.assertTrue(exists)
        self.report.delete()
        sleep(2)
        exists = file_exists_on_s3(object_name)
        self.assertFalse(exists)
