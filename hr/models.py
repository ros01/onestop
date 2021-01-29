from django.db import models
import uuid
from django.conf import settings
from datetime import datetime

# Create your models here.

class Employee(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ) 

    BLOOD_GROUP = (
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
        ) 

    MARITAL_STATUS = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ) 

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
        ('Registrars Office', 'Registrars Office'),
        ('Zonal Office ', 'Zonal Office'),
        )   

    ZONE = (
        ('HQ', 'HQ'),
        ('Lagos Zonal Office ', 'Lagos Zonal Office'),
        ('Lagos CERT-RADMIRS', 'Lagos CERT-RADMIRS'),
        ('Asaba', 'Asaba'),
        ('Enugu', 'Enugu'),
        ('Port Harcourt', 'Port Harcourt'),
        ('Kano', 'Kano'),
        ('Sokoto', 'Sokoto'),
        ('Nnewi', 'Nnewi'),
        ('Calabar', 'Calabar'),
        )

    QUALIFICATION = (
        ('OND', 'OND'),
        ('HND', 'HND'),
        ('B.Sc', 'B.Sc'),
        ('M.Sc', 'M.Sc'),
        ('BA', 'BA'),
        ('MD', 'MD'),
        ('LLB', 'LLB'),
        ('Ph.D', 'Ph.D'),
        ('MBA', 'MBA'),
        ('PROF', 'PROF'),
        )


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    dob = models.DateTimeField(default=datetime.now, blank=True)
    gender = models.CharField(max_length=120, choices=GENDER,  null=True, blank=True)
    marital_status = models.CharField(max_length=120, choices=MARITAL_STATUS,  null=True, blank=True)
    next_of_kin = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    zone = models.CharField(max_length=120, choices=ZONE,  null=True, blank=True)
    department = models.CharField(max_length=120, choices=DEPARTMENT,  null=True, blank=True)
    designation = models.ForeignKey('Title', null=True, blank=True, on_delete=models.DO_NOTHING)
    pay_grade = models.ForeignKey('Grade', null=True, blank=True, on_delete=models.DO_NOTHING)
    national_id = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100)
    contact_address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    state_of_origin = models.CharField(max_length=100)
    local_government_area = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=datetime.now, blank=True)
    pension_date = models.DateTimeField(default=datetime.now, blank=True)
    qualification = models.CharField(max_length=120, choices=QUALIFICATION,  null=True, blank=True)
    languages = models.CharField(max_length=100)
    professional_organizations = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=120, choices=BLOOD_GROUP,  null=True, blank=True)
    drivers_license = models.ImageField(upload_to='%Y/%m/%d/', blank=True)
    digital_passport = models.ImageField(upload_to='%Y/%m/%d/', blank=True)
    special_interests = models.TextField(blank=True)
    hobbies = models.TextField(blank=True)
    profile_creation_date = models.DateTimeField(default=datetime.now, blank=True)

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def dob_pretty(self):
        return self.dob.strftime('%b %e %Y')

    def date_joined_pretty(self):
        return self.date_joined.strftime('%b %e %Y')

    def pension_date_pretty(self):
        return self.pension_date.strftime('%b %e %Y')

    def profile_creation_date_pretty(self):
        return self.profile_creation_date.strftime('%b %e %Y')
    
    def __str__(self):
        return self.full_name

class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200) 
    designation = models.CharField(max_length=200)  

class Title(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_title = models.CharField(max_length=200)
    description = models.TextField(blank=True) 
    date_added = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.job_title)


class Grade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pay_grade_name = models.CharField(max_length=200)
    paygrade_description = models.TextField(blank=True, null=True)
    pay_grade_code = models.CharField(max_length=200, unique=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)


    def date_created_pretty(self):
        return self.date_created.strftime('%b %e %Y')

    def __str__(self):
        return str(self.pay_grade_name)


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
    
    def __str__(self):
        return str(self.reviewer)

class Leave(models.Model):

    LEAVE_CHOICES = (
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('examination', 'Examination Leave'),
        ('maternity', 'Maternity Leave'),
        ('compassionate', 'Compassionate Leave'),
        )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)
    leave_type = models.CharField(max_length=120, choices=LEAVE_CHOICES, blank=False)
    leave_compliance = models.CharField(max_length=200)
    start_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    end_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.status)
    

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
    



