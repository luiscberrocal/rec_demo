from rec_demo.real_estate.models import SalesType


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
