# Generated by Django 3.1.6 on 2021-02-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0002_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
