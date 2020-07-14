'''
Created on 2018/12/12

@author: t16cs060
'''

from django.urls import path
from . import views
from django.urls.conf import include

app_name = 'accounts'

urlpatterns = [
    path('login/', views.employee_login, name='login'),
    path('logout/', views.employee_logout, name='logout'),
    path('manager_login/', views.manager_login, name='manager_login'),
    path('manager_logout/', views.manager_logout, name='manager_logout'),
    path('top_test/', views.top_test, name='top_test'),
    path('manager_top_test/', views.manager_top_test, name='manager_top_test')
]
