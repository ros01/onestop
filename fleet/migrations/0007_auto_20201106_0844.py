# Generated by Django 3.1 on 2020-11-06 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0006_auto_20201105_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assign',
            name='driver',
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
    ]
