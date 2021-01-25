from rest_framework import serializers

from ..models import Transaction, TransactionType


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


class TransactionTypePostSerializer(serializers.ModelSerializer):
    """
    Standard Serializer for Transaction model.
    """

    class Meta:
        model = TransactionType
        fields = ('id', 'name', 'short_name', 'allowed_for', 'created', 'modified', 'created_by', 'modified_by',)


class TransactionTypeSerializer(TransactionTypePostSerializer):
    """
    Standard Serializer for Transaction model.
    """
    pass
