from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer
from channels.sessions import channel_session
from .models import Sensor
import json


class SensorConsumer(JsonWebsocketConsumer):

    def connect(self, message, multiplexer, **kwargs):
        print("I just connected!")
        # Send data with the multiplexer
        multiplexer.send({"status": "I just connected!"})

    def disconnect(self, message, multiplexer, **kwargs):
        print("Stream %s is closed" % multiplexer.stream)

    def receive(self, content, multiplexer, **kwargs):
        # Simple echo
        multiplexer.send({"original_message": content})
