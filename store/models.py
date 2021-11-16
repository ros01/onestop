from django.db import models
import uuid
from django.conf import settings
from datetime import datetime
from datetime import date
from django.utils import timezone
from .choices import UNIT_OF_MEASUREMENT
from multiselectfield import MultiSelectField
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse



def increment_restock_no():
    last_restock_no = Restock.objects.all().order_by('restock_no').last()
    if not last_restock_no:
        return '1000'
    restock_no = last_restock_no.restock_no
    new_restock_no = str(int(restock_no) + 1)
    new_restock_no = restock_no[0:-(len(new_restock_no))] + new_restock_no
    return new_restock_no

class Vendor(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    description = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return self.vendor_name

    def date_created_pretty(self):
        return self.date_created.strftime('%b %e %Y')

    class Meta:
        ordering = ["-date_created"]

class Item(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length=200)
    item_description = models.TextField()
    #requisition = models.ForeignKey(Requisition, related_name='items_requisition',  on_delete=models.DO_NOTHING)
    category = models.ForeignKey('Category', related_name='default_category', null=True,  on_delete=models.DO_NOTHING)
    stock_code = models.CharField(max_length=200, unique=True)
    vendor = models.ForeignKey('Vendor', null=True, on_delete=models.DO_NOTHING)
    unit = models.CharField(max_length=100, choices = UNIT_OF_MEASUREMENT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=20)
    re_order_no = models.IntegerField()
    item_image = models.ImageField(upload_to='%Y/%m/%d/', blank=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    entry_date = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)
    below_re_order_date = models.DateField(default=date.today, blank=True)
    unavailable_date = models.DateField(default=date.today, blank=True)
    
    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def get_absolute_url(self):
        return reverse("store:item_detail", kwargs={"pk": self.pk})

    def add_to_requisition(self):
        return "%s?item=%s&qty=1" %(reverse("store:create_item_requisition"), self.id)

    def remove_from_requisition(self):
        return "%s?item=%s&qty=1&delete=True" %(reverse("store:create_item_requisition"), self.id)

    def get_success_url(self):
        return reverse("store:item_detail", kwargs={"id": self.object.id})

    class Meta:
        ordering = ["-entry_date"]
    
class Category(models.Model):
	#id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	category_name = models.CharField(max_length=120, unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	entry_date = models.DateField(auto_now_add=True, auto_now=False)
	updated = models.DateField(auto_now_add=False, auto_now=True)

	def __str__(self):
   		return self.category_name
    
    #class Meta:
        #ordering = ["-entry_date"]



class Issue(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length=200)
    requisition_no = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    requisition_date = models.DateField(default=date.today, blank=True)
    quantity_requested = models.IntegerField()
    requesting_staff = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requesting_staff',  on_delete=models.DO_NOTHING)
    quantity_issued = models.IntegerField()
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='issuing_staff',  on_delete=models.DO_NOTHING)
    issue_date = models.DateField(auto_now_add = True, auto_now = False)
    
    def __str__(self):
        return str(self.quantity_issued)

    class Meta:
       unique_together = (('requisition_no', 'item_name',), ('requisition_no', 'requesting_staff',))
       ordering = ["-issue_date"]


    def requisition_date_pretty(self):
        return self.requisition_date.strftime('%b %e %Y')


    def issue_date_pretty(self):
        return self.issue_date.strftime('%b %e %Y')


    def save(self, *args, **kwargs):
        super(Issue, self).save(*args, **kwargs)
        
        try:
            requisition = Requisition.objects.get(
                requisition_no=self.requisition_no,
                requesting_staff=self.requesting_staff,
                
                )
        except Requisition.DoesNotExist:
            pass
        
       
        if self.id is not None:
            requisition.requisition_status = 2
            requisition.save()


        p = Item.objects.get(item_name=self.item_name)
        p.quantity -= self.quantity_issued
        p.save()
  

class Restock(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restock_no = models.CharField(max_length=500, null=True, blank=True, unique=True, default=increment_restock_no)
    item_name =models.CharField(max_length=200)
    item_description = models.TextField(blank=True, null=True)
    category = models.ForeignKey('Category', related_name='item_category', null=True, blank=True, on_delete=models.DO_NOTHING)
    stock_code = models.CharField(max_length=200)
    vendor = models.ForeignKey('Vendor', null=True, blank=True, on_delete=models.DO_NOTHING)
    unit = models.CharField(max_length=100, choices = UNIT_OF_MEASUREMENT)
    quantity_ordered = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=20)
    quantity_received = models.IntegerField()
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_by',  on_delete=models.DO_NOTHING)
    received_on = models.DateField(default=date.today, blank=True)


    
    def __str__(self):
        return str(self.item_name)

    class Meta:
        ordering = ["-received_on"]


    def received_on_pretty(self):
        return self.received_on.strftime('%b %e %Y')


    def save(self, *args, **kwargs):
        super(Restock, self).save(*args, **kwargs)
        

        p = Item.objects.get(item_name=self.item_name)
        p.quantity += self.quantity_received
        p.save()


        
  
        
           




        




    







    



