# Generated by Django 3.1 on 2020-12-19 19:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrbnstaff', '0005_auto_20201219_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='projected_end_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='request',
            name='projected_start_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
