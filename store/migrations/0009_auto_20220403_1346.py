# Generated by Django 3.1 on 2022-04-03 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_auto_20220403_0755'),
        ('store', '0008_auto_20220403_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='requested_by', to='hr.employee'),
        ),
    ]
