import tempfile

from ..real_estate.models import Client
from ..real_estate.resources import ClientResource


def generate_client_report(**kwargs):
    qs = Client.objects.all()
    resource = ClientResource()

    base_filename = kwargs.get('filename', 'client.xlsx')
    dataset = resource.export(queryset=qs)
    if 'LOCAL' == 'LOCAL':
        filename = base_filename #self._get_report_filename(filename=base_filename)
        with open(filename, 'wb') as excel_file:
            excel_file.write(dataset.xlsx)
        #self.clean_up(filename, model_name)
        return filename
    elif 'SSSS' == 'S3':
        object_name = base_filename
        with tempfile.NamedTemporaryFile() as temp:
            filename = temp.name + '.xlsx'
            with open(filename, 'wb') as excel_file:
                excel_file.write(dataset.xlsx)
            #self.clean_up(filename, model_name)
            #url = self._upload_to_s3(filename, object_name)
        return url
    else:
        msg = f'{location} is not a supported location for writing reports'
        raise FinanceException(msg)