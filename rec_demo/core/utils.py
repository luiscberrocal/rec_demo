import re
from datetime import date
from decimal import Decimal

import boto3
import botocore
from django.conf import settings
from django.db.models import Model
from django.forms import model_to_dict
from django.utils import timezone


def years_ago(years, from_date=None) -> date:
    if from_date is None:
        from_date = timezone.now().date()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29  # can be removed
        return from_date.replace(month=2, day=28,
                                 year=from_date.year - years)


def parse_role_name(role):
    value = str(role)
    regexp = re.compile(r'\<class\s\'[a-z_]+\.roles\.([\w]+)\'>')
    match = regexp.match(value)
    if match:
        return match.group(1)
    else:
        raise ValueError('{} does not match a role name'.format(value))


def clean_dict(dictionary, clean_for='json', **kwargs):
    """
    Function to clean a model dictionary. It will change:
    1. elements that are None to blank string so it will be valid for POST data.
    2. elements that are date to string value in format %Y-%m-%d
    :param dictionary:
    :return:
    """
    if clean_for not in ['json', 'form', 'all']:
        raise ValueError(f'{clean_for} in not a valid choice')
    for key in dictionary.keys():
        if clean_for == 'json' or clean_for == 'all':
            if dictionary[key] is None:
                dictionary[key] = ''
        if isinstance(dictionary[key], date):
            date_format = kwargs.get('date_format', '%Y-%m-%d')
            dictionary[key] = dictionary[key].strftime(date_format)
        if isinstance(dictionary[key], Decimal):
            dictionary[key] = str(dictionary[key])
        if clean_for == 'form' or clean_for == 'all':
            if isinstance(dictionary[key], Model):
                dictionary[key] = dictionary[key].pk
    return dictionary


def model_to_json_dict(instance, **kwargs):
    model_dict = model_to_dict(instance)
    clean_data = clean_dict(model_dict, **kwargs)
    return clean_data


def convert_to_decimal(data):
    if isinstance(data, list):
        new_list = list()
        for dec in data:
            new_list.append(convert_to_decimal(dec))
        return new_list
    elif isinstance(data, str):
        clean_dec = data.replace(',', '')
        return Decimal(clean_dec)
    elif isinstance(data, Decimal):
        return data
    else:
        raise ValueError('Unsupported type to convert to decimal')


class CaseChanger(object):
    def filters(self):
        return {'to_snake_case': self.to_snake_case,
                'to_dash_case': self.to_dash_case,
                'to_camel_case': self.to_camel_case}

    def to_snake_case(self, variable_name):
        """
        Converts from TransactionType to transaction_type
        :param variable_name:
        :return:
        """
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', variable_name).lower()
        return name

    def to_dash_case(self, variable_name):
        """
        Converts from TransactionType to transaction-type
        :param variable_name:
        :return:
        """
        name = re.sub(r'(?<!^)(?=[A-Z])', '-', variable_name).lower()
        return name

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return ''.join(x.title() for x in components)


def file_exists_on_s3(filename, bucket_name=None, s3_client=None):
    if filename is None:
        return False
    if bucket_name is None:
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    if s3_client is None:
        s3_client = get_s3_client()
    try:
        s3_client.get_object_acl(Bucket=bucket_name, Key=filename )
        return True
    except Exception as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            return False
        else:
            raise e #TODO Wrap in core Exception
    raise CoreException('Could not find file in bucket')


def get_s3_client():
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    s3_client = session.client('s3')
    return s3_client

