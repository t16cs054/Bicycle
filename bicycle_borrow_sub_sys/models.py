from django.db import models
from accounts.models import Employee
import datetime
import time
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Office(models.Model):
    office_id = models.IntegerField(primary_key=True)
    office_name = models.CharField(max_length=6)
    bicycle_nums_office = models.IntegerField()
    
    
    
    
class Bicycle(models.Model):
    bicycle_id = models.IntegerField(primary_key = True)
    color = models.IntegerField()
    status = models.BooleanField()
    office_id = models.ForeignKey(Office,on_delete=models.SET_NULL,
    null=True)
    
    
    
class Borrow_history(models.Model):
    borrow_id = models.IntegerField(primary_key = True)
    bicycle_id = models.ForeignKey(Bicycle,on_delete=models.SET_NULL,
    null=True)
    employee_id = models.ForeignKey(Employee,on_delete=models.SET_NULL,
    null=True, blank=True)
    start_day = models.DateField(null=True,blank=True)
    
    def how_long_borrow(self):
        if(self.start_day == None):
            return -1
        now = datetime.date.today()
        return (now - self.start_day).days