# Generated by Django 3.1.6 on 2021-02-06 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('created',)},
        ),
        migrations.AddField(
            model_name='report',
            name='url',
            field=models.URLField(blank=True, max_length=256, null=True, verbose_name='Url'),
        ),
        migrations.AlterField(
            model_name='report',
            name='metadata',
            field=models.JSONField(blank=True, null=True, verbose_name='Metadata'),
        ),
    ]