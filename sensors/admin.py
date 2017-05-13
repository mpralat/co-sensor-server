from django.contrib import admin
from accounts.models import Profile
from sensors.models import Room, Message, Sensor

# Register your models here.
admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Sensor)
