# Generated by Django 3.1 on 2022-05-11 07:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fleet.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workshop_name', models.CharField(max_length=200)),
                ('mechanic_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('entered_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('vehicle_type', models.CharField(blank=True, choices=[('Sedan', 'Sedan'), ('Bus', 'Bus'), ('Truck', 'Truck'), ('Van', 'Van'), ('Wagon', 'Wagon'), ('SUV', 'SUV')], max_length=120, null=True)),
                ('model', models.CharField(max_length=200)),
                ('purchase_year', models.CharField(max_length=200)),
                ('location', models.CharField(choices=[('HQ', 'HQ'), ('Lagos Zonal Office ', 'Lagos Zonal Office'), ('Lagos CERT-RADMIRS', 'Lagos CERT-RADMIRS'), ('Asaba', 'Asaba'), ('Enugu', 'Enugu'), ('Port Harcourt', 'Port Harcourt'), ('Kano', 'Kano'), ('Sokoto', 'Sokoto'), ('Nnewi', 'Nnewi'), ('Calabar', 'Calabar')], max_length=120)),
                ('interstate_trip', models.CharField(choices=[('local', 'Local Trip'), ('interstate', 'Interstate Trip')], default='interstate', max_length=120)),
                ('category', models.CharField(blank=True, choices=[('Pool Vehicle', 'Pool Vehicle'), ('Departmental Vehicle', 'Departmental Vehicle'), ('Zonal Office Vehicle', 'Zonal Office Vehicle')], max_length=120, null=True)),
                ('engine_number', models.CharField(max_length=200)),
                ('chasis_number', models.CharField(max_length=200)),
                ('colour', models.CharField(blank=True, choices=[('White', 'White'), ('Grey', 'Grey'), ('Red', 'Red'), ('Blue', 'Blue'), ('Black', 'Black'), ('Brown', 'Brown'), ('Custom', 'Custom')], max_length=120, null=True)),
                ('department_assigned', models.CharField(blank=True, choices=[('Monitoring', 'Monitoring'), ('Registrations', 'Registrations'), ('Institute', 'Institute'), ('Hr', 'HR'), ('Procurement', 'Procurement'), ('Finance', 'Finance'), ('Audit', 'Audit'), ('ICT', 'ICT'), ('Stores', 'Stores'), ('Protocol', 'PR & Protocol'), ('Registrars Office', 'Registrars Office'), ('Zonal Office ', 'Zonal Office')], max_length=120, null=True)),
                ('private_license_no', models.CharField(max_length=200)),
                ('official_license_no', models.CharField(max_length=200)),
                ('insurance_details', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('trip_status', models.IntegerField(default=1)),
                ('entered_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['vehicle_name'],
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(max_length=200)),
                ('contact_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('station_credit', models.DecimalField(decimal_places=2, max_digits=20)),
                ('re_order_credit', models.DecimalField(decimal_places=2, max_digits=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('entered_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fault', models.TextField(blank=True, null=True)),
                ('reported_by', models.CharField(max_length=200)),
                ('driver', models.CharField(max_length=200)),
                ('current_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('repair_details', models.TextField(blank=True, null=True)),
                ('repair_cost', models.DecimalField(decimal_places=2, max_digits=50)),
                ('repair_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('authorised_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='protocol_officer', to=settings.AUTH_USER_MODEL)),
                ('mechanic_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='mechanic', to='fleet.workshop')),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.vehicle')),
                ('workshop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.workshop')),
            ],
        ),
        migrations.CreateModel(
            name='Refill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refill_no', models.CharField(blank=True, default=fleet.models.increment_refill_no, max_length=500, null=True, unique=True)),
                ('station_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('station_credit', models.DecimalField(decimal_places=2, max_digits=20)),
                ('refill_credit_value', models.DecimalField(decimal_places=2, max_digits=20)),
                ('refill_on', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('refill_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='refill_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-refill_on'],
            },
        ),
        migrations.CreateModel(
            name='Fueling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver', models.CharField(max_length=200)),
                ('voucher_no', models.CharField(blank=True, max_length=500, null=True)),
                ('current_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('fuel_input', models.IntegerField()),
                ('fuel_cost', models.DecimalField(decimal_places=2, max_digits=50)),
                ('fueling_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('authorised_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='protocol_hod', to=settings.AUTH_USER_MODEL)),
                ('station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.station')),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('entered_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_no', models.CharField(blank=True, default=fleet.models.increment_schedule_no, max_length=500, null=True)),
                ('target_maintenance_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('target_maintenance_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('schedule_status', models.IntegerField(default=1)),
                ('scheduled_on', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('maintenance_scheduled_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='maintenance_scheduler', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.vehicle')),
            ],
            options={
                'ordering': ['-scheduled_on'],
                'unique_together': {('schedule_no', 'vehicle')},
            },
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_name', models.CharField(max_length=200)),
                ('request_no', models.CharField(max_length=200)),
                ('request_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('department', models.CharField(max_length=200)),
                ('driver', models.CharField(max_length=200)),
                ('approved_start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('approved_end_date', models.DateTimeField(default=datetime.datetime.now)),
                ('actual_trip_start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('actual_trip_end_date', models.DateTimeField(default=datetime.datetime.now)),
                ('trip_start_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('trip_end_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('release_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('released_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='protocol_staff', to=settings.AUTH_USER_MODEL)),
                ('requesting_staff', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='request_staff', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-release_date'],
                'unique_together': {('request_no', 'requesting_staff'), ('request_no', 'vehicle_name')},
            },
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_no', models.CharField(blank=True, default=fleet.models.increment_schedule_no, max_length=500, null=True)),
                ('driver', models.CharField(max_length=200)),
                ('target_maintenance_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('target_maintenance_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('scheduled_on', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('current_mileage', models.DecimalField(decimal_places=2, max_digits=50)),
                ('maintenance_cost', models.DecimalField(decimal_places=2, max_digits=50)),
                ('maintenance_details', models.TextField(blank=True, null=True)),
                ('maintenance_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('maintenance_recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='maintenance_recorded_by', to=settings.AUTH_USER_MODEL)),
                ('maintenance_scheduled_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('mechanic_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='maintenance_mechanic', to='fleet.workshop')),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.vehicle')),
                ('workshop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fleet.workshop')),
            ],
            options={
                'ordering': ['-schedule_no'],
                'unique_together': {('schedule_no', 'vehicle')},
            },
        ),
        migrations.CreateModel(
            name='Assign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_no', models.CharField(max_length=200)),
                ('vehicle_name', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('request_reason', models.TextField(blank=True, null=True)),
                ('destination', models.CharField(max_length=200)),
                ('request_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('driver', models.CharField(max_length=200)),
                ('issue_status', models.IntegerField(default=1)),
                ('trip_status', models.CharField(choices=[('created', 'Created'), ('completed', 'Completed')], default='created', max_length=120)),
                ('projected_start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('projected_end_date', models.DateTimeField(default=datetime.datetime.now)),
                ('approved_start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('approved_end_date', models.DateTimeField(default=datetime.datetime.now)),
                ('approved_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='assigning_staff', to=settings.AUTH_USER_MODEL)),
                ('requesting_staff', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='applying_staff', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-request_no'],
                'unique_together': {('request_no', 'requesting_staff'), ('request_no', 'vehicle_name')},
            },
        ),
    ]
