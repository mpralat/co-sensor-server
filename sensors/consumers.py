import smtplib
from datetime import datetime
from decimal import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.renderers import JSONRenderer

from co_sensor import settings
from .models import Sensor, SensorData
from .serializers import SensorDataSerializer

CRITICAL_VALUE = 4.0

class SensorConsumer(JsonWebsocketConsumer):
    channel_session = True

    def connect(self, message, **kwargs):
        serial_number = message['path'].split('/')[-2]
        message.channel_session['serial_number'] = serial_number

        if not self.sensor_exists():
            if not self.register_sensor():
                self.close()

        super().connect(message, **kwargs)

    def receive(self, content, **kwargs):
        timestamp = content["timestamp"]
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
        value = Decimal(content["value"]).quantize(Decimal('.01'))

        print("[{timestamp}] {value}".format(timestamp=timestamp, value=value))
        serial_number = self.message.channel_session['serial_number']
        sensor = Sensor.objects.get(serial_number=serial_number)

        if value > CRITICAL_VALUE:
            send_mail(value=value, owner=sensor.owner)

        data = SensorData(timestamp=timestamp, value=value, sensor=sensor)
        try:
            data.full_clean()
        except ValidationError:
            return
        data.save()

        frame = {
            'timestamp': content['timestamp'],
            'value': content['value']
        }
        self.group_send('room-' + serial_number, frame)

    def sensor_exists(self):
        serial_number = self.message.channel_session['serial_number']

        try:
            Sensor.objects.get(serial_number=serial_number)
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def register_sensor(self):
        serial_number = self.message.channel_session['serial_number']

        sensor = Sensor(serial_number=serial_number)

        try:
            sensor.full_clean()
        except ValidationError:
            return False
        else:
            sensor.save()
            return True


class ClientConsumer(JsonWebsocketConsumer):
    channel_session_user = True
    http_user = True

    def connect(self, message, **kwargs):
        serial_number = message['path'].split('/')[-2]

        message.channel_session['serial_number'] = serial_number

        if not self.user_is_sensor_owner():
            self.close()

        group = Group('room-' + serial_number)
        group.add(self.message.reply_channel)

        super().connect(message, **kwargs)

        if 'client' in message['path']:
            sensor = Sensor.objects.get(serial_number=self.message.channel_session['serial_number'])
            initial_data = SensorData.objects.filter(sensor=sensor).order_by('timestamp')[20:]
            serializer = SensorDataSerializer(initial_data, many=True)
            frame = JSONRenderer().render(serializer.data).decode()

            message.reply_channel.send({
                'text': frame
            })

    def disconnect(self, message, **kwargs):
        serial_number = self.message.channel_session['serial_number']
        group = Group('room-' + serial_number)
        group.discard(self.message.reply_channel)

        super().disconnect(message, **kwargs)

    def user_is_sensor_owner(self):
        serial_number = self.message.channel_session['serial_number']
        user = self.message.user

        try:
            Sensor.objects.filter(serial_number=serial_number, owner=user)
        except ObjectDoesNotExist:
            return False
        else:
            return True


def create_the_mail(to):
    msg = MIMEMultipart()
    msg['From'] = 'No-Reply test_django@o2.pl'
    msg['To'] = to
    msg['Subject'] = 'simple email in python'
    message = 'here is the email'
    msg.attach(MIMEText(message))
    return msg

def send_mail(value, owner):
    smtp = smtplib.SMTP(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT)
    smtp.ehlo()
    smtp.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
    msg = create_the_mail(to='pralatmarta@gmail.com')
    smtp.sendmail(from_addr=settings.EMAIL_HOST_USER, to_addrs='pralatmarta@gmail.com', msg=msg.as_string())