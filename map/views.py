from django.shortcuts import render
from django.conf import settings

from sensors.models import Sensor


def show_map(request):
    google_key = settings.GOOGLE_MAPS_API_KEY
    sensors_list = Sensor.objects.filter(owner=request.user)
    return render(request, 'map.html', {'google_key': google_key,
                                        'sensors_list': sensors_list})

