# Generated by Django 3.1 on 2020-12-13 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        ('rrbnstaff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='store.item'),
            preserve_default=False,
        ),
    ]