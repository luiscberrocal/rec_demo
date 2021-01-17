from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
# Create your models here.
from model_utils.models import TimeStampedModel

from .exceptions import RealEstateException
from ..banking.models import Account
from ..core.models import Auditable, Human


class Company(Auditable, TimeStampedModel):
    name = models.CharField(_('Name'), max_length=80)
    short_name = models.CharField(_('Short name'), max_length=15)
    logo = models.ImageField(_('Logo'), null=True, blank=True)
    active = models.BooleanField(_('Active'), default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')


class RealEstateProject(Auditable, TimeStampedModel):
    name = models.CharField(_('Name'), max_length=80)
    short_name = models.CharField(_('Short name'), max_length=15)
    company = models.ForeignKey(Company, verbose_name=_('Company'),
                                related_name='real_estate_projects', on_delete=models.CASCADE)
    logo = models.ImageField(_('Logo'), null=True, blank=True)
    active = models.BooleanField(_('Active'), default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Real estate project')
        verbose_name_plural = _('Real estate projects')


class RealEstateSpace(Auditable, TimeStampedModel):
    PARKING_SPACE = 'PARKING'
    LIVING_SPACE = 'LIVING'
    STORAGE_SPACE = 'STORAGE'
    OTHER_SPACE = 'OTHER'

    SPACE_TYPE_CHOICES = (
        (LIVING_SPACE, _('Living space')),
        (PARKING_SPACE, _('Parking')),
        (STORAGE_SPACE, _('Storage')),
        (OTHER_SPACE, _('Other')),
    )
    project = models.ForeignKey(RealEstateProject, verbose_name=_('Project'),
                                on_delete=models.CASCADE, related_name='real_estate_spaces')
    name = models.CharField(_('Name'), max_length=20)
    space_type = models.CharField(_('Space type'), max_length=8, choices=SPACE_TYPE_CHOICES,
                                  default=LIVING_SPACE)
    area = models.DecimalField(_('Area'), max_digits=6, decimal_places=2, default=Decimal('0.00'))
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    contract = models.ForeignKey('Contract', verbose_name=_('Contract'), related_name='real_estate_spaces',
                                 null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project.name} {self.get_space_type_display()} {self.name}'

    class Meta:
        verbose_name = _('Real estate space')
        verbose_name_plural = _('Real estate spaces')
        ordering = ('project__name', 'space_type', 'name')


class Client(Auditable, Human):
    NATURAL_TYPE = 'N'  # Natural
    JURIDICAL_TYPE = 'J'  # Juridical
    CLIENT_TYPE_CHOICES = (
        (NATURAL_TYPE, _('Natural person')),
        (JURIDICAL_TYPE, _('Juridical person')),
    )
    full_name = models.CharField(_('Full name'), max_length=120, null=True, blank=True)
    client_type = models.CharField(_('Client type'), max_length=1, choices=CLIENT_TYPE_CHOICES,
                                   default=NATURAL_TYPE)

    def __str__(self):
        if self.client_type == Client.NATURAL_TYPE:
            return f'{self.last_name}, {self.first_name}'
        else:
            return f'{self.full_name}'

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')


class Broker(Auditable, Human):
    NATURAL_TYPE = 'N'  # Natural
    JURIDICAL_TYPE = 'J'  # Juridical
    CLIENT_TYPE_CHOICES = (
        (NATURAL_TYPE, _('Natural person')),
        (JURIDICAL_TYPE, _('Juridical person')),
    )
    full_name = models.CharField(_('Full name'), max_length=120, null=True, blank=True)
    broker_type = models.CharField(_('Broker type'), max_length=1, choices=CLIENT_TYPE_CHOICES,
                                   default=NATURAL_TYPE)

    def __str__(self):
        if self.broker_type == Client.NATURAL_TYPE:
            return f'{self.last_name}, {self.first_name}'
        else:
            return f'{self.full_name}'

    class Meta:
        verbose_name = _('Broker')
        verbose_name_plural = _('Brokers')


class SalesType(Auditable, TimeStampedModel):
    name = models.CharField(_('Name'), max_length=60)
    short_name = models.CharField(_('Short name'), max_length=20, unique=True)
    requires_loan = models.BooleanField(_('Requires loan'), default=False)

    def __str__(self):
        return f'{self.name}'


class Contract(Auditable, TimeStampedModel):
    date = models.DateField(_('Date'))
    project = models.ForeignKey(RealEstateProject, verbose_name=_('Project'), related_name='contracts',
                                on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, verbose_name=_('Broker'), related_name='contracts',
                               on_delete=models.SET_NULL, null=True, blank=True)
    sales_type = models.ForeignKey(SalesType, verbose_name=_('Sales type'), related_name='contracts',
                                   on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(_('Total amount'), max_digits=12, decimal_places=2, default=Decimal('0.00'))
    down_payment = models.DecimalField(_('Down payment'), max_digits=12, decimal_places=2, default=Decimal('0.00'))
    account = models.OneToOneField(Account, verbose_name=_('Account'), related_name='contract',
                                   on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    def __str__(self):
        return f'{self.project.name} ({self.id})'

    def add_space(self, real_estate_space, **kwargs):
        raise_error = kwargs.get('raise_error', True)
        if real_estate_space.project.id == self.project.id:
            if real_estate_space.contract is None:
                real_estate_space.contract = self
                real_estate_space.save()
            else:
                if raise_error:
                    msg = _(f'Real estate space already has a contract {real_estate_space.contract.id}')
                    raise RealEstateException(msg)
        else:
            if raise_error:
                msg = _(f'Contract project and space project are not the same')
                raise RealEstateException(msg)

    def add_client(self, client, **kwargs):
        raise_error = kwargs.get('raise_error', True)
        count = ContractClient.objects.filter(client=client, contract=self).count()
        if count == 0:
            return ContractClient.objects.create(client=client, contract=self)

    def calculate_total(self, **kwargs):
        assign = kwargs.get('assign', False)
        save = kwargs.get('save', False)
        check = kwargs.get('check', False)
        current_total = self.real_estate_spaces.aggregate(Sum('price'))
        total = current_total['price__sum']
        if check and total != self.total_amount:
            msg = _('The sum of prices in the contract is not the same as the total_amount')
            raise RealEstateException(msg)
        if assign:
            self.total_amount = total
        if save and assign:
            self.save()
        return total




class ContractClient(Auditable, TimeStampedModel):
    client = models.ForeignKey(Client, verbose_name=_('Client'), related_name='contract_clients',
                               on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, verbose_name=_('Contract'), related_name='contract_clients',
                                 on_delete=models.CASCADE)
    is_principal = models.BooleanField(_('Is principal'), default=True)

    class Meta:
        ordering = ('is_principal',)


class ContractBroker(Auditable, TimeStampedModel):
    broker = models.ForeignKey(Broker, verbose_name=_('Broker'), related_name='contract_brokers',
                               on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, verbose_name=_('Contract'), related_name='contract_brokers',
                                 on_delete=models.CASCADE)
    is_active = models.BooleanField(_('Is active'), default=True)
