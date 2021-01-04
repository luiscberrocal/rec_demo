# -*- coding: utf-8 -*-
from django.contrib import admin

from .forms import CompanyForm
from .models import Company, RealEstateProject, RealEstateSpace, Client, Broker, Contract, ContractClient, \
    ContractBroker


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
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
    readonly_fields = ['created_by', 'modified_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)



@admin.register(RealEstateProject)
class RealEstateProjectAdmin(admin.ModelAdmin):
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
    search_fields = ('name',)


@admin.register(RealEstateSpace)
class RealEstateSpaceAdmin(admin.ModelAdmin):
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
class ClientAdmin(admin.ModelAdmin):
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
class BrokerAdmin(admin.ModelAdmin):
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
class ContractAdmin(admin.ModelAdmin):
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
class ContractClientAdmin(admin.ModelAdmin):
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
class ContractBrokerAdmin(admin.ModelAdmin):
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
