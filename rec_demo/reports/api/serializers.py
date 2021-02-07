from rest_framework import serializers

from ..models import Report


class ReportPostSerializer(serializers.ModelSerializer):
    """
    Standard Serializer for Report model.
    """

    class Meta:
        model = Report
        fields = ('id', 'name', 'task_id', 'url', 'metadata', 'created', 'modified', 'created_by', 'modified_by',)


class ReportSerializer(ReportPostSerializer):
    """
    Standard Serializer for Report model.
    """
    pass