# Generated by Django 4.0.1 on 2022-03-11 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0025_organizations_access_right'),
    ]

    operations = [
        migrations.AddField(
            model_name='il_info',
            name='Mlab',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='il_info',
            name='Ushauri',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='il_info',
            name='air',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
