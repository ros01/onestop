# Generated by Django 3.1 on 2022-04-03 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_auto_20220403_0755'),
        ('store', '0007_auto_20220403_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hr.department'),
        ),
    ]
