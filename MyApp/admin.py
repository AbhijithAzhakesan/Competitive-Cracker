from django.contrib import admin

from MyApp import models

# Register your models here.

admin.site.register(models.Customers)
admin.site.register(models.TeachersLogin)
admin.site.register(models.Courses)
admin.site.register(models.OnlineClass)
admin.site.register(models.Purchase)
