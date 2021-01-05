# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from .forms import ContractForm
from .models import Contract
from ..core.mixins import AuditableViewMixin


class ContractCreateView(AuditableViewMixin, LoginRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy('real_estate:list-contract')


contract_create_view = ContractCreateView.as_view()


class ContractUpdateView(AuditableViewMixin, LoginRequiredMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy('real_estate:list-contract')


contract_update_view = ContractUpdateView.as_view()


class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    context_object_name = 'contract_list'
    paginate_by = 10


contract_list_view = ContractListView.as_view()


class ContractDeleteView(LoginRequiredMixin, DeleteView):
    model = Contract
    success_url = reverse_lazy('real_estate:list-contract')


contract_delete_view = ContractDeleteView.as_view()


class ContractDetailView(LoginRequiredMixin, DetailView):
    model = Contract


contract_detail_view = ContractDetailView.as_view()
