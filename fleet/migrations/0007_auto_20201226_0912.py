# Generated by Django 3.1 on 2020-12-26 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0006_auto_20201225_0834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='mechanic_name',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='workshop',
        ),
    ]