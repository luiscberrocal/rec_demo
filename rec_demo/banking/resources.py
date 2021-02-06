from import_export import resources

from .models import Transaction


class TransactionResource(resources.ModelResource):
    #project = resources.Field(column_name='project')

    class Meta:
        model = Transaction
        fields = ('id',
                  #'project',
                  'type', 'date', 'account', 'transaction_type', 'amount', 'comments',
                  'due_date', 'related_debit', 'created', 'modified', 'created_by', 'modified_by')
        export_order = ('id',
                        #'project',
                        'type', 'date', 'account', 'transaction_type', 'amount', 'comments',
                        'due_date', 'related_debit', 'created', 'modified', 'created_by', 'modified_by')

    # noinspection PyMethodMayBeStatic
    # def dehydrate_project(self, obj):
    #     if hasattr(obj, 'account') and obj.account is not None:
    #         return obj.account.contract.project.name
