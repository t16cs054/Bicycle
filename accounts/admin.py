from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import Employee
 
 
class EmployeeChangeForm(UserChangeForm):
    class Meta:
        model = Employee
        fields = '__all__'
 
 
class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('employee_id',)
 
 
class EmployeeAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('employee_id','password',)}),
        (_('Personal info'), {'fields': ('username','borrowed_bicycles',)}),
        (_('Permissions'), {'fields': ('is_staff','is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee_id','password1', 'password2',),
        }),
    )
    form = EmployeeChangeForm
    add_form = EmployeeCreationForm
    list_display = ('employee_id', 'username','borrowed_bicycles','is_staff','is_superuser',)
    list_filter = ('is_staff','is_superuser',)
    search_fields = ('employee_id', 'username')
    ordering = ('employee_id',)
 
 
admin.site.register(Employee, EmployeeAdmin)