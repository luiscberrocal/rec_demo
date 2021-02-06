from django.urls import path, re_path

from .views import real_estate_space_list_api_view, contract_list_api_view, contract_create_api_view, \
    contract_detail_api_view, real_estate_space_detail_api_view

app_name = "real_estate-api"
urlpatterns = [

    # RealEstateSpace CRUD urls
    path('real-estate-space/list/', real_estate_space_list_api_view, name='list-real-estate-space'),
    re_path('^real-estate-space/list/(?P<project_id>.+)/$', real_estate_space_list_api_view,
            name='list-real-estate-space-by-project'),
    # path('real-estate-space/create/', real_estate_space_create_api_view, name='create-real-estate-space'),
    # path('real-estate-space/update/<int:pk>/', real_estate_space_detail_api_view, name='update-real-estate-space'),
    # path('real-estate-space/delete/<int:pk>/', real_estate_space_detail_api_view, name='delete-real-estate-space'),
    path('real-estate-space/<int:pk>/', real_estate_space_detail_api_view, name='detail-real-estate-space'),
    #//contract=snakeCase(MODEL)
    #//contract=lowercaseAndDash(MODEL)

    #Contract CRUD urls
    # path('contract/list/', contract_list_api_view, name='list-contract'),
    # path('contract/create/', contract_create_api_view, name='create-contract'),
    # path('contract/update/<int:pk>/', contract_detail_api_view, name='update-contract'),
    # path('contract/delete/<int:pk>/', contract_detail_api_view, name='delete-contract'),
    path('contract/<int:pk>/', contract_detail_api_view, name='detail-contract'),


]
