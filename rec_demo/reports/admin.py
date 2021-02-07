# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'task_id', 'url', 'metadata', 'created', 'modified', 'created_by', 'modified_by',)
    list_filter = ('created', 'modified', 'created_by', 'modified_by')
    search_fields = ('name',)
