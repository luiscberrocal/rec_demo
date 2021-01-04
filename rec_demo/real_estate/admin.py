# -*- coding: utf-8 -*-
from django.contrib import admin

from .forms import CompanyForm
from .models import Company, RealEstateProject, RealEstateSpace, Client, Broker, Contract, ContractClient, \
    ContractBroker
from ..core.mixins import AdminAuditableMixin


@admin.register(Company)
class CompanyAdmin(AdminAuditableMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'short_name',
        'logo',
        'created',
        'modified',
        'created_by',
        'modified_by',
    )
    list_filter = ('created', 'modified', 'created_by', 'modified_by')
    search_fields = ('name',)


class RealEstateSpaceInline(AdminAuditableMixin, admin.TabularInline):
    model = RealEstateSpace

@admin.register(RealEstateProject)
class RealEstateProjectAdmin(AdminAuditableMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'short_name',
        'company',
        'logo',
        'created',
        'modified',
        'created_by',
        'modified_by',
    )
    list_filter = (
        'company',
        'created_by',
        'modified_by',

    )
    inlines = (RealEstateSpaceInline,)
    search_fields = ('name',)


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


@admin.register(Client)
class ClientAdmin(AdminAuditableMixin, admin.ModelAdmin):
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
        'religion',
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
        'religion',
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


@admin.register(Contract)
class ContractAdmin(AdminAuditableMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'created_by',
        'modified_by',
        'date',
    )
    list_filter = (
        'created',
        'modified',
        'created_by',
        'modified_by',
        'date',
    )


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
