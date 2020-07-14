
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView



urlpatterns = [
    path('admin/', admin.site.urls),
    #    path('', RedirectView.as_view(url='/accounts/login/')),
    #path('accounts/', include('accounts.urls')),
    path('', RedirectView.as_view(url='/accounts/login/')),
    path('accounts/', include("accounts.urls")),
    path('admin_func/', include("admin_func.urls")),
    path('bicycle_borrow_sub_sys/', include('bicycle_borrow_sub_sys.urls')),
]
