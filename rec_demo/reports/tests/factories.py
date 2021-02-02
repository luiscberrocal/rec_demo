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

faker = FakerFactory.create()