from django.contrib import admin

# Register your models here.

from .models.ride import RideRequest


admin.site.register(RideRequest)
