from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

from .serializers import TransactionSerializer, TransactionTypeSerializer
from ..models import Transaction, TransactionType


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


class TransactionTypeListAPIView(ListAPIView):
    serializer_class = TransactionTypeSerializer

    def get_queryset(self):
        qs = TransactionType.objects.all()
        if self.kwargs.get('type_cr') == 'debit':
            qs = qs.filter(Q(allowed_for=TransactionType.ALLOWED_FOR_DEBIT) |
                           Q(allowed_for=TransactionType.ALLOWED_FOR_ALL))
        if self.kwargs.get('type_cr') == 'credit':
            qs = qs.filter(Q(allowed_for=TransactionType.ALLOWED_FOR_CREDIT) |
                           Q(allowed_for=TransactionType.ALLOWED_FOR_ALL))
        return qs


transaction_type_list_api_view = TransactionTypeListAPIView.as_view()


class TransactionTypeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionTypeSerializer
    queryset = TransactionType.objects.all()

    def get_object(self):
        return super(TransactionTypeDetailAPIView, self).get_object()


transaction_type_detail_api_view = TransactionTypeDetailAPIView.as_view()


class TransactionTypeCreateAPIView(CreateAPIView):
    serializer_class = TransactionTypeSerializer


transaction_type_create_api_view = TransactionTypeCreateAPIView.as_view()
