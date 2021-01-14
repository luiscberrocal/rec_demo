from import_export import resources

from .models import Company, Client


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company
        fields = ('id', 'name', 'short_name')
        export_order = ('id', 'name', 'short_name')


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'sex', 'national_id', 'national_id_type',
                  'country_for_id', 'full_name', 'client_type', )

