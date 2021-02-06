from django.urls import path

from .views import report_list_view, report_create_view, report_delete_view, report_detail_view, report_status_view

app_name = "reports"

urlpatterns = [
    #add your views here
    #Report CRUD urls
    path(r'report/list/', report_list_view, name='list-report'),
    path(r'report/create/', report_create_view, name='create-report'),
    #path(r'report/update/<int:pk>/', report_update_view, name='update-report'),
    path(r'report/delete/<int:pk>/', report_delete_view, name='delete-report'),
    path(r'report/<int:pk>/', report_detail_view, name='detail-report'),
    path(r'report/status/<str:task_id>/', report_status_view, name='status-report'),

]