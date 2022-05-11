from django.db import models
import uuid
from django.conf import settings
from datetime import datetime
from datetime import date
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


def increment_schedule_no():
    last_schedule_no = Schedule.objects.all().order_by('schedule_no').last()
    if not last_schedule_no:
        return '0000'
    schedule_no = last_schedule_no.schedule_no
    new_schedule_no = str(int(schedule_no) + 1)
    new_schedule_no = schedule_no[0:-(len(new_schedule_no))] + new_schedule_no
    return new_schedule_no


def increment_request_no():
    last_request_no = Leave.objects.all().order_by('request_no').last()
    if not last_request_no:
        return '1000'
    request_no = last_request_no.request_no
    new_request_no = str(int(request_no) + 1)
    new_request_no = request_no[0:-(len(new_request_no))] + new_request_no
    return new_request_no


def increment_case_no():
    last_case_no = Discipline.objects.all().order_by('case_no').last()
    if not last_case_no:
        return '0000'
    case_no = last_case_no.case_no
    new_case_no = str(int(case_no) + 1)
    new_case_no = case_no[0:-(len(new_case_no))] + new_case_no
    return new_case_no


def increment_training_no():
    last_training_no = Training.objects.all().order_by('training_no').last()
    if not last_training_no:
        return '0000'
    training_no = last_training_no.training_no
    new_training_no = str(int(training_no) + 1)
    new_training_no = training_no[0:-(len(new_training_no))] + new_training_no
    return new_training_no

class Department(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


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


    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.IntegerField(primary_key=True)
    employee = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    dob = models.DateField(default=date.today)
    gender = models.CharField(max_length=120, choices=GENDER,  null=True, blank=True)
    marital_status = models.CharField(max_length=120, choices=MARITAL_STATUS,  null=True, blank=True)
    next_of_kin = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    zone = models.CharField(max_length=120, choices=ZONE,  null=True, blank=True)
    #department = models.CharField(max_length=120, choices=DEPARTMENT,  null=True, blank=True)
    department = models.ForeignKey(Department, null=True,  on_delete=models.CASCADE)
    designation = models.ForeignKey('Title', null=True, blank=True, on_delete=models.DO_NOTHING)
    pay_grade = models.ForeignKey('Grade', null=True, blank=True, on_delete=models.DO_NOTHING)
    national_id = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=100)
    contact_address = models.TextField(blank = False, null = False)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    state_of_origin = models.CharField(max_length=100)
    local_government_area = models.CharField(max_length=100)
    date_joined = models.DateField(default=date.today)
    pension_date = models.DateField(default=date.today)
    qualification = models.CharField(max_length=120, choices=QUALIFICATION,  null=True, blank=True)
    languages = models.CharField(max_length=100)
    professional_organizations = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=120, choices=BLOOD_GROUP,  null=True, blank=True)
    drivers_license = models.ImageField(upload_to='%Y/%m/%d/', blank=True)
    digital_passport = models.ImageField(upload_to='%Y/%m/%d/', blank=True)
    special_interests = models.TextField(blank=True)
    hobbies = models.TextField(blank = False, null = False)
    profile_creation_date = models.DateField(default=date.today)

        
    def __str__(self):
        return str(self.employee.get_full_name)

class Driver(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200) 
    designation = models.CharField(max_length=200)  

class Title(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_title = models.CharField(max_length=200)
    description = models.TextField(blank = False, null = False) 
    date_added = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.job_title)


class Grade(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pay_grade_name = models.CharField(max_length=200)
    paygrade_description = models.TextField(blank = False, null = False)
    pay_grade_code = models.CharField(max_length=200, unique=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    date_created = models.DateField(auto_now_add=True, auto_now=False)


    def date_created_pretty(self):
        return self.date_created.strftime('%b %e %Y')

    def __str__(self):
        return str(self.pay_grade_name)

class Leave(models.Model):

    LEAVE_CHOICES = (
        ('Annual Leave', 'Annual Leave'),
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
        ('Examination Leave', 'Examination Leave'),
        ('Maternity Leave', 'Maternity Leave'),
        ('Compassionate Leave', 'Compassionate Leave'),
        ('Leave on Urgent Matter', 'Leave on Urgent Matter'),
        ('Leave of Absence', 'Leave of Absence'),
        ('Study Leave With Pay', 'Study Leave With Pay'),
        ('Study Leave Without Pay', 'Study Leave Without Pay'),
        ('Sabatical Leave', 'Sabatical Leave'),
        )

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_no = models.CharField(max_length=500, null=True, blank=True, unique=True,
        default=increment_request_no)
    requested_start_date = models.DateField(default=date.today)
    requested_end_date = models.DateField(default=date.today)
    staff_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    leave_type = models.CharField(max_length=120, choices=LEAVE_CHOICES, blank=False)
    leave_status = models.CharField(max_length=200, default="Pending Approval")
    leave_application_date = models.DateField(default=date.today)
    approved_on = models.DateField(auto_now_add=False, auto_now=True)


    class Meta:
       unique_together = ('request_no', 'staff_name',)
       ordering = ["-request_no"]

    
    def requested_start_date_pretty(self):
        return self.requested_start_date.strftime('%b %e %Y')

    def requested_end_date_pretty(self):
        return self.requested_end_date.strftime('%b %e %Y')

    def leave_application_date_pretty(self):
        return self.leave_application_date.strftime('%b %e %Y')

    def __str__(self):
        return str(self.staff_name)
    
class Specify(models.Model):

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_no = models.CharField(max_length=200)
    staff_name = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='staff', on_delete=models.DO_NOTHING)
    leave_type = models.CharField(max_length=200)
    leave_application_date = models.DateField(default=date.today)
    requested_start_date = models.DateField(default=date.today)
    requested_end_date = models.DateField(default=date.today)
    approved_start_date = models.DateField(default=date.today)
    approved_end_date = models.DateField(default=date.today)
    comments = models.TextField(blank = False, null = False)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approving_staff',  on_delete=models.DO_NOTHING)
    approved_date = models.DateField(default=date.today)
    leave_status = models.CharField(max_length=200, default="Leave Days Assigned")


    class Meta:
       unique_together = ('request_no', 'staff_name',)
       ordering = ["-request_no"]

    def __str__(self):
        return str(self.staff_name)
        #return self.staff_name.first_name + ' ' + self.staff_name.last_name
    def leave_application_date_pretty(self):
        return self.leave_application_date.strftime('%b %e %Y')

    def requested_start_date_pretty(self):
        return self.requested_start_date.strftime('%b %e %Y')

    def requested_end_date_pretty(self):
        return self.requested_end_date.strftime('%b %e %Y')

    def approved_start_date_pretty(self):
        return self.approved_start_date.strftime('%b %e %Y')

    def approved_end_date_pretty(self):
        return self.approved_end_date.strftime('%b %e %Y')


    def save(self, *args, **kwargs):
        super(Specify, self).save(*args, **kwargs)
        
        #try:
            #request = Request.objects.get(
                #request_no=self.request_no,
                #requesting_staff=self.requesting_staff,
                
                #)
        #except Request.DoesNotExist:
            #pass
         
        #if self.id is not None:
            #request.request_status = 2
            #request.save()

        p = Leave.objects.get(request_no=self.request_no)
        p.leave_status = "Leave Days Assigned"
        p.save()


class Document(models.Model):

    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_no = models.CharField(max_length=200)
    staff_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    leave_type = models.CharField(max_length=200)
    leave_application_date = models.DateField(default=date.today)
    requested_start_date = models.DateField(default=date.today)
    requested_end_date = models.DateField(default=date.today)
    approved_start_date = models.DateField(default=date.today)
    approved_end_date = models.DateField(default=date.today)
    actual_start_date = models.DateField(default=date.today)
    actual_end_date = models.DateField(default=date.today)
    comments = models.TextField(blank = False, null = False)
    documented_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='leave_entry_by', on_delete=models.DO_NOTHING)
    entry_date = models.DateField(default=date.today)
    leave_status = models.CharField(max_length=200, default="Leave Completed")


    class Meta:
       unique_together = ('request_no', 'staff_name',)
       ordering = ["-request_no"]

    def __str__(self):
        return str(self.staff_name)
        
    
    def requested_start_date_pretty(self):
        return self.requested_start_date.strftime('%b %e %Y')

    def requested_end_date_pretty(self):
        return self.requested_end_date.strftime('%b %e %Y')

    def approved_start_date_pretty(self):
        return self.approved_start_date.strftime('%b %e %Y')

    def approved_end_date_pretty(self):
        return self.approved_end_date.strftime('%b %e %Y')


    def save(self, *args, **kwargs):
        super(Document, self).save(*args, **kwargs)
        
        p = Specify.objects.get(request_no=self.request_no)
        p.leave_status = "Leave Completed"
        p.save()



class Location(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    address = models.TextField(blank = False, null = False)
    

class Category(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank = False, null = False)
    added_on = models.DateField(default=date.today)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='category_added_by', on_delete=models.DO_NOTHING)
    

    def __str__(self):
        return self.category_name

class Vendor(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    description = models.TextField(blank = False, null = False)
    date_created = models.DateField(default=date.today)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='vendor_added_by', on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.vendor_name

    def date_created_pretty(self):
        return self.date_created.strftime('%b %e %Y')

    class Meta:
        ordering = ["-date_created"]


class Course(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training_name = models.CharField(max_length=200)
    training_description = models.CharField(max_length=200)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.DO_NOTHING)
    vendor = models.ForeignKey('Vendor', null=True, blank=True, on_delete=models.DO_NOTHING)
    date_added = models.DateField(default=date.today)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='course_added_by',on_delete=models.DO_NOTHING)

    class Meta:
       ordering = ['-date_added']

    def __str__(self):
        return self.training_name


class Training(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training_no = models.CharField(max_length=500, null=True, blank=True, unique=True,
        default=increment_training_no)
    training_name = models.CharField(max_length=200)
    training_description = models.CharField(max_length=200)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.DO_NOTHING)
    vendor = models.ForeignKey('Vendor', null=True, blank=True, on_delete=models.DO_NOTHING)
    #staff_name = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='scheduled_staff')
    employee = models.ManyToManyField(Employee, related_name='employee_tr')
    #department = models.ManyToManyField(Department, related_name='department_tr')
    department = models.ForeignKey(Department, null=True, related_name='department_tr', on_delete=models.CASCADE)
    
    projected_start_date = models.DateField(default=date.today)
    projected_end_date = models.DateField(default=date.today)
    training_venue = models.CharField(max_length=200)
    training_budget = models.DecimalField(max_digits=50, decimal_places=2,)
    training_status = models.CharField(max_length=200, default="Scheduled")
    date_added = models.DateField(default=date.today)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='training_added_by',on_delete=models.DO_NOTHING)


    class Meta:
       ordering = ['-date_added']

    def __str__(self):
        return self.training_name

 
class Record(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training_no = models.CharField(max_length=200)
    training_name = models.CharField(max_length=200)
    training_description = models.CharField(max_length=200)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.DO_NOTHING)
    vendor = models.ForeignKey('Vendor', null=True, blank=True, on_delete=models.DO_NOTHING)
    staff_name = models.ManyToManyField(settings.AUTH_USER_MODEL)
    projected_start_date = models.DateField(default=date.today)
    projected_end_date = models.DateField(default=date.today)
    training_venue = models.CharField(max_length=200)
    training_budget = models.DecimalField(max_digits=50, decimal_places=2,)
    training_start_date = models.DateField(default=date.today)
    training_end_date = models.DateField(default=date.today)
    training_cost = models.DecimalField(max_digits=50, decimal_places=2,)
    training_status = models.CharField(max_length=200, default="Concluded")
    date_recorded = models.DateField(default=date.today)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='record_added_by', on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.training_name


    def save(self, *args, **kwargs):
        super(Record, self).save(*args, **kwargs)
        
        try:
            schedule = Training.objects.get(
                schedule_no=self.schedule_no,
                staff_name=self.staff_name,
                
                )
        except Training.DoesNotExist:
            pass
        
       
        if self.id is not None:
            training.training_status = "Concluded"
            training.save()


class Appraisal(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appraisal_name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank = False, null = False)
    added_on = models.DateField(default=date.today)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appraisal_added_by', on_delete=models.DO_NOTHING)
    

    def __str__(self):
        return self.appraisal_name

class Schedule(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule_no = models.CharField(max_length=500, null=True, blank=True, unique=True, 
        default=increment_schedule_no)
    staff_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    appraisal = models.ForeignKey('Appraisal', related_name="appraisal_type", null=False, blank=False, on_delete=models.DO_NOTHING)
    appraisal_due_date = models.DateField(default=date.today)
    projected_start_date = models.DateField(default=date.today)
    projected_end_date = models.DateField(default=date.today)
    appraisal_status = models.CharField(max_length=200, default="Scheduled")
    appraisal_scheduled_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appraisal_scheduler', on_delete=models.DO_NOTHING)
    appraisal_scheduled_on = models.DateField(default=date.today)
    
    def __str__(self):
        return str(self.staff_name)

    class Meta:
        unique_together = ('schedule_no','staff_name')
        ordering = ["-appraisal_scheduled_on"]

      
class Performance(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule_no = models.CharField(max_length=200)
    staff_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    appraisal = models.ForeignKey('Appraisal', related_name="appraisal", null=False, blank=False, on_delete=models.DO_NOTHING)
    appraisal_due_date = models.DateField(default=date.today)
    projected_start_date = models.DateField(default=date.today)
    projected_end_date = models.DateField(default=date.today)
    appraisal_start_date = models.DateField(default=date.today)
    appraisal_end_date = models.DateField(default=date.today)
    appraisal_status = models.CharField(max_length=200, default="Appraised")
    comments = models.TextField(blank = False, null = False)
    score = models.IntegerField()
    appraised_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appraiser', on_delete=models.DO_NOTHING)
    documented_on = models.DateField(default=date.today)
    
    
    def __str__(self):
        return str(self.staff_name)


    class Meta:
        unique_together = ('schedule_no','staff_name')
        ordering = ["-documented_on"]


    def save(self, *args, **kwargs):
        super(Performance, self).save(*args, **kwargs)
        
        try:
            schedule = Schedule.objects.get(
                schedule_no=self.schedule_no,
                staff_name=self.staff_name,
                
                )
        except Schedule.DoesNotExist:
            pass
        
       
        if self.id is not None:
            schedule.appraisal_status = "Appraised"
            schedule.save()
    

class Discipline(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case_no = models.CharField(max_length=500, null=True, blank=True, unique=True, 
        default=increment_case_no)
    staff_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    case_name = models.CharField(max_length=200)
    case_description = models.TextField(blank = False, null = False)
    penalty = models.CharField(max_length=200)
    due_date = models.DateField(default=date.today)
    case_status = models.CharField(max_length=200, default="In Progress")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='admin_officer', on_delete=models.DO_NOTHING)
    assigned_on = models.DateField(default=date.today)
    
    def __str__(self):
        return str(self.staff_name)

    class Meta:
        unique_together = ('case_no','staff_name')
        ordering = ["-assigned_on"]

      
class Compliance(models.Model):

    CASE_CHOICES = (
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        )


    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case_no = models.CharField(max_length=200)
    staff_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    case_name = models.CharField(max_length=200)
    case_description = models.TextField(blank = False, null = False)
    penalty = models.CharField(max_length=200)
    due_date = models.DateField(default=date.today)
    case_status = models.CharField(max_length=200, choices=CASE_CHOICES, blank=False)
    completed_on = models.DateField(default=date.today)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='hr_officer', on_delete=models.DO_NOTHING)
    closed_on = models.DateField(default=date.today)
    
    
    def __str__(self):
        return str(self.staff_name)


    def save(self, *args, **kwargs):
        super(Compliance, self).save(*args, **kwargs)
        
        try:
            discipline = Discipline.objects.get(
                case_no=self.case_no,
                staff_name=self.staff_name,
                
                )
        except Discipline.DoesNotExist:
            pass
        
       
        if self.id is not None:
            discipline.case_status = "Completed"
            discipline.save()


    class Meta:
        unique_together = ('case_no','staff_name')
        ordering = ["-closed_on"]


    
    

