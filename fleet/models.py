from django.db import models
import uuid
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from rrbnstaff.models import Request


# Create your models here.

def increment_schedule_no():
	last_schedule_no = Schedule.objects.all().order_by('schedule_no').last()
	if not last_schedule_no:
		return '0000'
	schedule_no = last_schedule_no.schedule_no
	new_schedule_no = str(int(schedule_no) + 1)
	new_schedule_no = schedule_no[0:-(len(new_schedule_no))] + new_schedule_no
	return new_schedule_no


class Station(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	station_name = models.CharField(max_length=200)
	contact_name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	phone = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=100, null=True, blank=True)
	station_credit = models.DecimalField(decimal_places=2, max_digits=20)
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
		return self.workshop_name

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
		('Institute', 'Institute'),
		('Hr', 'HR'),
		('Procurement', 'Procurement'),
		('Finance', 'Finance'),
		('Audit', 'Audit'),
		('ICT', 'ICT'),
		('Stores', 'Stores'),
		('Protocol', 'PR & Protocol'),
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

	LOCATION = (
		('HQ', 'HQ'),
		('Lagos', 'Lagos'),
		('Asaba', 'Asaba'),
		('Enugu', 'Enugu'),
		('Port Harcourt', 'Port Harcourt'),
		('Kano', 'Kano'),
		('Sokoto', 'Sokoto'),
		('Nnewi', 'Nnewi'),
		('Calabar', 'Calabar'),
		)

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	vehicle_name = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	vehicle_type = models.CharField(max_length=120, choices=TYPE,  null=True, blank=True)
	model = models.CharField(max_length=200)
	purchase_year = models.CharField(max_length=200)
	location = models.CharField(max_length=120, choices=LOCATION,  null=True, blank=True)
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

	TRIP_STATUS = (
		('created', 'Created'),
		('completed', 'Completed'),
		)

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
	trip_status = models.CharField(max_length=120, choices=TRIP_STATUS, default='created')
	current_mileage = models.DecimalField(max_digits=50, decimal_places=2)
	start_date = models.DateTimeField(default=datetime.now, blank=True)
	end_date = models.DateTimeField(default=datetime.now, blank=True)
	assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigning_staff',  on_delete=models.DO_NOTHING)
	approved_date = models.DateTimeField(default=datetime.now, blank=True)


	class Meta:
	   unique_together = (('request_no', 'vehicle',), ('request_no', 'requesting_staff',))
	   ordering = ["-approved_date"]

	def __str__(self):
		return self.request_no

	def start_date_pretty(self):
		return self.start_date.strftime('%b %e %Y')

	def end_date_pretty(self):
		return self.end_date.strftime('%b %e %Y')

	def request_date_pretty(self):
		return self.request_date.strftime('%b %e %Y')

	def approved_date_pretty(self):
		return self.approved_date.strftime('%b %e %Y')


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
	driver = models.CharField(max_length=200)
	start_date = models.DateTimeField(default=datetime.now, blank=True)
	end_date = models.DateTimeField(default=datetime.now, blank=True)
	trip_start_mileage = models.DecimalField(max_digits=50, decimal_places=2)
	trip_end_mileage = models.DecimalField(max_digits=50, decimal_places=2)
	released_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='protocol_staff',  on_delete=models.DO_NOTHING)
	release_date = models.DateTimeField(default=datetime.now, blank=True)

	class Meta:
	   unique_together = (('request_no', 'vehicle',), ('request_no', 'requesting_staff',))
	   ordering = ["-release_date"]


	def __str__(self):
		return self.request_no

	def save(self, *args, **kwargs):
		super(Release, self).save(*args, **kwargs)
		
		try:
			assign = Assign.objects.get(
				request_no=self.request_no,
				requesting_staff=self.requesting_staff,
				
				)
		except Assign.DoesNotExist:
			pass
		
	   
		if self.id is not None:
			assign.trip_status = "completed"
			assign.save()



class Fueling(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.DO_NOTHING)
	#driver = models.ForeignKey("hr.Driver", null=True, blank=True, on_delete=models.DO_NOTHING)
	driver = models.CharField(max_length=200)
	current_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	fuel_input = models.IntegerField()
	fuel_cost = models.DecimalField(max_digits=50, decimal_places=2,)
	station = models.ForeignKey('Station', null=True, blank=True, on_delete=models.DO_NOTHING)
	authorised_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='protocol_hod', on_delete=models.DO_NOTHING)
	fueling_date = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return str(self.vehicle)

	def fueling_date_pretty(self):
		return self.fueling_date.strftime('%b %e %Y')

	def save(self, *args, **kwargs):
		super(Fueling, self).save(*args, **kwargs)
        
        #try:
            #requisition = Requisition.objects.get(
                #requisition_no=self.requisition_no,
                #requesting_staff=self.requesting_staff,
                
                #)
        #except Requisition.DoesNotExist:
            #pass
        
       
        #if self.id is not None:
            #requisition.requisition_status = 2
            #requisition.save()

		p = Station.objects.get(station_name=self.station)
		p.station_credit -= self.fuel_cost
		p.save()


class Repair(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.DO_NOTHING)
	fault = models.TextField(null=True, blank=True)
	#reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reported_by', on_delete=models.DO_NOTHING)
	#verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='verified_by', on_delete=models.DO_NOTHING)
	#driver = models.ForeignKey("hr.Driver", null=True, blank=True, on_delete=models.DO_NOTHING)
	reported_by = models.CharField(max_length=200)
	driver = models.CharField(max_length=200)
	current_mileage = models.DecimalField(max_digits=50, decimal_places=2)
	repair_details = models.TextField(blank=True, null=True)
	repair_cost = models.DecimalField(max_digits=50, decimal_places=2)
	workshop = models.ForeignKey('Workshop', null=True, blank=True, on_delete=models.DO_NOTHING)
	mechanic_name = models.ForeignKey('Workshop', null=True, blank=True, related_name='mechanic', on_delete=models.DO_NOTHING)
	repair_date = models.DateTimeField(default=datetime.now, blank=True)
	authorised_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='protocol_officer', on_delete=models.DO_NOTHING)

	def __str__(self):
		return str(self.vehicle)

	def repair_date_pretty(self):
		return self.repair_date.strftime('%b %e %Y')

class Schedule(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	schedule_no = models.CharField(max_length=500, null=True, blank=True, 
        default=increment_schedule_no)
	vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.DO_NOTHING)
	current_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	#last_maintenance_date = models.DateTimeField(default=datetime.now, blank=True)
	maintenance_due_date = models.DateTimeField(default=datetime.now, blank=True)
	workshop = models.ForeignKey('Workshop', null=True, blank=True, on_delete=models.DO_NOTHING)
	mechanic_name = models.ForeignKey('Workshop', null=True, blank=True, related_name='workshop_mechanic', on_delete=models.DO_NOTHING)
	#maintenance_cost_estimate = models.DecimalField(max_digits=50, decimal_places=2,)
	#projected_maintenance = models.TextField(null=True, blank=True)
	schedule_status = models.IntegerField(default=1)
	maintenance_scheduled_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='maintenance_scheduler', on_delete=models.DO_NOTHING)
	scheduled_on = models.DateTimeField(default=datetime.now, blank=True)
	
	#driver = models.ForeignKey("hr.Driver", null=True, blank=True, on_delete=models.DO_NOTHING)


	def __str__(self):
		return str(self.vehicle)

	class Meta:
		unique_together = ('schedule_no','vehicle')
		ordering = ["-scheduled_on"]

	def scheduled_on_pretty(self):
		return self.scheduled_on.strftime('%b %e %Y')

	def maintenance_due_date_pretty(self):
		return self.maintenance_due_date.strftime('%b %e %Y')
	

class Maintenance(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	schedule_no = models.CharField(max_length=500, null=True, blank=True, default=increment_schedule_no)
	vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.DO_NOTHING)
	driver = models.CharField(max_length=200)
	#last_maintenance_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	#last_maintenance_date = models.DateTimeField(default=datetime.now, blank=True)
	maintenance_due_date = models.DateTimeField(default=datetime.now, blank=True)
	workshop = models.ForeignKey('Workshop', null=True, blank=True, on_delete=models.DO_NOTHING)
	mechanic_name = models.ForeignKey('Workshop', null=True, blank=True, related_name='maintenance_mechanic', on_delete=models.DO_NOTHING)
	#maintenance_cost_estimate = models.DecimalField(max_digits=50, decimal_places=2,)
	#projected_maintenance = models.TextField(null=True, blank=True)
	maintenance_scheduled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
	scheduled_on = models.DateTimeField(default=datetime.now, blank=True)
	current_maintenance_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	actual_maintenance_cost = models.DecimalField(max_digits=50, decimal_places=2,)
	actual_maintenance_details = models.TextField(null=True, blank=True)
	next_maintenance_date = models.DateTimeField(default=datetime.now, blank=True)
	maintenance_recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='maintenance_recorded_by', on_delete=models.DO_NOTHING)
	actual_maintenance_date = models.DateTimeField(default=datetime.now, blank=True)

	class Meta:
	   unique_together = ('schedule_no', 'vehicle')
	   ordering = ["-actual_maintenance_date"]

	def __str__(self):
		return self.driver

	def save(self, *args, **kwargs):
		super(Maintenance, self).save(*args, **kwargs)
		
		try:
			schedule = Schedule.objects.get(
				schedule_no=self.schedule_no,
				vehicle=self.vehicle,
				
				)
		except Schedule.DoesNotExist:
			pass
		
	   
		if self.id is not None:
			schedule.schedule_status = 2
			schedule.save()
	
	





