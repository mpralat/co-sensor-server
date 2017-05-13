from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer
from channels.sessions import channel_session
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Sensor, SensorData
import json
from decimal import *
from datetime import datetime


class SensorConsumer(JsonWebsocketConsumer):
    channel_session_user = True

    def connect(self, message, multiplexer, **kwargs):
        serial_number = message['path'].split('/')[-1]
        message.channel_session['serial_number'] = serial_number

        if not self.sensor_exists(serial_number):
            if not self.register_sensor(serial_number):
                multiplexer.send({"close": True})

    def disconnect(self, message, multiplexer, **kwargs):
        print("Stream %s is closed" % multiplexer.stream)

    def receive(self, content, multiplexer, **kwargs):
        timestamp = content["timestamp"]
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
        value = Decimal(content["value"]).quantize(Decimal('.01'))
        print("[{timestamp}] {value}".format(timestamp=timestamp, value=value))
        serial_number = self.message.channel_session['serial_number']
        sensor = Sensor.objects.get(serial_number=serial_number)

        data = SensorData(timestamp=timestamp, value=value, sensor=sensor)
        try:
            data.full_clean()
        except ValidationError:
            return
        data.save()

    def sensor_exists(self, serial_number):
        try:
            Sensor.objects.get(serial_number=serial_number)
        except ObjectDoesNotExist:
            return False

        return True

    def register_sensor(self, serial_number):
        sensor = Sensor(serial_number=serial_number)

        try:
            sensor.full_clean()
        except ValidationError:
            return False

        sensor.save()
        return True
