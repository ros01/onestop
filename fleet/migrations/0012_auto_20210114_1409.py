# Generated by Django 3.1 on 2021-01-14 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0011_auto_20210111_2356'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='release',
            options={'ordering': ['-release_date']},
        ),
    ]
