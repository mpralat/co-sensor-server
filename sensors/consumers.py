from channels.generic.websockets import JsonWebsocketConsumer
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Sensor, SensorData
from decimal import *
from datetime import datetime


class SensorConsumer(JsonWebsocketConsumer):
    channel_session = True

    def connect(self, message, **kwargs):
        serial_number = message['path'].split('/')[-2]
        message.channel_session['serial_number'] = serial_number

        if not self.sensor_exists(serial_number):
            if not self.register_sensor(serial_number):
                self.close()

        super().connect(message, **kwargs)

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

        self.group_send('room-' + serial_number, {
            'text': {
                'timestamp': content['timestamp'],
                'value': content['value']
            }
        })

    @classmethod
    def sensor_exists(cls, serial_number):
        try:
            Sensor.objects.get(serial_number=serial_number)
        except ObjectDoesNotExist:
            return False

        return True

    @classmethod
    def register_sensor(cls, serial_number):
        sensor = Sensor(serial_number=serial_number)

        try:
            sensor.full_clean()
        except ValidationError:
            return False

        sensor.save()
        return True


class ClientConsumer(JsonWebsocketConsumer):
    channel_session_user = True