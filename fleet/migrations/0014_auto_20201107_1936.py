# Generated by Django 3.1 on 2020-11-07 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0013_assign_trip_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='driver',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
