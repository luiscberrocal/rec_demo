from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DeleteView, DetailView

from .forms import ReportForm
from .models import Report
from .utils import generate_transaction_report


class ReportCreateView(LoginRequiredMixin, FormView):
    form_class = ReportForm
    success_url = reverse_lazy('reports:list-report')
    template_name = 'reports/report_form.html'

    def form_valid(self, form):
        self.build_report(form.cleaned_data)
        return super(ReportCreateView, self).form_valid(form)

    def build_report(self, cleaned_data):
        report_data = dict()
        report_data['name'] = cleaned_data['type']
        report_data['task_id'] = '999'
        report_data['url'] = generate_transaction_report(location='S3', expiration_time=3000)
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
