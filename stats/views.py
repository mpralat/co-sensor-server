import datetime

import numpy as np
from django.db.models import Count, Avg
from django.db.models.functions import ExtractWeekDay
from django.shortcuts import render
from sklearn import linear_model

from sensors.models import Sensor, SensorData


def _get_sensors_data(owner):
    sensors = Sensor.objects.filter(owner=owner)
    return {sensor.serial_number: sensor.name for sensor in sensors}


def _prepare_data_array(iterable, item):
    result_arr = [0] * 8
    for val in iterable:
        index = int(val.get(item))
        result_arr.insert(index, val.get('value'))
    return result_arr

def _prepare_month_stats(sensors_labels):
    sensor_data_filtered = SensorData.objects.filter(
        sensor__serial_number__in=sensors_labels,
        timestamp__gte=datetime.datetime.today() - datetime.timedelta(days=30)
    )
    averages = sensor_data_filtered.annotate(
        weekday=ExtractWeekDay('timestamp')).values('weekday').annotate(value=Avg('value')).order_by()
    counters = sensor_data_filtered.annotate(
        weekday=ExtractWeekDay('timestamp')).values('weekday').annotate(value=Count('value')).order_by()
    avgs = _prepare_data_array(averages, 'weekday')
    counts = _prepare_data_array(counters, 'weekday')
    return {'averages': avgs[1:], 'counts': counts[1:]}


def _count_average(data):
    return float(sum(data)/max(len(data),1))


def _prepare_week_stats(sensors_labels):
    week_sensors = SensorData.objects.filter(
        sensor__serial_number__in=sensors_labels,
        timestamp__gte=datetime.datetime.now() - datetime.timedelta(days=7)
    )
    morning = []
    midday = []
    evening = []
    night = []
    for item in week_sensors:
        hour = item.timestamp.hour
        print(hour)
        if  6 < hour <= 12:
            morning.append(item.value)
        elif 12 < hour <= 18:
            midday.append(item.value)
        elif 18 < hour <= 24:
            evening.append(item.value)
        else:
            night.append(item.value)
    avgs = [_count_average(morning), _count_average(midday), _count_average(evening), _count_average(night)]
    counts = [len(morning), len(midday), len(evening), len(night)]
    print(avgs, counts)
    return {'daytime_avgs': avgs, 'daytime_counts': counts}


def show_week_stats(request):
    sensors_data = _get_sensors_data(request.user)
    sensors_labels = list(sensors_data.keys())
    result_dict = {
        'sensors_data': sensors_data,
        'sensors_labels': sensors_labels
    }

    monthly_data = _prepare_month_stats(sensors_labels)
    result_dict.update(monthly_data)
    weekly_data = _prepare_week_stats(sensors_labels)
    print(weekly_data)
    result_dict.update(weekly_data)
    return render(request, "stats/main_statistics.html", result_dict)

