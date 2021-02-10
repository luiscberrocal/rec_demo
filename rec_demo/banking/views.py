from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from .forms import AccountForm, PaymentPlanForm
from .models import Account
from ..core.mixins import AuditableViewMixin


class AccountCreateView(AuditableViewMixin, LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm

    # success_url = reverse_lazy('banking:list-account')

    def get_success_url(self):
        return reverse('real_estate:detail-contract', args=(self.object.id,))


account_create_view = AccountCreateView.as_view()


class AccountUpdateView(AuditableViewMixin, LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm

    # success_url = reverse_lazy('banking:list-account')

    def get_success_url(self):
        return reverse('real_estate:detail-contract', args=(self.object.contract.id,))


account_update_view = AccountUpdateView.as_view()


class AccountListView(AuditableViewMixin, LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'account_list'
    paginate_by = 10


account_list_view = AccountListView.as_view()


class AccountDeleteView(AuditableViewMixin, LoginRequiredMixin, DeleteView):
    model = Account
    success_url = reverse_lazy('banking:list-account')


account_delete_view = AccountDeleteView.as_view()


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account


account_detail_view = AccountDetailView.as_view()


class PaymentPlanUpdateView(AuditableViewMixin, LoginRequiredMixin, UpdateView):
    model = Account
    form_class = PaymentPlanForm
    template_name = 'banking/payment_plan_form.html'

    def get_success_url(self):
        return reverse('real_estate:detail-contract', args=(self.object.contract.id,))


payment_plan_update_view = PaymentPlanUpdateView.as_view()

