from django.urls import path

from .views import report_list_api_view, report_create_api_view, report_detail_api_view

app_name = "reports-api"
urlpatterns = [
    # Report CRUD urls
    path('report/list/', report_list_api_view, name='list-report'),
    #path('report/create/', report_create_api_view, name='create-report'),
   # path('report/update/<int:pk>/', report_detail_api_view, name='update-report'),
    path('report/delete/<int:pk>/', report_detail_api_view, name='delete-report'),
    path('report/<int:pk>/', report_detail_api_view, name='detail-report'),

]
