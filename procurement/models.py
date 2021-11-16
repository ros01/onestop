from django.db import models
import uuid
from django.conf import settings
from datetime import datetime
from datetime import date

# Create your models here.

def increment_contract_no():
    last_contract_no = Contract.objects.all().order_by('contract_no').last()
    if not last_contract_no:
        return '0000'
    contract_no = last_contract_no.contract_no
    new_contract_no = str(int(contract_no) + 1)
    new_contract_no = contract_no[0:-(len(new_contract_no))] + new_contract_no
    return new_contract_no

class Category(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank = False, null = False)
    added_on = models.DateField(default=date.today)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_category_added_by', on_delete=models.DO_NOTHING)
    

    def __str__(self):
        return self.category_name


class Vendor(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    description = models.TextField(blank = False, null = False)
    date_created = models.DateField(default=date.today)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_vendor_added_by', on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.vendor_name

    def date_created_pretty(self):
        return self.date_created.strftime('%b %e %Y')

    class Meta:
        ordering = ["-date_created"]



class Contract(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract_no = models.CharField(max_length=500, null=True, blank=True, unique=True, 
        default=increment_contract_no)
    contract_name = models.CharField(max_length=200)
    contract_description = models.TextField(blank = False, null = False)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.DO_NOTHING)
    vendor = models.ForeignKey('Vendor', null=True, blank=True, on_delete=models.DO_NOTHING)
    contact_award_date = models.DateField(default=date.today)
    contact_award_amount = models.DecimalField(max_digits=50, decimal_places=2,)
    projected_start_date = models.DateField(default=date.today)
    projected_end_date = models.DateField(default=date.today)
    contract_status = models.CharField(max_length=200, default="Awarded")
    contract_award_letter = models.FileField(upload_to='%Y/%m/%d/', blank=True)
    vendor_proposal = models.FileField(upload_to='%Y/%m/%d/', blank=True)
    date_added = models.DateField(default=date.today)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contract_added_by',on_delete=models.DO_NOTHING)

    class Meta:
       ordering = ['-date_added']

    def __str__(self):
        return self.contract_name


class Project(models.Model):

    CONTRACT_STATUS = (
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Abandoned', 'Abandoned'),
        )


    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract_no = models.CharField(max_length=200)
    contract_name = models.CharField(max_length=200)
    contract_description = models.TextField(blank = False, null = False)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.DO_NOTHING)
    vendor = models.ForeignKey('Vendor', null=True, blank=True, on_delete=models.DO_NOTHING)
    contact_award_date = models.DateField(default=date.today)
    contact_award_amount = models.DecimalField(max_digits=50, decimal_places=2,)
    projected_start_date = models.DateField(default=date.today)
    projected_end_date = models.DateField(default=date.today)
    start_date = models.DateField(default=date.today)
    completion_date = models.DateField(null=True, blank=True)
    contract_status = models.CharField(max_length=120, choices=CONTRACT_STATUS,  null=True, blank=True)
    performance_rating = models.IntegerField()
    remarks = models.TextField(blank = False, null = False)
    date_documented = models.DateField(default=date.today)
    documented_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_documented_by',on_delete=models.DO_NOTHING)

    class Meta:
       ordering = ['-date_documented']

    def __str__(self):
        return self.contract_name



