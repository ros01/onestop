# Generated by Django 3.1 on 2020-11-05 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0005_auto_20201105_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='category',
            field=models.CharField(blank=True, choices=[('Pool Vehicle', 'Pool Vehicle'), ('Departmental Vehicle', 'Departmental Vehicle')], max_length=120, null=True),
        ),
    ]
