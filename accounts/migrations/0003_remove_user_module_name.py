# Generated by Django 3.1 on 2021-02-12 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201212_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='module_name',
        ),
    ]