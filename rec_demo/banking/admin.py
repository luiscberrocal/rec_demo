# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Account, TransactionType, Debit, Credit, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'modified', 'created_by', 'modified_by',)
    list_filter = ('created', 'modified', 'created_by', 'modified_by')
    search_fields = ('name',)


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name', 'allowed_for', 'created', 'modified', 'created_by', 'modified_by',)
    list_filter = ('created', 'modified', 'created_by', 'modified_by')
    search_fields = ('name',)


@admin.register(Debit)
class DebitAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'account', 'transaction_type', 'amount', 'comments', 'due_date', 'created',
                    'modified', 'created_by', 'modified_by')
    list_filter = ('date', 'account', 'transaction_type', 'due_date',)


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'account', 'transaction_type', 'amount', 'related_debit', 'comments', 'created',
                    'modified', 'created_by', 'modified_by',)
    list_filter = ('date', 'account', 'transaction_type', 'related_debit',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'date', 'account', 'transaction_type', 'amount', 'comments',
                    'due_date', 'related_debit', 'created', 'modified', 'created_by', 'modified_by',)
    list_filter = ('date', 'account', 'transaction_type', 'due_date', 'created_by', 'modified_by',)
