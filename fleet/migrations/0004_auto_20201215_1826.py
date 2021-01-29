# Generated by Django 3.1 on 2020-12-15 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0003_auto_20201212_1927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assign',
            old_name='end_date',
            new_name='approved_end_date',
        ),
        migrations.RenameField(
            model_name='assign',
            old_name='start_date',
            new_name='approved_start_date',
        ),
        migrations.RenameField(
            model_name='release',
            old_name='end_date',
            new_name='actual_trip_end_date',
        ),
        migrations.RenameField(
            model_name='release',
            old_name='start_date',
            new_name='actual_trip_start_date',
        ),
        migrations.RemoveField(
            model_name='assign',
            name='current_mileage',
        ),
    ]