# Generated by Django 3.0.11 on 2021-01-21 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('type', models.CharField(max_length=1, verbose_name='Type')),
                ('date', models.DateField(verbose_name='Date')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Amount')),
                ('comments', models.CharField(blank=True, max_length=60, null=True, verbose_name='Comments')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Due date')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='banking.Account', verbose_name='Account')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_transaction', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_transaction', to=settings.AUTH_USER_MODEL)),
                ('related_debit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credits', to='banking.Transaction', verbose_name='Related debit')),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='banking.TransactionType', verbose_name='Type')),
            ],
            options={
                'ordering': ('date',),
            },
        ),
    ]
