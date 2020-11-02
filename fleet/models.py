from django.db import models
import uuid
from django.conf import settings
from hr.models import Driver

# Create your models here.


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    vehicle_type = models.CharField(max_length=200)
    categories = models.ManyToManyField('Category', blank=True)
    engine_number = models.CharField(max_length=200)
    chasis_number = models.CharField(max_length=200)
    colour = models.CharField(max_length=200)
    unit_assigned = models.CharField(max_length=200)
    license_no = models.CharField(max_length=200)
    insurance_details = models.CharField(max_length=200)
    

    
    def __str__(self):
        return self.vehicle_name

    #def get_absolute_url(self):
		#return reverse("item_detail", kwargs={"pk": self.pk})

	#class Meta:
		#ordering = ["-title"]

#class ItemImage(models.Model):
	#product = models.ForeignKey(Item)
	#image = models.ImageField(upload_to=image_upload_to)

	#def __str__(self):
		#return self.product.title


class Category(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	#def __str__(self):
        #return self.title

	def get_absolute_url(self):
		return reverse("category_detail", kwargs={"slug": self.slug })



class Requisition(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	vehicle_name = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.DO_NOTHING)
	driver_name = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.DO_NOTHING)
	purpose = models.TextField(null=True, blank=True)
	destination = models.CharField(max_length=200)
	requisition_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applying_staff', on_delete=models.DO_NOTHING)
	department = models.CharField(max_length=200)
	departure_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	return_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	timeount = models.DateTimeField(auto_now_add=True, auto_now=False)
	timein = models.DateTimeField(auto_now_add=True, auto_now=False)
	authorised_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='deparment_hod', on_delete=models.DO_NOTHING)



class Fueling(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	vehicle_name = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.DO_NOTHING)
	driver_name = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.DO_NOTHING)
	current_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	fuel_input = models.IntegerField()
	fuel_cost = models.DecimalField(max_digits=50, decimal_places=2,)
	station_name = models.CharField(max_length=200)
	authorised_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='protocol_hod', on_delete=models.DO_NOTHING)
	fueling_date = models.DateTimeField(auto_now_add=True, auto_now=False)


class Repair(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	fault = models.CharField(max_length=200)
	reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reported_by', on_delete=models.DO_NOTHING)
	verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='verified_by', on_delete=models.DO_NOTHING)
	driver_name = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.DO_NOTHING)
	current_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	repair_details = models.CharField(max_length=200)
	repair_cost = models.DecimalField(max_digits=50, decimal_places=2,)
	workshop_name = models.CharField(max_length=200)
	mechanic_name = models.CharField(max_length=200)
	repair_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	

class Maintenance(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	last_maintenance_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	maintenance_due_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	maintenance_approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
	last_maintenance_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	current_mileage = models.DecimalField(max_digits=50, decimal_places=2,)
	workshop_name = models.CharField(max_length=200)
	mechanic_name = models.CharField(max_length=200)
	maintenance_cost = models.DecimalField(max_digits=50, decimal_places=2,)
	next_maintenance_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	remarks = models.TextField(null=True, blank=True)
	driver_name = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.DO_NOTHING)
	
	





