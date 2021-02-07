from celery.result import AsyncResult
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DeleteView, DetailView
from django.views.generic.base import View

from .forms import ReportForm
from .models import Report
from .tasks import create_transaction_report_task


class ReportCreateView(LoginRequiredMixin, FormView):
    form_class = ReportForm
    success_url = reverse_lazy('reports:list-report')
    template_name = 'reports/report_form.html'

    def form_valid(self, form):
        self.build_report(form.cleaned_data)
        return super(ReportCreateView, self).form_valid(form)

    def build_report(self, cleaned_data):
        report_config = {'location': 'S3', 'expiration_time': 3000} ###TODO Set in settings
        task_id = create_transaction_report_task.delay(**report_config)
        report_data = dict()
        report_data['name'] = cleaned_data['type']
        report_data['task_id'] = task_id
        report_data['metadata'] = {'config': report_config}
        Report.objects.create(**report_data)


report_create_view = ReportCreateView.as_view()


# class ReportUpdateView(LoginRequiredMixin, UpdateView):
#     model = Report
#     form_class = ReportForm
#     success_url = reverse_lazy('reports:list-report')
#
# report_update_view = ReportUpdateView.as_view()

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    context_object_name = 'report_list'
    paginate_by = 10


report_list_view = ReportListView.as_view()


class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    success_url = reverse_lazy('reports:list-report')


report_delete_view = ReportDeleteView.as_view()


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report


report_detail_view = ReportDetailView.as_view()


class ReportStatusView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
        return JsonResponse(result, status=200)

report_status_view = ReportStatusView.as_view()