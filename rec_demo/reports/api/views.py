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
        task_result = AsyncResult(report.task_id)
        result = {
            "task_id": report.task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
        if report.metadata is None:
            report.metadata = result
        else:
            report.metadata = {**report.metadata, **result}
        if task_result.status == 'SUCCESS2':
            report.url = task_result.result
        report.save()
        return report


report_detail_api_view = ReportDetailAPIView.as_view()


class ReportCreateAPIView(CreateAPIView):
    serializer_class = ReportSerializer


report_create_api_view = ReportCreateAPIView.as_view()
