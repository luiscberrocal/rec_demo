from django.urls import path

from .views import contract_list_view, contract_create_view, contract_update_view, contract_delete_view, \
    contract_detail_view

app_name = "real_estate"

urlpatterns = [
   #contract CRUD urls
   path(r'contract/list/', contract_list_view, name='list-contract'),
   path(r'contract/create/', contract_create_view, name='create-contract'),
   path(r'contract/update/<int:pk>/', contract_update_view, name='update-contract'),
   path(r'contract/delete/<int:pk>/', contract_delete_view, name='delete-contract'),
   path(r'contract/<int:pk>/', contract_detail_view, name='detail-contract'),

]