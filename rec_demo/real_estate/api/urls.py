from django.urls import path

from rec_demo.real_estate.api.views import real_estate_space_list_api_view, real_estate_space_create_api_view, \
    real_estate_space_detail_api_view

app_name = "real_estate-api"
urlpatterns = [

    #RealEstateSpace CRUD urls
    path('real-estate-space/list/', real_estate_space_list_api_view, name='list-real-estate-space'),
    # path('real-estate-space/create/', real_estate_space_create_api_view, name='create-real-estate-space'),
    # path('real-estate-space/update/<int:pk>/', real_estate_space_detail_api_view, name='update-real-estate-space'),
    # path('real-estate-space/delete/<int:pk>/', real_estate_space_detail_api_view, name='delete-real-estate-space'),
    # path('real-estate-space/<int:pk>/', real_estate_space_detail_api_view, name='detail-real-estate-space'),

]