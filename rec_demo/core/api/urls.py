from django.urls import path

from .views import app_data

app_name = "core-api"
urlpatterns = [
    path('version', app_data, name='app_data'),
]
