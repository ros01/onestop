# Generated by Django 3.1 on 2020-12-15 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrbnstaff', '0003_auto_20201214_0817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requisition',
            name='item',
        ),
        migrations.AddField(
            model_name='requisition',
            name='item_name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
