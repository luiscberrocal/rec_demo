import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from slugify import slugify

from ..real_estate.exceptions import RealEstateException
from ..real_estate.models import Client, Broker, Company, RealEstateProject
from ..real_estate.utils import create_spaces


def create_clients(**kwargs):
    results = _create_people(Client, **kwargs)
    return results


def create_broker(**kwargs):
    results = _create_people(Broker, **kwargs)
    return results


def create_companies(**kwargs):
    results = _create_people(Company, **kwargs)
    return results


def create_real_estate_projects(**kwargs):
    company = kwargs.get('company', Company.objects.first())
    if company is None:
        raise RealEstateException('To create real estate projects a company must exist')
    results = _create_people(RealEstateProject, **kwargs)
    return results


def _create_people(RECModel, **kwargs):
    model_name = RECModel.__name__.lower()
    filename = kwargs.get('filename', settings.APPS_DIR / f'demo/fake_{model_name}_data.json')
    delete = kwargs.get('delete', False)
    user = kwargs.get('user', get_user_model().objects.first())
    company = kwargs.get('company')
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
            if model_name in ['client', 'broker']:
                rec_model = RECModel.objects.get(national_id=model_data['national_id'])
            else:
                rec_model = RECModel.objects.get(name=model_data['name'])
            if delete:
                rec_model.delete()
                raise RECModel.DoesNotExist
            else:
                model_data['created'] = False
                model_data['id'] = rec_model.id
        except RECModel.DoesNotExist:
            if model_name in ['client', 'broker']:
                model_data['full_name'] = f'{model_data["first_name"]} {model_data["last_name"]}'
            elif model_name == 'realestateproject':
                spaces_data = dict()
                to_del = [key for key in model_data if key not in ['name', 'company', 'created_by']]
                for key in to_del:
                    spaces_data[key] = model_data.get(key)
                for key in to_del:
                    del model_data[key]
                model_data['short_name'] = slugify(model_data['name'])
                model_data['company'] = company

            elif model_name == 'company':
                pass
            else:
                msg = f'Model {model_name} is not supported'
                raise RealEstateException(msg)

            rec_model = RECModel.objects.create(**model_data)
            if model_name == 'realestateproject':
                floors = spaces_data.pop('floors')
                create_spaces(rec_model, floors, **spaces_data)

            model_data['created'] = True
            model_data['id'] = rec_model.id
    return model_list
