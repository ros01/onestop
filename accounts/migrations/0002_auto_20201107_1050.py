# Generated by Django 3.1 on 2020-11-07 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.CharField(blank=True, choices=[('Monitoring', 'Monitoring'), ('Registrations', 'Registrations'), ('Hr', 'Hr'), ('Procurement', 'Procurement'), ('Finance', 'Finance'), ('Audit', 'Audit'), ('ICT', 'ICT'), ('Stores', 'Stores'), ('Institute', 'Institute'), ('Protocol', 'PR & Protocol')], max_length=30, null=True),
        ),
    ]
