# Generated by Django 3.1 on 2020-11-06 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrbnstaff', '0003_auto_20201105_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='request_status',
            field=models.IntegerField(default=1),
        ),
    ]
