from django.contrib import admin

from map.models import Address
from .models import Sensor, SensorData

admin.site.register(Sensor)
admin.site.register(SensorData)
admin.site.register(Address)