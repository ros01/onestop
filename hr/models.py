from django.db import models
import uuid
from django.conf import settings

# Create your models here.

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    dob = models.DateTimeField(auto_now_add=True, auto_now=False)
    gender = models.CharField(max_length=200)
    marital_status = models.CharField(max_length=100)
    next_of_kin = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    department = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    national_id = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100)
    contact_address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    state_of_origin = models.CharField(max_length=100)
    local_government_area = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True, auto_now=False)
    pension_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    qualiification = models.CharField(max_length=100)
    languages = models.CharField(max_length=100)
    professional_organizations = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=100)
    drivers_license = models.ImageField(upload_to='%Y/%m/%d/', blank=True)
    digital_passport = models.ImageField(upload_to='%Y/%m/%d/', blank=True)
    special_interests = models.TextField(blank=True)
    hobbies = models.TextField(blank=True)


    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


    
    def __str__(self):
        return self.full_name

class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200) 
    designation = models.CharField(max_length=200)  


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    line_manager = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True, auto_now=False)



class Performance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_performance_review = models.DateTimeField(auto_now_add=True, auto_now=False)
    performance_review_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    next_performance_review = models.DateTimeField(auto_now_add=True, auto_now=False)
    performance_notes = models.TextField(blank=True)
    rate = models.IntegerField()
    reviewer = models.CharField(max_length=100)
    comments = models.TextField(blank=True)
    

class Leave(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)
    leave_type = models.CharField(max_length=200)
    leave_compliance = models.CharField(max_length=200)
    start_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    end_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    

class Learning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training_name = models.CharField(max_length=200)
    training_venue = models.CharField(max_length=200)
    training_vendor = models.CharField(max_length=200)
    training_objectives = models.TextField(blank=True)
    staff_names = models.TextField(blank=True)
    unit = models.CharField(max_length=200)
    grade = models.CharField(max_length=200)
    training_cost = models.DecimalField(max_digits=50, decimal_places=2,)
    start_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    end_date = models.DateTimeField(auto_now_add=True, auto_now=False)

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    



