from django.urls import path
from . import views
from django.urls.conf import include

app_name = 'admin_func'

urlpatterns = [
    path('', views.top, name='top'),
    path('transfer_warning/<int:num>', views.transfer_warning, name='transfer_warning'),
    path('transfer_comp/<int:num>', views.transfer_comp, name='transfer_comp'),
]
