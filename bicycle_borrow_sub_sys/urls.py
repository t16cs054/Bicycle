from django.urls import path
from . import views
from django.urls.conf import include

app_name = 'bicycle_borrow_sub_sys'

urlpatterns = [
    path('', views.top, name='top'),
    path('borrow_bicycle/', views.borrow_bicycle, name='borrow_bicycle'),
    path('borrow_warning/<int:num>', views.borrow_warning, name='borrow_warning'),
    path('borrowed/<int:num>', views.borrowed, name='borrowed'),
    path('return_bicycle/', views.return_bicycle, name='return_bicycle'),
    path('return_warning/', views.return_warning, name='return_warning'),
    path('returned/<int:num>', views.returned, name='returned'),
    path('accounts/',include('accounts.urls'))
    ]