from django.urls import path

from .views import account_list_view, account_create_view, account_update_view, account_delete_view, account_detail_view

app_name = "banking"

urlpatterns = [
    # Account CRUD urls
    path(r'account/list/', account_list_view, name='list-account'),
    path(r'account/create/', account_create_view, name='create-account'),
    path(r'account/update/<int:pk>/', account_update_view, name='update-account'),
    path(r'account/delete/<int:pk>/', account_delete_view, name='delete-account'),
    path(r'account/<int:pk>/', account_detail_view, name='detail-account'),

]
