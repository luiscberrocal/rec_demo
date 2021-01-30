from decimal import Decimal

from .exceptions import RealEstateException
from .models import SalesType, RealEstateSpace
from ..core.utils import convert_to_decimal


def get_or_create_sales_types():
    data = [
        {'name': 'Venta al contado', 'short_name': 'CONTADO', 'requires_loan': False},
        {'name': 'Venta al Crédito', 'short_name': 'CREDITO', 'requires_loan': True},
        {'name': 'Alquiler con opción a compra', 'short_name': 'ALQUILER_COMPRA', 'requires_loan': True},
    ]
    for sales_type in data:
        sales_type_count = SalesType.objects.filter(short_name=sales_type['short_name']).count()
        if sales_type_count == 0:
            SalesType.objects.create(**sales_type)
            sales_type['created'] = True
        else:
            sales_type['created'] = False
    return data


def create_spaces(project, floors, **kwargs):
    # Kwargs
    apartment_per_floor = kwargs.get('apartment_per_floor', 4)
    parkings = kwargs.get('parkings', 0)
    parking_default_price = kwargs.get('parking_default_price', Decimal('20000'))
    storage = kwargs.get('storage', 0)
    storage_default_price = kwargs.get('storage_default_price',  Decimal('20000'))
    areas = kwargs.pop('areas', list())
    default_area = kwargs.pop('default_area', Decimal('100.00'))
    price_per_sq_meter = kwargs.pop('price_per_sq_meter', Decimal('1200.00'))
    increment_per_floor = kwargs.pop('increment_per_floor',  Decimal('0.03'))

    apartment_letters = 'ABCDEFGHI'
    areas = convert_to_decimal(areas)
    if len(areas) == 0:
        for i in range(apartment_per_floor):
            areas.append(default_area)
    elif len(areas) != 0 and len(areas) != apartment_per_floor:
        apartment_per_floor = len(areas)

    if apartment_per_floor > len(apartment_letters):
        msg = _('Maximum number of apartments per floor exceeded')
        raise RealEstateException(msg)

    space_list = list()
    floor_increment = Decimal('1.0')
    for floor in range(1, floors + 1):
        for i in range(apartment_per_floor):
            space_data = dict()
            space_data['project'] = project
            space_data['space_type'] = RealEstateSpace.LIVING_SPACE
            space_data['created_by'] = project.created_by
            space_data['name'] = f'{floor}-{apartment_letters[i]}'
            space_data['area'] = areas[i]
            space_data['price'] = areas[i] * price_per_sq_meter * floor_increment
            real_estate_space = RealEstateSpace(**space_data)
            space_list.append(real_estate_space)
        floor_increment += increment_per_floor
    RealEstateSpace.objects.bulk_create(space_list)

    space_list = list()
    for i in range(parkings):
        space_data = dict()
        space_data['project'] = project
        space_data['space_type'] = RealEstateSpace.PARKING_SPACE
        space_data['created_by'] = project.created_by
        space_data['name'] = f'Estacionamiento {i+1}'
        space_data['area'] = None
        space_data['price'] = parking_default_price
        real_estate_space = RealEstateSpace(**space_data)
        space_list.append(real_estate_space)

    for i in range(storage):
        space_data = dict()
        space_data['project'] = project
        space_data['space_type'] = RealEstateSpace.STORAGE_SPACE
        space_data['created_by'] = project.created_by
        space_data['name'] = f'Storage {i + 1}'
        space_data['area'] = None
        space_data['price'] = storage_default_price
        real_estate_space = RealEstateSpace(**space_data)
        space_list.append(real_estate_space)
    if len(space_list) > 0:
        RealEstateSpace.objects.bulk_create(space_list)
    return project