# Generated by Django 3.1 on 2022-04-25 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20220423_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='stock_code',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
