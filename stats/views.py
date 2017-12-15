import datetime

from django.db.models import Count, Avg
from django.db.models.functions import ExtractWeekDay
from django.shortcuts import render

from sensors.models import Sensor, SensorData

def _get_sensors_serial_nums(owner):
    sensors = Sensor.objects.filter(owner=owner)
    return [sensor.serial_number for sensor in sensors]

def show_week_stats(request):
    sensor_labels = _get_sensors_serial_nums(request.user)
    sensor_data_filtered = SensorData.objects.filter(
        sensor__serial_number__in=sensor_labels,
        timestamp__gte=datetime.datetime.today() - datetime.timedelta(days=30)
    )
    averages = sensor_data_filtered.annotate(
        weekday=ExtractWeekDay('timestamp')).values('weekday').annotate(value=Avg('value')).order_by()
    counters = sensor_data_filtered.annotate(
            weekday=ExtractWeekDay('timestamp')).values('weekday').annotate(value=Count('value')).order_by()
    avgs = [0] * 8
    counts = [0] * 8
    for val in averages:
        index = int(val.get('weekday'))
        avgs.insert(index, val.get('value'))
    for val in counters:
        index = int(val.get('weekday'))
        counts.insert(index, val.get('value'))

    return render(request, "stats/main_statistics.html", {
        'averages': avgs[1:],
        'counts': counts[1:],
        'sensor_labels': sensor_labels
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

def get_average_from_last_month(request):
    sensors = Sensor.objects.filter(owner=request.user)
    data = SensorData.objects.filter(
        sensor_in=sensors,
        timestamp__gte=datetime.datetime.today() - datetime.timedelta(days=7)
    )
    return render(request, "stats/main_statistics.html", {
        'data': data
    })