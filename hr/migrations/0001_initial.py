# Generated by Django 3.1 on 2024-02-08 12:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hr.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appraisal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appraisal_name', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField()),
                ('added_on', models.DateField(default=datetime.date.today)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='appraisal_added_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField()),
                ('added_on', models.DateField(default=datetime.date.today)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='category_added_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('designation', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('dob', models.DateField(default=datetime.date.today)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=120, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('Single', 'Single'), ('Married', 'Married')], max_length=120, null=True)),
                ('next_of_kin', models.CharField(max_length=100)),
                ('nationality', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('zone', models.CharField(blank=True, choices=[('HQ', 'HQ'), ('Lagos Zonal Office ', 'Lagos Zonal Office'), ('Lagos CERT-RADMIRS', 'Lagos CERT-RADMIRS'), ('Asaba', 'Asaba'), ('Enugu', 'Enugu'), ('Port Harcourt', 'Port Harcourt'), ('Kano', 'Kano'), ('Sokoto', 'Sokoto'), ('Nnewi', 'Nnewi'), ('Calabar', 'Calabar')], max_length=120, null=True)),
                ('national_id', models.CharField(max_length=100)),
                ('staff_id', models.CharField(max_length=100)),
                ('contact_address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('state_of_origin', models.CharField(max_length=100)),
                ('local_government_area', models.CharField(max_length=100)),
                ('date_joined', models.DateField(default=datetime.date.today)),
                ('pension_date', models.DateField(default=datetime.date.today)),
                ('qualification', models.CharField(blank=True, choices=[('OND', 'OND'), ('HND', 'HND'), ('B.Sc', 'B.Sc'), ('M.Sc', 'M.Sc'), ('BA', 'BA'), ('MD', 'MD'), ('LLB', 'LLB'), ('Ph.D', 'Ph.D'), ('MBA', 'MBA'), ('PROF', 'PROF')], max_length=120, null=True)),
                ('languages', models.CharField(max_length=100)),
                ('professional_organizations', models.CharField(max_length=100)),
                ('blood_group', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], max_length=120, null=True)),
                ('drivers_license', models.ImageField(blank=True, upload_to='%Y/%m/%d/')),
                ('digital_passport', models.ImageField(blank=True, upload_to='%Y/%m/%d/')),
                ('special_interests', models.TextField(blank=True)),
                ('hobbies', models.TextField()),
                ('profile_creation_date', models.DateField(default=datetime.date.today)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.department')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('description', models.TextField()),
                ('date_created', models.DateField(default=datetime.date.today)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='vendor_added_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_no', models.CharField(blank=True, default=hr.models.increment_training_no, max_length=500, null=True, unique=True)),
                ('training_name', models.CharField(max_length=200)),
                ('training_description', models.CharField(max_length=200)),
                ('projected_start_date', models.DateField(default=datetime.date.today)),
                ('projected_end_date', models.DateField(default=datetime.date.today)),
                ('training_venue', models.CharField(max_length=200)),
                ('training_budget', models.DecimalField(decimal_places=2, max_digits=50)),
                ('training_status', models.CharField(default='Scheduled', max_length=200)),
                ('date_added', models.DateField(default=datetime.date.today)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='training_added_by', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.category')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department_tr', to='hr.department')),
                ('employee', models.ManyToManyField(related_name='employee_tr', to='hr.Employee')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.vendor')),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_no', models.CharField(max_length=200)),
                ('training_name', models.CharField(max_length=200)),
                ('training_description', models.CharField(max_length=200)),
                ('projected_start_date', models.DateField(default=datetime.date.today)),
                ('projected_end_date', models.DateField(default=datetime.date.today)),
                ('training_venue', models.CharField(max_length=200)),
                ('training_budget', models.DecimalField(decimal_places=2, max_digits=50)),
                ('training_start_date', models.DateField(default=datetime.date.today)),
                ('training_end_date', models.DateField(default=datetime.date.today)),
                ('training_cost', models.DecimalField(decimal_places=2, max_digits=50)),
                ('training_status', models.CharField(default='Concluded', max_length=200)),
                ('date_recorded', models.DateField(default=datetime.date.today)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.category')),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='record_added_by', to=settings.AUTH_USER_MODEL)),
                ('staff_name', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_grade_name', models.CharField(max_length=200)),
                ('paygrade_description', models.TextField()),
                ('pay_grade_code', models.CharField(max_length=200, unique=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='designation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.title'),
        ),
        migrations.AddField(
            model_name='employee',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employee',
            name='pay_grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.grade'),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_name', models.CharField(max_length=200)),
                ('training_description', models.CharField(max_length=200)),
                ('date_added', models.DateField(default=datetime.date.today)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='course_added_by', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.category')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.vendor')),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Specify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_no', models.CharField(max_length=200)),
                ('leave_type', models.CharField(max_length=200)),
                ('leave_application_date', models.DateField(default=datetime.date.today)),
                ('requested_start_date', models.DateField(default=datetime.date.today)),
                ('requested_end_date', models.DateField(default=datetime.date.today)),
                ('approved_start_date', models.DateField(default=datetime.date.today)),
                ('approved_end_date', models.DateField(default=datetime.date.today)),
                ('comments', models.TextField()),
                ('approved_date', models.DateField(default=datetime.date.today)),
                ('leave_status', models.CharField(default='Leave Days Assigned', max_length=200)),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='approving_staff', to=settings.AUTH_USER_MODEL)),
                ('staff_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='staff', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-request_no'],
                'unique_together': {('request_no', 'staff_name')},
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_no', models.CharField(blank=True, default=hr.models.increment_schedule_no, max_length=500, null=True, unique=True)),
                ('appraisal_due_date', models.DateField(default=datetime.date.today)),
                ('projected_start_date', models.DateField(default=datetime.date.today)),
                ('projected_end_date', models.DateField(default=datetime.date.today)),
                ('appraisal_status', models.CharField(default='Scheduled', max_length=200)),
                ('appraisal_scheduled_on', models.DateField(default=datetime.date.today)),
                ('appraisal', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='appraisal_type', to='hr.appraisal')),
                ('appraisal_scheduled_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='appraisal_scheduler', to=settings.AUTH_USER_MODEL)),
                ('staff_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-appraisal_scheduled_on'],
                'unique_together': {('schedule_no', 'staff_name')},
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_no', models.CharField(max_length=200)),
                ('appraisal_due_date', models.DateField(default=datetime.date.today)),
                ('projected_start_date', models.DateField(default=datetime.date.today)),
                ('projected_end_date', models.DateField(default=datetime.date.today)),
                ('appraisal_start_date', models.DateField(default=datetime.date.today)),
                ('appraisal_end_date', models.DateField(default=datetime.date.today)),
                ('appraisal_status', models.CharField(default='Appraised', max_length=200)),
                ('comments', models.TextField()),
                ('score', models.IntegerField()),
                ('documented_on', models.DateField(default=datetime.date.today)),
                ('appraisal', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='appraisal', to='hr.appraisal')),
                ('appraised_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='appraiser', to=settings.AUTH_USER_MODEL)),
                ('staff_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-documented_on'],
                'unique_together': {('schedule_no', 'staff_name')},
            },
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_no', models.CharField(blank=True, default=hr.models.increment_request_no, max_length=500, null=True, unique=True)),
                ('requested_start_date', models.DateField(default=datetime.date.today)),
                ('requested_end_date', models.DateField(default=datetime.date.today)),
                ('leave_type', models.CharField(choices=[('Annual Leave', 'Annual Leave'), ('Sick Leave', 'Sick Leave'), ('Casual Leave', 'Casual Leave'), ('Examination Leave', 'Examination Leave'), ('Maternity Leave', 'Maternity Leave'), ('Compassionate Leave', 'Compassionate Leave'), ('Leave on Urgent Matter', 'Leave on Urgent Matter'), ('Leave of Absence', 'Leave of Absence'), ('Study Leave With Pay', 'Study Leave With Pay'), ('Study Leave Without Pay', 'Study Leave Without Pay'), ('Sabatical Leave', 'Sabatical Leave')], max_length=120)),
                ('leave_status', models.CharField(default='Pending Approval', max_length=200)),
                ('leave_application_date', models.DateField(default=datetime.date.today)),
                ('approved_on', models.DateField(auto_now=True)),
                ('staff_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-request_no'],
                'unique_together': {('request_no', 'staff_name')},
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_no', models.CharField(max_length=200)),
                ('leave_type', models.CharField(max_length=200)),
                ('leave_application_date', models.DateField(default=datetime.date.today)),
                ('requested_start_date', models.DateField(default=datetime.date.today)),
                ('requested_end_date', models.DateField(default=datetime.date.today)),
                ('approved_start_date', models.DateField(default=datetime.date.today)),
                ('approved_end_date', models.DateField(default=datetime.date.today)),
                ('actual_start_date', models.DateField(default=datetime.date.today)),
                ('actual_end_date', models.DateField(default=datetime.date.today)),
                ('comments', models.TextField()),
                ('entry_date', models.DateField(default=datetime.date.today)),
                ('leave_status', models.CharField(default='Leave Completed', max_length=200)),
                ('documented_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='leave_entry_by', to=settings.AUTH_USER_MODEL)),
                ('staff_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-request_no'],
                'unique_together': {('request_no', 'staff_name')},
            },
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_no', models.CharField(blank=True, default=hr.models.increment_case_no, max_length=500, null=True, unique=True)),
                ('case_name', models.CharField(max_length=200)),
                ('case_description', models.TextField()),
                ('penalty', models.CharField(max_length=200)),
                ('due_date', models.DateField(default=datetime.date.today)),
                ('case_status', models.CharField(default='In Progress', max_length=200)),
                ('assigned_on', models.DateField(default=datetime.date.today)),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='admin_officer', to=settings.AUTH_USER_MODEL)),
                ('staff_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-assigned_on'],
                'unique_together': {('case_no', 'staff_name')},
            },
        ),
        migrations.CreateModel(
            name='Compliance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_no', models.CharField(max_length=200)),
                ('case_name', models.CharField(max_length=200)),
                ('case_description', models.TextField()),
                ('penalty', models.CharField(max_length=200)),
                ('due_date', models.DateField(default=datetime.date.today)),
                ('case_status', models.CharField(choices=[('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=200)),
                ('completed_on', models.DateField(default=datetime.date.today)),
                ('closed_on', models.DateField(default=datetime.date.today)),
                ('closed_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='hr_officer', to=settings.AUTH_USER_MODEL)),
                ('staff_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-closed_on'],
                'unique_together': {('case_no', 'staff_name')},
            },
        ),
    ]
