from django.db import models
from datetime import datetime
from datetime import date
import uuid
from django.conf import settings
from django.urls import reverse
from store.models import Item

 
# Create your models here.
def increment_requisition_no():
	last_requisition_no = Requisition.objects.all().order_by('requisition_no').last()
	if not last_requisition_no:
		return '1000'
	requisition_no = last_requisition_no.requisition_no
	new_requisition_no = str(int(requisition_no) + 1)
	new_requisition_no = requisition_no[0:-(len(new_requisition_no))] + new_requisition_no
	return new_requisition_no

def increment_request_no():
	last_request_no = Request.objects.all().order_by('request_no').last()
	if not last_request_no:
		return '1000'
	request_no = last_request_no.request_no
	new_request_no = str(int(request_no) + 1)
	new_request_no = request_no[0:-(len(new_request_no))] + new_request_no
	return new_request_no


class RequisitionItem(models.Model):
	requisition = models.ForeignKey("Requisition", on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
	quantity = models.PositiveIntegerField(default=1)
	line_item_total = models.PositiveIntegerField(default=1)
	
	def __str__(self):
		return self.item.item_name


	def remove(self):
		return self.item.remove_from_requisition()

	#def remove(self):
		#return self.item.remove_from_cart()

class Requisition(models.Model):
	#id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	requisition_no = models.CharField(max_length=500, null=True, blank=True, 
        default=increment_requisition_no)
	#item_name = models.CharField(max_length=200)
	#item_name = models.ForeignKey('store.Item', related_name='store_item', on_delete=models.DO_NOTHING)
	items = models.ManyToManyField(Item, through=RequisitionItem)
	#quantity_requested = models.IntegerField()
	requisition_reason = models.TextField(blank=True, null=True)
	requesting_staff = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING)
	authorized_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_by', null=True, on_delete=models.DO_NOTHING)
	department = models.CharField(max_length=200, null=True)
	requisition_date = models.DateField(auto_now_add=True, auto_now=False)
	requisition_status = models.IntegerField(default=1)

	def __str__(self):
		return str(self.requisition_no)
	

	def get_absolute_url(self):
		return reverse("store:requisition_details", kwargs={"id": self.id})

		
	class Meta:
		unique_together = ('requisition_no','requesting_staff')
		ordering = ["-requisition_date"]

REQUEST_DURATION_CHOICES = (
	('1 day', '1 day'),
	('2 days', '2 days'),
	('3 days', '3 days'),
	('4 days', '4 days'),
	('1 week', '1 week'),
	('2 weeks', '2 weeks'),
)


class Request(models.Model):
	#id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	request_no = models.CharField(max_length=500, null=True, blank=True, unique=True,
        default=increment_request_no)
	vehicle_name = models.CharField(max_length=200)
	department = models.CharField(max_length=200)
	request_reason = models.TextField()
	destination = models.CharField(max_length=200)
	request_duration = models.CharField(max_length=120, choices=REQUEST_DURATION_CHOICES, default='1 day')
	requesting_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
	request_date = models.DateField(auto_now_add=True, auto_now=False)
	projected_start_date = models.DateField(default=date.today)
	projected_end_date = models.DateField(default=date.today)
	request_status = models.IntegerField(default=1)
	

	def __str__(self):
		return self.request_no


	class Meta:
		unique_together = ('request_no','requesting_staff')
		ordering = ["-request_date"]




	
