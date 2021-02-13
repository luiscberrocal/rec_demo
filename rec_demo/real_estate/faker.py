import json
import os

from django.conf import settings

from .exceptions import RealEstateException
from .models import Client, Broker


def create_clients(**kwargs):
    filename = kwargs.get('filename', settings.APPS_DIR / 'real_estate/fake_clients.json')
    if not os.path.exists(filename):
        raise RealEstateException('File not found')
    with open(filename, 'r', encoding='utf-8') as json_file:
        client_list = json.load(json_file)
    for client_data in client_list:
        try:
            client = Client.objects.get(national_id=client_data['national_id'])
            client_data['created'] = False
            client_data['id'] = client.id
        except Client.DoesNotExist:
            client_data['full_name'] = f'{client_data["first_name"]} {client_data["last_name"]}'
            client = Client.objects.create(**client_data)
            client_data['created'] = True
            client_data['id'] = client.id
    return client_list


def create_broker(**kwargs):
    filename = kwargs.get('filename', settings.APPS_DIR / 'real_estate/fake_broker.json')
    if not os.path.exists(filename):
        raise RealEstateException('File not found')
    with open(filename, 'r', encoding='utf-8') as json_file:
        broker_list = json.load(json_file)
    for broker_data in broker_list:
        try:
            broker = Broker.objects.get(national_id=broker_data['national_id'])
            broker_data['created'] = False
            broker_data['id'] = broker.id
        except Client.DoesNotExist:
            broker_data['full_name'] = f'{broker_data["first_name"]} {broker_data["last_name"]}'
            broker = Client.objects.create(**broker_data)
            broker_data['created'] = True
            broker_data['id'] = broker.id
    return broker_list
