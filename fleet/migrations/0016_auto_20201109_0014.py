# Generated by Django 3.1 on 2020-11-09 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0015_auto_20201107_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fueling',
            name='driver',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='driver',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='repair',
            name='driver',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
