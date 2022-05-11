from django.db import models
from datetime import datetime
from datetime import date
import uuid
from django.conf import settings
from django.urls import reverse
from store.models import Item

 
# Create your models here.


def increment_request_no():
	last_request_no = Request.objects.all().order_by('request_no').last()
	if not last_request_no:
		return '1000'
	request_no = last_request_no.request_no
	new_request_no = str(int(request_no) + 1)
	new_request_no = request_no[0:-(len(new_request_no))] + new_request_no
	return new_request_no




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
		# unique_together = ('request_no','requesting_staff')
		ordering = ["-request_date"]




	
