# Generated by Django 3.1 on 2020-11-09 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0018_auto_20201109_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair',
            name='mechanic_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='mechanic', to='fleet.workshop'),
        ),
    ]
