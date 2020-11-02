from django.db import models
import uuid
from django.conf import settings

# Create your models here.


class Procurement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=200)
    project_tasks = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=50, decimal_places=2,)
    project_total = models.DecimalField(max_digits=50, decimal_places=2,)
    task_start_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    task_end_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    completion_status = models.CharField(max_length=200)
    task_dependencies = models.CharField(max_length=200)
    remarks = models.TextField(blank=True, null=True)

    
      
    def __str__(self):
        return self.project_name