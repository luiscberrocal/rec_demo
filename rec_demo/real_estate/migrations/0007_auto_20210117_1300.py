# Generated by Django 3.0.11 on 2021-01-17 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0001_initial'),
        ('real_estate', '0006_auto_20210113_1812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broker',
            name='client_type',
        ),
        migrations.AddField(
            model_name='broker',
            name='broker_type',
            field=models.CharField(choices=[('N', 'Natural person'), ('J', 'Juridical person')], default='N', max_length=1, verbose_name='Broker type'),
        ),
        migrations.AddField(
            model_name='contract',
            name='account',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contract', to='banking.Account', verbose_name='Account'),
        ),
    ]