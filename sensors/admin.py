from django.contrib import admin
from .models import Sensor, SensorData

admin.site.register(Sensor)
admin.site.register(SensorData)
