# Generated by Django 3.1 on 2020-11-04 17:15

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hr', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('station_name', models.CharField(max_length=200)),
                ('contact_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('workshop_name', models.CharField(max_length=200)),
                ('mechanic_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vehicle_name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('vehicle_type', models.CharField(max_length=200)),
                ('engine_number', models.CharField(max_length=200)),
                ('chasis_number', models.CharField(max_length=200)),
                ('colour', models.CharField(max_length=200)),
                ('unit_assigned', models.CharField(max_length=200)),
                ('license_no', models.CharField(max_length=200)),
                ('insurance_details', models.CharField(max_length=200)),
                ('categories', models.ManyToManyField(blank=True, to='fleet.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fault', models.CharField(max_length=200)),
                ('current_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('repair_details', models.TextField(blank=True, null=True)),
                ('repair_cost', models.DecimalField(decimal_places=2, max_digits=50)),
                ('mechanic_name', models.CharField(max_length=200)),
                ('repair_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.driver')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reported_by', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.vehicle')),
                ('verified_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='verified_by', to=settings.AUTH_USER_MODEL)),
                ('workshop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.workshop')),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('request_no', models.CharField(max_length=200)),
                ('request_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('department', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('end_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('trip_start_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('trip_end_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.driver')),
                ('released_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='protocol_staff', to=settings.AUTH_USER_MODEL)),
                ('requesting_staff', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='request_staff', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('last_maintenance_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('maintenance_due_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('last_maintenance_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('current_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('mechanic_name', models.CharField(max_length=200)),
                ('maintenance_cost', models.DecimalField(decimal_places=2, max_digits=50)),
                ('next_maintenance_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.driver')),
                ('maintenance_approved_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.vehicle')),
                ('workshop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.workshop')),
            ],
        ),
        migrations.CreateModel(
            name='Fueling',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('current_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('fuel_input', models.IntegerField()),
                ('fuel_cost', models.DecimalField(decimal_places=2, max_digits=50)),
                ('fueling_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('authorised_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='protocol_hod', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.driver')),
                ('station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.station')),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('request_no', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('request_reason', models.TextField(blank=True, null=True)),
                ('destination', models.CharField(max_length=200)),
                ('request_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('issue_status', models.IntegerField(default=1)),
                ('current_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('start_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('end_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('approved_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='assigning_staff', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.driver')),
                ('requesting_staff', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='applying_staff', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.vehicle')),
            ],
        ),
    ]
