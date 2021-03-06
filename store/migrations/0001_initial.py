# Generated by Django 3.1 on 2020-12-12 06:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import store.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('entry_date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vendor_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Restock',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('restock_no', models.CharField(blank=True, default=store.models.increment_restock_no, max_length=500, null=True, unique=True)),
                ('item_name', models.CharField(max_length=200)),
                ('item_description', models.TextField(blank=True, null=True)),
                ('stock_code', models.CharField(max_length=200)),
                ('unit', models.CharField(choices=[('Ream', 'Ream'), ('PC', 'PC'), ('Pkt', 'Pkt'), ('Booklet', 'Booklet'), ('Roll', 'Roll'), ('Bottle', 'Bottle'), ('Yard', 'Yard'), ('Sheet', 'Sheet'), ('Pad', 'Pad'), ('Tab', 'Tab'), ('Tin', 'Tin'), ('Pack', 'Pack')], max_length=100)),
                ('quantity_ordered', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('quantity_received', models.IntegerField()),
                ('received_on', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='item_category', to='store.category')),
                ('received_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='received_by', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.vendor')),
            ],
            options={
                'ordering': ['-received_on'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=200)),
                ('item_description', models.TextField(blank=True, null=True)),
                ('stock_code', models.CharField(max_length=200, unique=True)),
                ('unit', models.CharField(choices=[('Ream', 'Ream'), ('PC', 'PC'), ('Pkt', 'Pkt'), ('Booklet', 'Booklet'), ('Roll', 'Roll'), ('Bottle', 'Bottle'), ('Yard', 'Yard'), ('Sheet', 'Sheet'), ('Pad', 'Pad'), ('Tab', 'Tab'), ('Tin', 'Tin'), ('Pack', 'Pack')], max_length=100)),
                ('quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('re_order_no', models.IntegerField()),
                ('item_image', models.ImageField(blank=True, upload_to='%Y/%m/%d/')),
                ('entry_date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('below_re_order_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('unavailable_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='default_category', to='store.category')),
                ('entered_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.vendor')),
            ],
            options={
                'ordering': ['-entry_date'],
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('requisition_no', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('requisition_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('quantity_requested', models.IntegerField()),
                ('quantity_issued', models.IntegerField()),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('issued_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='issuing_staff', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='store.item')),
                ('requesting_staff', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='requesting_staff', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-issue_date'],
                'unique_together': {('requisition_no', 'requesting_staff'), ('requisition_no', 'item')},
            },
        ),
    ]
