
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
        ordering = ('created', )

    def __str__(self):
        return self.url
