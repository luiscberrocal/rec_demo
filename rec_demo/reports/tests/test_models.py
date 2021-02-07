from test_plus import TestCase

from ..models import Report
from ..tasks import create_transaction_report_task
from ...core.utils import file_exists_on_s3
from ...users.tests.factories import SimpleUserFactory


class TestReport(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = SimpleUserFactory.create()
        report_config = {'location': 'S3', 'expiration_time': 3000}  ###TODO Set in settings
        task_id = create_transaction_report_task.delay(**report_config)
        report_data = dict()
        report_data['name'] = 'TEST'
        report_data['task_id'] = task_id
        report_data['metadata'] = {'config': report_config}
        report_data['created_by'] = user
        report_data['modified_by'] = None

        cls.report = Report.objects.create(**report_data)
        #cls.report.update_report_metadata()

    def test_delete_signal(self):
        if self.report.get_s3_object_name() is None:
            self.report.update_report_metadata()
        object_name = self.report.get_s3_object_name()
        self.report.delete()
        exists = file_exists_on_s3(object_name)
        self.assertFalse(exists)

