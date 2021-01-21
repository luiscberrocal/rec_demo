from rest_framework import serializers

from ..models import Transaction


class TransactionPostSerializer(serializers.ModelSerializer):
    """
    Standard Serializer for Transaction model.
    """

    class Meta:
        model = Transaction
        fields = ('id', 'type', 'date', 'account', 'transaction_type', 'amount', 'comments',
                  'due_date', 'related_debit', 'created', 'modified', 'created_by', 'modified_by',)


class TransactionSerializer(TransactionPostSerializer):
    """
    Standard Serializer for Transaction model.
    """
    pass
