from django.contrib import admin

# Register your models here.

from .models import Bicycle

admin.site.register(Bicycle)

from .models import Office

admin.site.register(Office)

from .models import Borrow_history

admin.site.register(Borrow_history)