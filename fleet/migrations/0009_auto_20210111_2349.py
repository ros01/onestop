# Generated by Django 3.1 on 2021-01-11 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0008_auto_20201231_2103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='maintenance',
            options={'ordering': ['-schedule_no']},
        ),
    ]
