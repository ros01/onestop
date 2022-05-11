# Generated by Django 3.1 on 2022-01-27 21:12

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import rrbnstaff.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_no', models.CharField(blank=True, default=rrbnstaff.models.increment_request_no, max_length=500, null=True, unique=True)),
                ('vehicle_name', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('request_reason', models.TextField()),
                ('destination', models.CharField(max_length=200)),
                ('request_duration', models.CharField(choices=[('1 day', '1 day'), ('2 days', '2 days'), ('3 days', '3 days'), ('4 days', '4 days'), ('1 week', '1 week'), ('2 weeks', '2 weeks')], default='1 day', max_length=120)),
                ('request_date', models.DateField(auto_now_add=True)),
                ('projected_start_date', models.DateField(default=datetime.date.today)),
                ('projected_end_date', models.DateField(default=datetime.date.today)),
                ('request_status', models.IntegerField(default=1)),
                ('requesting_staff', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-request_date'],
            },
        ),
    ]
