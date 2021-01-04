from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
#from django_countries.fields import CountryField
from model_utils.models import TimeStampedModel


class Human(TimeStampedModel):
    MALE_SEX = 'M'
    FEMALE_SEX = 'F'
    SEX_CHOICES = ((MALE_SEX, _('Male')),
                   (FEMALE_SEX, _('Female')))

    NATIONAL_ID = 'NATIONAL_ID'
    RESIDENT_ID = 'RESIDENT_ID'
    DRIVERS_LICENSE = 'DRIVERS_LICENSE'
    PASSPORT = 'PASSPORT'
    OTHER = 'OTHER'

    NATIONAL_ID_TYPE_CHOICES = (
        (NATIONAL_ID, _('National Id')),
        (RESIDENT_ID, _('Resident Id')),
        (DRIVERS_LICENSE, _('Drivers License')),
        (PASSPORT, _('Passport')),
        (OTHER, _('Other')),
    )

    first_name = models.CharField(_('First name'), max_length=60, null=True, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=60, null=True, blank=True)
    last_name = models.CharField(_('Last name'), max_length=60, null=True, blank=True)
    sex = models.CharField(_('Gender'), max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    national_id = models.CharField('National id', max_length=50)
    national_id_type = models.CharField(_('National id type'), max_length=20,
                                        choices=NATIONAL_ID_TYPE_CHOICES, default=NATIONAL_ID)
    #country_for_id = CountryField(_('Country for id'))
    picture = models.ImageField(_('Picture'), null=True, blank=True)
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    blood_type = models.CharField('Blood type', max_length=4, null=True, blank=True)
    religion = models.CharField(_('Religion'), max_length=60, null=True, blank=True)

    @property
    def age(self):
        if self.date_of_birth is None:
            return -1
        today = timezone.now().date()
        try:
            birthday = self.date_of_birth.replace(year=today.year)

            # raised when birth date is February 29
        # and the current year is not a leap year
        except ValueError:
            birthday = self.date_of_birth.replace(year=today.year,
                                    month=self.date_of_birth.month + 1, day=1)

        if birthday > today:
            return today.year - self.date_of_birth.year - 1
        else:
            return today.year - self.date_of_birth.year

    class Meta:
        abstract = True


class Auditable(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='created_%(class)s', null=True, on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='modified_%(class)s', null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
