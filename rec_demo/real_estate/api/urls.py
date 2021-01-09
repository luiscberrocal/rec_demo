from django.urls import path, re_path

from .views import real_estate_space_list_api_view

app_name = "real_estate-api"
urlpatterns = [

    # RealEstateSpace CRUD urls
    path('real-estate-space/list/', real_estate_space_list_api_view, name='list-real-estate-space'),
    re_path('^real-estate-space/list/(?P<project_id>.+)/$', real_estate_space_list_api_view,
            name='list-real-estate-space-by-project'),
    # path('real-estate-space/create/', real_estate_space_create_api_view, name='create-real-estate-space'),
    # path('real-estate-space/update/<int:pk>/', real_estate_space_detail_api_view, name='update-real-estate-space'),
    # path('real-estate-space/delete/<int:pk>/', real_estate_space_detail_api_view, name='delete-real-estate-space'),
    # path('real-estate-space/<int:pk>/', real_estate_space_detail_api_view, name='detail-real-estate-space'),

]
