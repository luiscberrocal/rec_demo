from celery.result import AsyncResult
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

from .serializers import ReportSerializer
from ..models import Report


class ReportListAPIView(ListAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        return Report.objects.all()


report_list_api_view = ReportListAPIView.as_view()


class ReportDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    def get_object(self):
        update_report = False
        report = super(ReportDetailAPIView, self).get_object()
        report.update_report_metadata()
        return report


report_detail_api_view = ReportDetailAPIView.as_view()


class ReportCreateAPIView(CreateAPIView):
    serializer_class = ReportSerializer


report_create_api_view = ReportCreateAPIView.as_view()
