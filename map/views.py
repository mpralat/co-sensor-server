from django.shortcuts import render
from django.conf import settings

from sensors.models import Sensor


def _get_sensors_info(owner):
    sensors = Sensor.objects.filter(owner=owner)
    return [{
        "serial_number": sensor.serial_number,
        "name": sensor.name,
        "lat": sensor.address.latitude,
        "lng": sensor.address.longitude,
        "lastTimestamp": "",
        "co_value": ""
    } for sensor in sensors]


def show_map(request):
    google_key = settings.GOOGLE_MAPS_API_KEY
    sensors_list = _get_sensors_info(request.user)
    return render(request, 'map.html', {'google_key': google_key,
                                        'sensors_list': sensors_list})

