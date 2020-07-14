from django.db import models
from django.db.models.fields import AutoField
from django.core.validators import *
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.

class EmployeeManager(BaseUserManager):
    
    use_in_migrations = True
    
    def _create_user(self, employee_id, password, **extra_fields):
        """Create and save a user with the given username, employee_id, and
        password."""
        if not employee_id:
            raise ValueError('The given employee_id must be set')
        employee_id = employee_id
        user = self.model(employee_id=employee_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_user(self , employee_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(employee_id, password, **extra_fields)
 
    def create_superuser(self, employee_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
 
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
 
        return self._create_user(employee_id, password, **extra_fields)
    
    def get_by_natural_key(self,employee_id_):
        return self.get(employee_id=employee_id_)

class Employee(AbstractBaseUser,PermissionsMixin):
    employee_id = models.PositiveIntegerField(primary_key=True,verbose_name='社員番号',unique=True)
    username = models.CharField(max_length=10,verbose_name='社員名')
    password = models.CharField(max_length=128,verbose_name='パスワード')
    borrowed_bicycles = models.PositiveSmallIntegerField(default=0,validators=[MaxValueValidator(3)],verbose_name='借りている自転車の数')
    #is_staffとis_superuserの両方をTrueにしないと管理者サイトにアクセスできない
    is_staff = models.BooleanField(default=False,verbose_name='管理者サイトへのアクセス権限')
    is_superuser = models.BooleanField(default=False,verbose_name='管理者サイトでの編集権限')
    
    objects = EmployeeManager()
    
    def __str__ (self):
        return str(self.employee_id)
    
    def return_my_nums(self):
        if(self.borrowed_bicycles is None):
            return 0
        else:
            return self.borrowed_bicycles
    
    USERNAME_FIELD='employee_id'
