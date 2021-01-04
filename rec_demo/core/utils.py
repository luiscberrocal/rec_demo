
import re
from datetime import date

from django.forms import model_to_dict
from django.utils import timezone


def years_ago(years, from_date=None) -> date:
    if from_date is None:
        from_date = timezone.now().date()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29 # can be removed
        return from_date.replace(month=2, day=28,
                                 year=from_date.year-years)



def parse_role_name(role):
    value = str(role)
    regexp = re.compile(r'\<class\s\'[a-z_]+\.roles\.([\w]+)\'>')
    match = regexp.match(value)
    if match:
        return match.group(1)
    else:
        raise ValueError('{} does not match a role name'.format(value))


def clean_dict(dictionary, **kwargs):
    """
    Function to clean a model dictionary. It will change:
    1. elements that are None to blank string so it will be valid for POST data.
    2. elements that are date to string value in format %Y-%m-%d
    :param dictionary:
    :return:
    """
    for key in dictionary.keys():
        if dictionary[key] is None:
            dictionary[key] = ''
        if isinstance(dictionary[key], date):
            date_format = kwargs.get('date_format','%Y-%m-%d' )
            dictionary[key] = dictionary[key].strftime(date_format)
    return dictionary


def model_to_json_dict(instance, **kwargs):
    model_dict = model_to_dict(instance)
    clean_data = clean_dict(model_dict, **kwargs)
    return clean_data
