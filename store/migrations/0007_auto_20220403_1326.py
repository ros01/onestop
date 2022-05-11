# Generated by Django 3.1 on 2022-04-03 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_auto_20220403_0755'),
        ('store', '0006_requisitionitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.department'),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='requisition_cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.requisitioncart'),
        ),
        migrations.AlterField(
            model_name='requisitioncartitem',
            name='requisition_cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.requisitioncart'),
        ),
    ]
