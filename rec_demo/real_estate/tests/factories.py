import string
from decimal import Decimal

from django.conf import settings
from factory import Iterator, lazy_attribute
from factory import LazyAttribute
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from faker import Factory as FakerFactory
from pytz import timezone

from ..models import Company, RealEstateProject, RealEstateSpace, Client, Broker, Contract, ContractClient, \
    ContractBroker
from ...users.tests.factories import UserFactory

faker = FakerFactory.create()


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=80))
    short_name = LazyAttribute(lambda x: faker.text(max_nb_chars=15))
    # Field type ImageField for field logo is not currently supported
    created_by = SubFactory(UserFactory)

    @lazy_attribute
    def modified_by(self):
        return self.created_by


class RealEstateProjectFactory(DjangoModelFactory):
    class Meta:
        model = RealEstateProject

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=80))
    short_name = LazyAttribute(lambda x: faker.text(max_nb_chars=15))
    company = SubFactory(CompanyFactory)
    # Field type ImageField for field logo is not currently supported
    created_by = SubFactory(UserFactory)

    @lazy_attribute
    def modified_by(self):
        return self.created_by


class RealEstateSpaceFactory(DjangoModelFactory):
    class Meta:
        model = RealEstateSpace

    project = SubFactory(RealEstateProjectFactory)
    name = LazyAttribute(lambda x: faker.text(max_nb_chars=20))
    space_type = Iterator((('LIVING', 'Living space'),
                           ('PARKING', 'Parking'), ('STORAGE', 'Storage'), ('OTHER', 'Other')),
                          getter=lambda x: x[0])
    area = LazyAttribute(lambda x: faker.pydecimal(left_digits=4, right_digits=2, positive=True, min_value=50.0,
                                                   max_value=500.0))
    contract = None  # SubFactory(ContractFactory)

    created_by = SubFactory(UserFactory)

    @lazy_attribute
    def modified_by(self):
        return self.created_by

    @lazy_attribute
    def price(self):
        return self.area * Decimal('1200.00')


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client

    # middle_name = LazyAttribute(lambda x: FuzzyText(length=60, chars=string.digits).fuzz())
    sex = Iterator((('M', 'Male'), ('F', 'Female')), getter=lambda x: x[0])
    national_id = LazyAttribute(lambda x: FuzzyText(length=50, chars=string.digits).fuzz())
    national_id_type = Iterator((('NATIONAL_ID', 'National Id'), ('DRIVERS_LICENSE', 'Drivers License'),
                                 ('PASSPORT', 'Passport'), ('OTHER', 'Other')), getter=lambda x: x[0])
    country_for_id = Iterator(['PA', 'US', 'GB', ])
    # Field type ImageField for field picture is not currently supported
    date_of_birth = LazyAttribute(
        lambda x: faker.date_of_birth(tzinfo=timezone(settings.TIME_ZONE), minimum_age=18, maximum_age=90))
    religion = Iterator(['Catolico', 'Protestante', 'Judio', ])
    client_type = Iterator((('N', 'Natural person'), ('J', 'Juridical person')), getter=lambda x: x[0])

    created_by = SubFactory(UserFactory)

    @lazy_attribute
    def modified_by(self):
        return self.created_by

    @lazy_attribute
    def first_name(self):
        if self.client_type == 'N':
            if self.sex == 'M':
                return faker.first_name_male()
            else:
                return faker.first_name_female()
        else:
            return None

    @lazy_attribute
    def last_name(self):
        if self.client_type == 'N':
            return faker.last_name()
        else:
            return None

    @lazy_attribute
    def full_name(self):
        if self.client_type == 'N':
            return f'{self.last_name}, {self.first_name}'
        else:
            return faker.company()


class BrokerFactory(ClientFactory):
    class Meta:
        model = Broker


class ContractFactory(DjangoModelFactory):
    class Meta:
        model = Contract

    date = LazyAttribute(
        lambda x: faker.date_time_between(start_date="-1y", end_date="now", tzinfo=timezone(settings.TIME_ZONE)).date())
    project = SubFactory(RealEstateProjectFactory)

    created_by = SubFactory(UserFactory)

    @lazy_attribute
    def modified_by(self):
        return self.created_by


class ContractClientFactory(DjangoModelFactory):
    class Meta:
        model = ContractClient

    client = SubFactory(ClientFactory)
    contract = SubFactory(ContractFactory)
    is_principal = Iterator([True, False])

    created_by = SubFactory(UserFactory)

    @lazy_attribute
    def modified_by(self):
        return self.created_by


class ContractBrokerFactory(DjangoModelFactory):
    class Meta:
        model = ContractBroker

    broker = SubFactory(BrokerFactory)
    contract = SubFactory(ContractFactory)
    is_active = Iterator([True, False])

    created_by = SubFactory(UserFactory)

    @lazy_attribute
    def modified_by(self):
        return self.created_by
