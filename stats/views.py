from django.http import HttpResponse
from django.shortcuts import render

from sensors.models import Sensor


def show_stats(request):

    return render(request, "stats/main_statistics.html", {
        'sensors': get_sensor_list(request.user),
        'name': 'dupa'
    })


def get_sensor_list(user):
    objects = Sensor.objects.filter(owner=user)
    return [sensor.serial_number for sensor in objects]
    # return objects

def get_danger_level(value):
    levels = {
        'medium': (9, 24),
        'normal': (5, 9),
        'healthy': (0 ,5)
    }
    for level, (lower, upper) in levels.items():
        if  lower < value <= upper:
            return level
    return 'dangerous'