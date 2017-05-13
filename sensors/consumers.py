from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer
from channels.sessions import channel_session
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Sensor
import json


class SensorConsumer(JsonWebsocketConsumer):

    def connect(self, message, multiplexer, **kwargs):
        print(message['path'])
        serial_number = message['path'].split('/')[-1]
        print("I just connected!", serial_number)
        if not self.sensor_exists(serial_number):
            if not self.register_sensor(serial_number):
                multiplexer.send({"close": True})

    def disconnect(self, message, multiplexer, **kwargs):
        print("Stream %s is closed" % multiplexer.stream)

    def receive(self, content, multiplexer, **kwargs):
        value = content["value"]
        timestamp = content["timestamp"]
        print("[{timestamp}] {value}".format(timestamp=timestamp, value=value))

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
