from celery.result import AsyncResult
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
# Create your models here.
from model_utils.models import TimeStampedModel

from ..core.models import Auditable


class Report(Auditable, TimeStampedModel):
    name = models.CharField(_('Name'), max_length=80)
    task_id = models.CharField(_('Task id'), max_length=128)
    url = models.URLField(_('Url'), max_length=256, null=True, blank=True)
    metadata = JSONField(_('Metadata'), null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.url

    def get_s3_object_name(self):
        object_name = None
        if self.metadata is not None and self.metadata.get('task_result'):
            object_name = self.metadata['task_result'].get('s3_object_name', None)

        return object_name

    def update_report_metadata(self):
        if not isinstance(self.task_id, str):
            self.task_id = str(self.task_id)
        task_result = AsyncResult(self.task_id)
        result = {
            "task_id": self.task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
        if self.metadata is None:
            self.metadata = result
        else:
            self.metadata = {**self.metadata, **result}
        if task_result.status == 'SUCCESS':
            self.url = task_result.result
        self.save()