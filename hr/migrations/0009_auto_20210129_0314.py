# Generated by Django 3.1 on 2021-01-29 03:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hr', '0008_auto_20210128_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='last_name',
        ),
        migrations.AddField(
            model_name='employee',
            name='staff_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.CharField(blank=True, choices=[('Monitoring', 'Monitoring'), ('Registrations', 'Registrations'), ('Institute', 'Institute'), ('Hr', 'HR'), ('Procurement', 'Procurement'), ('Finance', 'Finance'), ('Audit', 'Audit'), ('ICT', 'ICT'), ('Stores', 'Stores'), ('Protocol', 'PR & Protocol'), ('Registrars Office', 'Registrars Office'), ('Zonal Office ', 'Zonal Office')], max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='pension_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employee',
            name='profile_creation_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employee',
            name='qualification',
            field=models.CharField(blank=True, choices=[('OND', 'OND'), ('HND', 'HND'), ('B.Sc', 'B.Sc'), ('M.Sc', 'M.Sc'), ('BA', 'BA'), ('MD', 'MD'), ('LLB', 'LLB'), ('Ph.D', 'Ph.D'), ('MBA', 'MBA'), ('PROF', 'PROF')], max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='zone',
            field=models.CharField(blank=True, choices=[('HQ', 'HQ'), ('Lagos Zonal Office ', 'Lagos Zonal Office'), ('Lagos CERT-RADMIRS', 'Lagos CERT-RADMIRS'), ('Asaba', 'Asaba'), ('Enugu', 'Enugu'), ('Port Harcourt', 'Port Harcourt'), ('Kano', 'Kano'), ('Sokoto', 'Sokoto'), ('Nnewi', 'Nnewi'), ('Calabar', 'Calabar')], max_length=120, null=True),
        ),
    ]