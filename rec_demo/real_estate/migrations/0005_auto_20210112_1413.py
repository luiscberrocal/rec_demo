# Generated by Django 3.0.11 on 2021-01-12 19:13

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('real_estate', '0004_auto_20210110_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='down_payment',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, verbose_name='Down payment'),
        ),
        migrations.AddField(
            model_name='contract',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, verbose_name='Total amount'),
        ),
        migrations.CreateModel(
            name='SalesType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=60, verbose_name='Name')),
                ('short_name', models.CharField(max_length=20, unique=True, verbose_name='Short name')),
                ('requires_loan', models.BooleanField(default=False, verbose_name='Requires loan')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_salestype', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_salestype', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contract',
            name='sales_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contracts', to='real_estate.SalesType', verbose_name='Sales type'),
        ),
    ]
