from django.http import JsonResponse

import rec_demo

def app_data(request):
    version = rec_demo.__version__
    data = dict()
    data['version'] = version
    data['name'] = 'REC Demo'
    data['copyright'] = '2021 (c) EMR Consultants'

    return JsonResponse(data)
