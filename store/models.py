from django.db import models
import uuid
from django.conf import settings
from datetime import datetime
from datetime import date
from django.utils import timezone
from accounts.choices import *
from .choices import UNIT_OF_MEASUREMENT
from multiselectfield import MultiSelectField
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render, redirect
User = settings.AUTH_USER_MODEL
# User = get_user_model()
from hr.models import Employee, Department
import datetime



def increment_requisition_no():
    last_requisition_no = RequisitionCart.objects.all().order_by('requisition_no').last()
    if not last_requisition_no:
        return '1000'
    requisition_no = last_requisition_no.requisition_no
    new_requisition_no = str(int(requisition_no) + 1)
    new_requisition_no = requisition_no[0:-(len(new_requisition_no))] + new_requisition_no
    return new_requisition_no



def increment_restock_no():
    last_restock_no = RestockCart.objects.all().order_by('restock_no').last()
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


class Category(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=120, unique=True)
    category_short = models.CharField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    entry_date = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.category_name
 

class Item(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length=200)
    item_description = models.TextField()
    #requisition = models.ForeignKey(Requisition, related_name='items_requisition',  on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, related_name='default_category', null=True,  on_delete=models.DO_NOTHING)
    stock_code = models.CharField(max_length=500, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.DO_NOTHING)
    unit = models.CharField(max_length=100, choices = UNIT_OF_MEASUREMENT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=20)
    re_order_no = models.IntegerField()
    item_image = models.ImageField(upload_to='%Y/%m/%d/', blank=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)
    below_re_order_date = models.DateField(default=date.today, blank=True)
    unavailable_date = models.DateField(default=date.today, blank=True)
    
    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return self.item.get_absolute_url()

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


    @property
    def imageURL(self):
        try:
            url = self.item_image.url
        except:
            url = ''
        return url




class RequisitionCart(models.Model):
    employee = models.ForeignKey(User, related_name='requisition_created_by', blank=True, on_delete=models.DO_NOTHING)
    requisition_date = models.DateField(auto_now_add=True, auto_now=False)
    requisition_status = models.IntegerField(default=1)
    requisition_no = models.CharField(max_length=500, null=True, blank=True, 
        default=increment_requisition_no)

    def __str__(self):
        return str(self.requisition_no)

    # def get_absolute_url(self):
    #     return reverse("store:requisition_details", kwargs={"id": self.id})
        
    @property
    def get_requisition_cart_total(self):
        requisitionCartItems = self.requisitioncartitem_set.all()
        total = sum([item.get_total for item in requisitionCartItems])
        return total 

    @property
    def get_requisition_cart_items(self):
        requisitionCartItems = self.requisitioncartitem_set.all()
        total = sum([item.quantity for item in requisitionCartItems])
        return total 

    @property
    def get_requisition_cart_items_qs(self):
        requisitionCartItems = self.requisitioncartitem_set.all()
        return requisitionCartItems 

    def get_requisition_item_quantity(self):
        item_quantity = 0
        items = self.requisitioncartitem_set.all()
        for item in items:
            item_quantity += item.quantity_issued
            return item_quantity
        
    def get_inventory_item(self):
        requisitioncartitem = []
        items = self.requisitioncartitem_set.all()
        for item in items:
            requisitioncartitem = item.item
            return requisitioncartitem

        
    def get_cartitems(self):
        items = self.requisitioncartitem_set.all()
        return items

    
class RequisitionCartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    requisition_cart = models.ForeignKey(RequisitionCart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    quantity_issued = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    # def __str__(self):
    #     return self.item.item_name
    
    def __str__(self):
        return str(self.requisition_cart.requisition_no)


    def remove(self):
        return self.item.remove_from_requisition()   

class Requisition(models.Model):
    # employee = models.ForeignKey(Employee, related_name='requested_by', blank=True, on_delete=models.DO_NOTHING)
    employee = models.CharField(max_length=200, null=True, blank=True)
    requisition_cart = models.ForeignKey(RequisitionCart, on_delete=models.CASCADE)
    requisition_reason = models.TextField(blank=True)
    # hod = models.ForeignKey(Employee, related_name='approved_by', blank=True, on_delete=models.DO_NOTHING)
    hod =models.CharField(max_length=200, null=True, blank=True)
    # department = models.ForeignKey(Department, blank=True, on_delete=models.DO_NOTHING)
    department = models.CharField (max_length=30, choices = DEPARTMENT,  null=True, blank=True)
    requisition_creation_date = models.DateField(auto_now_add=True, auto_now=False)
    requisition_status = models.IntegerField(default=1)

    def __str__(self):
        return str(self.requisition_cart.requisition_no)



class IssueRequisition(models.Model):
    # employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    #quantity_issued = models.IntegerField(default=0, null=True, blank=True)
    issued_by = models.ForeignKey(User, related_name='issuing_staff',  on_delete=models.DO_NOTHING)
    issue_date = models.DateField(default=date.today, blank=True)
    
    # def __str__(self):
    #     return str(self.requisition)    

    def __str__(self):
        return str(self.requisition.requisition_cart.requisition_no)
   
    def save(self, *args, **kwargs):
        super(IssueRequisition, self).save(*args, **kwargs)
        try:
            requisition = Requisition.objects.get(
                requisition_cart=self.requisition.requisition_cart.requisition_no)
                # requesting_staff=self.requisition.requesting_staff,      
        except Requisition.DoesNotExist:
            pass
       
        if self.id is not None:
            self.requisition.requisition_status = 2
            self.requisition.save()

    
@receiver(post_save, sender=IssueRequisition)
def update_item_quantity_on_save(sender, instance, created, *args, **kwargs):
    issuerequisition = instance
    item_quantity = 0
    cart_items = issuerequisition.requisition.requisition_cart.requisitioncartitem_set.all()
    for item in cart_items:
        item_quantity =+ item.quantity_issued
        item.item.quantity -= item_quantity
        if item.item.quantity:
            p = Item.objects.get(item_name=item.item)
            p.quantity -= item_quantity 
            p.save()


# def issue_requisition_receiver(sender, instance, created, *args, **kwargs):
#     issuerequisition = instance
#     item_quantity = 0
#     cart_items = issuerequisition.requisition.requisition_cart.requisitioncartitem_set.all()
#     for item in cart_items:
#         item_quantity =+ item.quantity_issued
#         item.item.quantity -= item_quantity
#         item.quantity -= item_quantity
#         item.save()
#         print(item.item)
#         print(item.item.quantity)
# post_save.connect(issue_requisition_receiver, sender=IssueRequisition)



   

class RestockCart(models.Model):
    staff_name = models.ForeignKey(User, related_name='restock_created_by', blank=True, on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now_add=True, auto_now=False)
    restock_no = models.CharField(max_length=500, null=True, blank=True, 
        default=increment_restock_no)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.restock_no)

    # def get_absolute_url(self):
    #     return reverse("store:requisition_details", kwargs={"id": self.id})
        
    @property
    def get_restock_cart_total(self):
        restockCartItems = self.restockcartitem_set.all()
        total = sum([item.get_total for item in restockCartItems])
        return total 

    @property
    def get_restock_cart_items(self):
        restockCartItems = self.restockcartitem_set.all()
        total = sum([item.qty for item in restockCartItems])
        return total 

    @property
    def get_restock_cart_items_qs(self):
        restockCartItems = self.restockcartitem_set.all()
        return restockCartItems 

    def get_restock_item_quantity(self):
        item_quantity = 0
        items = self.restockcartitem_set.all()
        for item in items:
            item_quantity += item.quantity_issued
            return item_quantity
        
    def get_inventory_item(self):
        restockcartitem = []
        items = self.restockcartitem_set.all()
        for item in items:
            restockcartitem = item.item
            return restockcartitem

        
    def get_cartitems(self):
        items = self.restockcartitem_set.all()
        return items

    
class RestockCartItem(models.Model):
    item_name = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey('Vendor', null=True, blank=True, on_delete=models.DO_NOTHING)
    restock_cart = models.ForeignKey(RestockCart, on_delete=models.CASCADE, null=True)
    unit_price = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    qty = models.IntegerField(default=0, null=True, blank=True)
    quantity_ordered = models.IntegerField(default=0, null=True, blank=True)
    quantity_received = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('item_name','restock_cart')
    
  
    @property
    def get_total(self):
        if self.unit_price:
            total = self.unit_price * self.quantity_received
            return total
        else:
            return self.qty

    
    def __str__(self):
        return str(self.restock_cart.restock_no)


    def save(self, *args, **kwargs):
        super(RestockCartItem, self).save(*args, **kwargs)

        if self.unit_price:
            p = Item.objects.get(item_name=self.item_name)
            p.quantity += self.quantity_received
            p.vendor = self.vendor
            p.unit_price = self.unit_price
            p.save()






        




    







    



