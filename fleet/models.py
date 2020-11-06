from django.db import models
import uuid
from django.conf import settings
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Station(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    station_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return self.station_name

    def date_created_pretty(self):
        return self.date_created.strftime('%b %e %Y')


class Workshop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workshop_name = models.CharField(max_length=200)
    mechanic_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)


    class Meta:
        ordering = ["-date_created"]
    
    def __str__(self):
        return self.vendor_name

    def date_created_pretty(self):
        return self.date_created.strftime('%b %e %Y')

class Category(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	category_name = models.CharField(max_length=120, unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
	date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
	

	def __str__(self):
		return self.category_name

	def date_created_pretty(self):
		return self.date_created.strftime('%b %e %Y')

	#def get_absolute_url(self):
		#return reverse("category_detail", kwargs={"id": self.id })

class Vehicle(models.Model):

	DEPARTMENT = (
        ('Monitoring', 'Monitoring'),
        ('Registrations', 'Registrations'),
        ('Hr', 'Hr'),
        ('Procurement', 'Procurement'),
        ('Finance', 'Finance'),
        ('Audit', 'Audit'),
        ('ICT', 'ICT'),
        ('Stores', 'Stores'),
        ('Protocol', 'Protocol'),
        )

	TYPE = (
        ('Sedan', 'Sedan'),
        ('Bus', 'Bus'),
        ('Truck', 'Truck'),
        ('Van', 'Van'),
        ('Wagon', 'Wagon'),
        )

	COLOUR = (
		('White', 'White'),
		('Grey', 'Grey'),
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Black', 'Black'),
        ('Brown', 'Brown'),
        ('Custom', 'Custom'),
        )

	CATEGORY = (
		('Pool Vehicle', 'Pool Vehicle'),
		('Departmental Vehicle', 'Departmental Vehicle'),
        )

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	vehicle_name = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	vehicle_type = models.CharField(max_length=120, choices=TYPE,  null=True, blank=True)
	category = models.CharField(max_length=120, choices=CATEGORY,  null=True, blank=True)
	engine_number = models.CharField(max_length=200)
	chasis_number = models.CharField(max_length=200)
	colour = models.CharField(max_length=120, choices=COLOUR,  null=True, blank=True)
	department_assigned = models.CharField(max_length=120, choices=DEPARTMENT,  null=True, blank=True)
	license_no = models.CharField(max_length=200)
	insurance_details = models.CharField(max_length=200)
	entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
	date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.vehicle_name

	def date_created_pretty(self):
		return self.date_created.strftime('%b %e %Y')

    

class Assign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_no = models.CharField(max_length=200)
    vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.DO_NOTHING)
    requesting_staff = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applying_staff',  on_delete=models.DO_NOTHING)
    department = models.CharField(max_length=200)
    request_reason = models.TextField(blank=True, null=True)
    destination = models.CharField(max_length=200)
    request_date = models.DateTimeField(default=datetime.now, blank=True)
    #driver = models.ForeignKey("hr.Driver", null=True, blank=True, on_delete=models.DO_NOTHING)
    driver =  models.CharField(max_length=200)
    issue_status = models.IntegerField(default=1)
    current_mileage = models.DecimalField(max_digits=50, decimal_places=2)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    end_date = models.DateTimeField(default=datetime.now, blank=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigning_staff',  on_delete=models.DO_NOTHING)
    approved_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.request_no


    def save(self, *args, **kwargs):
        super(Assign, self).save(*args, **kwargs)
        
        try:
            request = Request.objects.get(
                request_no=self.request_no,
                requesting_staff=self.requesting_staff,
                
                )
        except Request.DoesNotExist:
            pass
        
       
        if self.id is not None:
            request.request_status = 2
            request.save()




class Release(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.DO_NOTHING)
    request_no = models.CharField(max_length=200)
    request_date = models.DateTimeField(default=datetime.now, blank=True)
    requesting_staff = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='request_staff',  on_delete=models.DO_NOTHING)
    department = models.CharField(max_length=200)
    driver = models.ForeignKey("hr.Driver", null=True, blank=True, on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    end_date = models.DateTimeField(default=datetime.now, blank=True)
    trip_start_mileage = models.DecimalField(max_digits=50, decimal_places=2)
    trip_end_mileage = models.DecimalField(max_digits=50, decimal_places=2)
    released_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='protocol_staff',  on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.request_no

class Fueling(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.DO_NOTHING)
	driver = models.ForeignKey("hr.Driver", null=True, blank=True, on_delete=models.DO_NOTHING)
	current_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	fuel_input = models.IntegerField()
	fuel_cost = models.DecimalField(max_digits=50, decimal_places=2,)
	station = models.ForeignKey('Station', null=True, blank=True, on_delete=models.DO_NOTHING)
	authorised_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='protocol_hod', on_delete=models.DO_NOTHING)
	fueling_date = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.vehicle


class Repair(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.DO_NOTHING)
	fault = models.CharField(max_length=200)
	reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reported_by', on_delete=models.DO_NOTHING)
	verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='verified_by', on_delete=models.DO_NOTHING)
	driver = models.ForeignKey("hr.Driver", null=True, blank=True, on_delete=models.DO_NOTHING)
	current_mileage = models.DecimalField(max_digits=50, decimal_places=2)
	repair_details = models.TextField(blank=True, null=True)
	repair_cost = models.DecimalField(max_digits=50, decimal_places=2)
	workshop = models.ForeignKey('Workshop', null=True, blank=True, on_delete=models.DO_NOTHING)
	mechanic_name = models.CharField(max_length=200)
	repair_date = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.vehicle
	

class Maintenance(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.DO_NOTHING)
	last_maintenance_date = models.DateTimeField(default=datetime.now, blank=True)
	maintenance_due_date = models.DateTimeField(default=datetime.now, blank=True)
	maintenance_approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
	last_maintenance_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	driver = models.ForeignKey("hr.Driver", null=True, blank=True, on_delete=models.DO_NOTHING)
	current_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	workshop = models.ForeignKey('Workshop', null=True, blank=True, on_delete=models.DO_NOTHING)
	mechanic_name = models.CharField(max_length=200)
	maintenance_cost = models.DecimalField(max_digits=50, decimal_places=2,)
	next_maintenance_date = models.DateTimeField(default=datetime.now, blank=True)
	remarks = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.vehicle
	
	





