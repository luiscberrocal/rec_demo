from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Report
from ..core.utils import file_exists_on_s3, get_s3_client


@receiver(pre_delete, sender=Report)
def report_pre_delete(sender, **kwargs):
    report = kwargs['instance']
    s3_client = get_s3_client()
    s3_object_name = report.get_s3_object_name()
    bucket = settings.AWS_STORAGE_BUCKET_NAME
    if file_exists_on_s3(s3_object_name, s3_client=s3_client):
        s3_client.delete_object(Bucket=bucket, Key=s3_object_name)






