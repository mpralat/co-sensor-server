from channels.generic.websockets import JsonWebsocketConsumer
from channels import Group
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Sensor, SensorData
from decimal import *
from datetime import datetime


class SensorConsumer(JsonWebsocketConsumer):
    channel_session_user = True

    def connect(self, message, **kwargs):
        print(dict(message))
        serial_number = message['path'].split('/')[-2]
        print(serial_number)
        message.channel_session['serial_number'] = serial_number

        if not self.sensor_exists(serial_number):
            if not self.register_sensor(serial_number):
                self.close()

        self.message.reply_channel.send({"accept": True})

    def disconnect(self, message, **kwargs):
        self.close()

    def receive(self, content, **kwargs):
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

        Group('room-' + serial_number).send({
            'timestamp': content["timestamp"],
            'value': content["value"]
        })

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


class ClientConsumer(JsonWebsocketConsumer):
    channel_session_user = True

    def connect(self, message, **kwargs):
        serial_number = message['path'].split('/')[-1]
        message.channel_session['serial_number'] = serial_number
        Group('room-' + serial_number).add(message.reply_channel)

    def receive(self, content, **kwargs):
        serial_number = self.message.channel_session['serial_number']
        Group('room-' + serial_number).send({
            'text': "Echo!"
        })

    def disconnect(self, message, **kwargs):
        serial_number = message.channel_session['serial_number']
        Group('room-' + serial_number).discard(message.reply_channel)
