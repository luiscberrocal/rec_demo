# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Company, RealEstateProject, RealEstateSpace, Client, Broker, Contract, ContractClient, \
    ContractBroker
from ..core.mixins import AdminAuditableMixin


@admin.register(Company)
class CompanyAdmin(AdminAuditableMixin, ImportExportModelAdmin):
    list_display = ('id', 'name', 'short_name', 'logo', 'created', 'modified', 'created_by', 'modified_by',)
    list_filter = ('created', 'modified', 'created_by', 'modified_by')
    search_fields = ('name',)


class RealEstateSpaceInline(AdminAuditableMixin, admin.TabularInline):
    model = RealEstateSpace


@admin.register(RealEstateProject)
class RealEstateProjectAdmin(AdminAuditableMixin, admin.ModelAdmin):
    list_display = (
        'id', 'name', 'short_name', 'company', 'logo', 'created', 'modified', 'created_by', 'modified_by',
    )
    list_filter = (
        'company',
        'created_by',
        'modified_by',

    )
    inlines = (RealEstateSpaceInline,)
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super(RealEstateProjectAdmin, self).get_queryset(request)
        return qs.select_related('company', 'created_by', 'modified_by')


@admin.register(RealEstateSpace)
class RealEstateSpaceAdmin(AdminAuditableMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'project',
        'name',
        'space_type',
        'area',
        'price',
        'contract',
        'created',
        'modified',
        'created_by',
        'modified_by',
    )
    list_filter = (
        'project',
        'contract',
    )
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super(RealEstateSpaceAdmin, self).get_queryset(request)
        return qs.select_related('project', 'created_by', 'modified_by')


@admin.register(Client)
class ClientAdmin(AdminAuditableMixin, ImportExportModelAdmin):
    list_display = ('id', 'first_name', 'middle_name', 'last_name', 'sex', 'national_id', 'national_id_type',
                    'country_for_id', 'picture', 'date_of_birth', 'full_name', 'client_type', 'created', 'modified',
                    'created_by', 'modified_by',)
    list_filter = (
        'created',
        'modified',
        'date_of_birth',
        'created_by',
        'modified_by',
    )
    search_fields = ('full_name',)


@admin.register(Broker)
class BrokerAdmin(AdminAuditableMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'middle_name',
        'last_name',
        'sex',
        'national_id',
        'national_id_type',
        'country_for_id',
        'picture',
        'date_of_birth',
        'full_name',
        'client_type',
        'created',
        'modified',
        'created_by',
        'modified_by',
    )
    list_filter = (
        'created',
        'modified',
        'date_of_birth',
        'created_by',
        'modified_by',
    )
    search_fields = ('full_name',)


@admin.register(Contract)
class ContractAdmin(AdminAuditableMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'project',
        'broker',
        'created',
        'modified',
        'created_by',
        'modified_by',

    )
    list_filter = (
        'broker',
        'project',
        'created',
        'modified',
        'created_by',
        'modified_by',
        'date',
    )
    # inlines = (RealEstateSpaceInline,)


@admin.register(ContractClient)
class ContractClientAdmin(AdminAuditableMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'created_by',
        'modified_by',
        'client',
        'contract',
        'is_principal',
    )
    list_filter = (
        'created',
        'modified',
        'created_by',
        'modified_by',
        'client',
        'contract',
        'is_principal',
    )


@admin.register(ContractBroker)
class ContractBrokerAdmin(AdminAuditableMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'broker',
        'contract',
        'is_active',
        'created',
        'modified',
        'created_by',
        'modified_by',
    )
    list_filter = (
        'broker',
        'contract',
        'is_active',
    )
