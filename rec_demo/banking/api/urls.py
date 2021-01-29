from django.urls import path

from .views import transaction_list_api_view, transaction_type_list_api_view, transaction_type_create_api_view, \
    transaction_type_detail_api_view

app_name = "banking-api"
urlpatterns = [

    # Transaction CRUD urls
    path('transaction/list/', transaction_list_api_view, name='list-transaction'),
    path('transaction/list/<int:account_pk>', transaction_list_api_view, name='list-transaction-account'),
    path('transaction/list/debits/<int:account_pk>', transaction_list_api_view, {'type': 'debit'},
         name='list-debits-account', ),
    # path('transaction/create/', transaction_create_api_view, name='create-transaction'),
    # path('transaction/update/<int:pk>/', transaction_detail_api_view, name='update-transaction'),
    # path('transaction/delete/<int:pk>/', transaction_detail_api_view, name='delete-transaction'),
    # path('transaction/<int:pk>/', transaction_detail_api_view, name='detail-transaction'),

    # TransactionType CRUD urls
    path('transaction-type/list/', transaction_type_list_api_view, name='list-transaction-type'),
    path('transaction-type/list/credits/', transaction_type_list_api_view, {'type_cr': 'credit'},
         name='list-credit-transaction-type'),
    path('transaction-type/list/debits/', transaction_type_list_api_view, {'type_cr': 'debit'},
         name='list-debit-transaction-type'),
    # path('transaction-type/create/', transaction_type_create_api_view, name='create-transaction-type'),
    # path('transaction-type/update/<int:pk>/', transaction_type_detail_api_view, name='update-transaction-type'),
    # path('transaction-type/delete/<int:pk>/', transaction_type_detail_api_view, name='delete-transaction-type'),
    # path('transaction-type/<int:pk>/', transaction_type_detail_api_view, name='detail-transaction-type'),

]
