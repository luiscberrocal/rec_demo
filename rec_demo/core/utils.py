import re
from datetime import date
from decimal import Decimal

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
