# Generated by Django 3.0.11 on 2021-01-13 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0005_auto_20210112_1413'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broker',
            name='religion',
        ),
        migrations.RemoveField(
            model_name='client',
            name='religion',
        ),
    ]
