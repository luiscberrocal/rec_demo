# Generated by Django 3.0.11 on 2021-01-04 20:50

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Broker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('first_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='First name')),
                ('middle_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='middle name')),
                ('last_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='Last name')),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True, verbose_name='Gender')),
                ('national_id', models.CharField(max_length=50, verbose_name='National id')),
                ('national_id_type', models.CharField(choices=[('NATIONAL_ID', 'National Id'), ('DRIVERS_LICENSE', 'Drivers License'), ('PASSPORT', 'Passport'), ('OTHER', 'Other')], default='NATIONAL_ID', max_length=20, verbose_name='National id type')),
                ('country_for_id', django_countries.fields.CountryField(max_length=2, verbose_name='Country for id')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Picture')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
                ('religion', models.CharField(blank=True, max_length=60, null=True, verbose_name='Religion')),
                ('full_name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Full name')),
                ('client_type', models.CharField(choices=[('N', 'Natural person'), ('J', 'Juridical person')], default='N', max_length=1, verbose_name='Client type')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_broker', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_broker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('first_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='First name')),
                ('middle_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='middle name')),
                ('last_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='Last name')),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True, verbose_name='Gender')),
                ('national_id', models.CharField(max_length=50, verbose_name='National id')),
                ('national_id_type', models.CharField(choices=[('NATIONAL_ID', 'National Id'), ('DRIVERS_LICENSE', 'Drivers License'), ('PASSPORT', 'Passport'), ('OTHER', 'Other')], default='NATIONAL_ID', max_length=20, verbose_name='National id type')),
                ('country_for_id', django_countries.fields.CountryField(max_length=2, verbose_name='Country for id')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Picture')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
                ('religion', models.CharField(blank=True, max_length=60, null=True, verbose_name='Religion')),
                ('full_name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Full name')),
                ('client_type', models.CharField(choices=[('N', 'Natural person'), ('J', 'Juridical person')], default='N', max_length=1, verbose_name='Client type')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_client', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_client', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('short_name', models.CharField(max_length=15, verbose_name='Short name')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Logo')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_company', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_company', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateField(verbose_name='Date')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_contract', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_contract', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RealEstateProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('short_name', models.CharField(max_length=15, verbose_name='Short name')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Logo')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='real_estate_projects', to='real_estate.Company', verbose_name='Company')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_realestateproject', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_realestateproject', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RealEstateSpace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('space_type', models.CharField(choices=[('LIVING', 'Living space'), ('PARKING', 'Parking'), ('STORAGE', 'Storage'), ('OTHER', 'Other')], default='LIVING', max_length=8, verbose_name='Space type')),
                ('area', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6, verbose_name='Area')),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, verbose_name='Price')),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='real_estate_spaces', to='real_estate.Contract', verbose_name='Contract')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_realestatespace', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_realestatespace', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='real_estate_spaces', to='real_estate.RealEstateProject', verbose_name='Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContractClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_principal', models.BooleanField(default=True, verbose_name='Is principal')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_clients', to='real_estate.Client', verbose_name='Client')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_clients', to='real_estate.Contract', verbose_name='Contract')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_contractclient', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_contractclient', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContractBroker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('broker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_brokers', to='real_estate.Broker', verbose_name='Broker')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_brokers', to='real_estate.Contract', verbose_name='Contract')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_contractbroker', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_contractbroker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
