from django.db import models
from datetime import datetime
import uuid
from django.conf import settings
from django.urls import reverse



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


class Requisition(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	requisition_no = models.CharField(max_length=500, null=True, blank=True, 
        default=increment_requisition_no)
	item = models.ForeignKey("store.Item", null=True, blank=True, on_delete=models.DO_NOTHING)
	quantity_requested = models.IntegerField()
	requesting_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
	department = models.CharField(max_length=200)
	requisition_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	requisition_status = models.IntegerField(default=1)

	def __str__(self):
		return self.requisition_no

	def requisition_date_pretty(self):
		return self.requisition_date.strftime('%b %e %Y')

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
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	request_no = models.CharField(max_length=500, null=True, blank=True, 
        default=increment_request_no)
	vehicle = models.ForeignKey("fleet.Vehicle", null=True, blank=True, on_delete=models.DO_NOTHING)
	department = models.CharField(max_length=200)
	request_reason = models.TextField(blank=True, null=True)
	destination = models.CharField(max_length=200)
	request_duration = models.CharField(max_length=120, choices=REQUEST_DURATION_CHOICES, default='1 day')
	requesting_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
	request_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	trip_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	request_status = models.IntegerField(default=1)

	def __str__(self):
		return self.request_no

	def request_date_pretty(self):
		return self.request_date.strftime('%b %e %Y')

	def trip_date_pretty(self):
		return self.trip_date.strftime('%b %e %Y')

	class Meta:
		unique_together = ('request_no','requesting_staff')
		ordering = ["-request_date"]




	
