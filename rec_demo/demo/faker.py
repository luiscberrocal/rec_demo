import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model

from ..real_estate.exceptions import RealEstateException
from ..real_estate.models import Client, Broker


def create_clients(**kwargs):
    results = _create_people(Client, **kwargs)
    return results


def create_broker(**kwargs):
    results = _create_people(Broker, **kwargs)
    return results


def _create_people(RECModel, **kwargs):
    model_name = RECModel.__name__.lower()
    filename = kwargs.get('filename', settings.APPS_DIR / f'demo/fake_{model_name}s.json')
    delete = kwargs.get('delete', False)
    user = kwargs.get('user', get_user_model().objects.first())
    if user is None:
        msg = 'A user must exist in the database for the created_by attribute'
        raise RealEstateException(msg)
    if not os.path.exists(filename):
        raise RealEstateException(f"File {filename} not found for {model_name}")
    with open(filename, 'r', encoding='utf-8') as json_file:
        model_list = json.load(json_file)
    for model_data in model_list:
        model_data['created_by'] = user
        try:
            rec_model = RECModel.objects.get(national_id=model_data['national_id'])
            if delete:
                rec_model.delete()
                raise RECModel.DoesNotExist
            else:
                model_data['created'] = False
                model_data['id'] = rec_model.id
        except RECModel.DoesNotExist:
            model_data['full_name'] = f'{model_data["first_name"]} {model_data["last_name"]}'
            rec_model = RECModel.objects.create(**model_data)
            model_data['created'] = True
            model_data['id'] = rec_model.id
    return model_list

