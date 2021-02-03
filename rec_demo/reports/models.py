from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from model_utils.models import TimeStampedModel

from ..core.models import Auditable


class Report(Auditable, TimeStampedModel):
    name = models.CharField(_('Name'), max_length=80)
    task_id = models.CharField(_('Task id'), max_length=30)
    metadata = JSONField(_('Metadata'), null=True, blank=True)
