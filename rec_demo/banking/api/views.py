from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

from .serializers import TransactionSerializer
from ..models import Transaction


class TransactionListAPIView(ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        qs = Transaction.objects.all()
        if self.kwargs.get('account_pk'):
            qs = qs.filter(account__pk=self.kwargs['account_pk'])
        if self.kwargs.get('type') == 'credit':
            qs = qs.filter(type=Transaction.DEBIT_TYPE)
        return qs


transaction_list_api_view = TransactionListAPIView.as_view()


class TransactionDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_object(self):
        return super(TransactionDetailAPIView, self).get_object()


transaction_detail_api_view = TransactionDetailAPIView.as_view()


class TransactionCreateAPIView(CreateAPIView):
    serializer_class = TransactionSerializer


transaction_create_api_view = TransactionCreateAPIView.as_view()
