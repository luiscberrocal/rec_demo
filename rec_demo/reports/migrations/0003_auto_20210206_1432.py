# Generated by Django 3.1.6 on 2021-02-06 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20210206_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='task_id',
            field=models.CharField(max_length=128, verbose_name='Task id'),
        ),
    ]