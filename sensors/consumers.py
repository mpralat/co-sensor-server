from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer
from channels.sessions import channel_session
from django.core.exceptions import ValidationError
from .models import Sensor
import json


class SensorConsumer(JsonWebsocketConsumer):

    def connect(self, message, multiplexer, **kwargs):
        print(message['path'])
        serial_number = message['path'].split('/')[-1]
        print("I just connected!", serial_number)
        if self.register(serial_number):
            print("Registered!")
        else:
            multiplexer.send({"close": True})

    def disconnect(self, message, multiplexer, **kwargs):
        print("Stream %s is closed" % multiplexer.stream)

    def receive(self, content, multiplexer, **kwargs):
        action = content["action"]
        if action == "register":
            serial_number = content["serial"]
            self.register(serial_number)
            multiplexer.send({"message": "Registered"})

    def register(self, serial_number):
        sensor = Sensor(serial_number=serial_number)
        try:
            sensor.full_clean()
        except ValidationError as error:
            return False

        sensor.save()
        return True
