from django.contrib import admin
from .models import IntelliUser, Company, History
# Register your models here.

admin.site.register(IntelliUser)
admin.site.register(Company)
admin.site.register(History)
