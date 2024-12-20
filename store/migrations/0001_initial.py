# Generated by Django 3.1 on 2024-02-08 12:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=120, unique=True)),
                ('category_short', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('entry_date', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=200)),
                ('item_description', models.TextField()),
                ('stock_code', models.CharField(blank=True, max_length=500, null=True)),
                ('unit', models.CharField(choices=[('Ream', 'Ream'), ('PC', 'PC'), ('Pkt', 'Pkt'), ('Booklet', 'Booklet'), ('Roll', 'Roll'), ('Bottle', 'Bottle'), ('Yard', 'Yard'), ('Sheet', 'Sheet'), ('Pad', 'Pad'), ('Tab', 'Tab'), ('Tin', 'Tin'), ('Pack', 'Pack')], max_length=100)),
                ('quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('re_order_no', models.IntegerField()),
                ('item_image', models.ImageField(blank=True, upload_to='%Y/%m/%d/')),
                ('entry_date', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('below_re_order_date', models.DateField(blank=True, default=datetime.date.today)),
                ('unavailable_date', models.DateField(blank=True, default=datetime.date.today)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='default_category', to='store.category')),
                ('entered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-entry_date'],
            },
        ),
        migrations.CreateModel(
            name='RequisitionCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requisition_date', models.DateField(auto_now_add=True)),
                ('requisition_status', models.IntegerField(default=1)),
                ('requisition_no', models.CharField(blank=True, default=store.models.increment_requisition_no, max_length=500, null=True)),
                ('employee', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='requisition_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RestockCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('restock_no', models.CharField(blank=True, default=store.models.increment_restock_no, max_length=500, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('staff_name', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='restock_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='RequisitionCartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('quantity_issued', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.item')),
                ('requisition_cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.requisitioncart')),
            ],
        ),
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.CharField(blank=True, max_length=200, null=True)),
                ('requisition_reason', models.TextField(blank=True)),
                ('hod', models.CharField(blank=True, max_length=200, null=True)),
                ('department', models.CharField(blank=True, choices=[('Monitoring', 'Monitoring'), ('Registrations', 'Registrations'), ('Hr', 'Hr'), ('Procurement', 'Procurement'), ('Finance', 'Finance'), ('Audit', 'Audit'), ('ICT', 'ICT'), ('Stores', 'Stores'), ('Protocol', 'PR & Protocol'), ('Registrars Office', 'Registrars Office')], max_length=30, null=True)),
                ('requisition_creation_date', models.DateField(auto_now_add=True)),
                ('requisition_status', models.IntegerField(default=1)),
                ('requisition_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.requisitioncart')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.vendor'),
        ),
        migrations.CreateModel(
            name='IssueRequisition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(blank=True, default=datetime.date.today)),
                ('issued_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='issuing_staff', to=settings.AUTH_USER_MODEL)),
                ('requisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.requisition')),
            ],
        ),
        migrations.CreateModel(
            name='RestockCartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('qty', models.IntegerField(blank=True, default=0, null=True)),
                ('quantity_ordered', models.IntegerField(blank=True, default=0, null=True)),
                ('quantity_received', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('item_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.item')),
                ('restock_cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.restockcart')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.vendor')),
            ],
            options={
                'unique_together': {('item_name', 'restock_cart')},
            },
        ),
    ]
