# Generated by Django 3.1 on 2020-12-22 00:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrbnstaff', '0009_auto_20201221_2357'),
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
