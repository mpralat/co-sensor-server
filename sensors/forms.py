from django.forms import CharField, TextInput, Form, ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import escape
from .models import Sensor


class SensorForm(Form):
    serial_number = CharField()
    name = CharField(widget=TextInput, max_length=20)

    def clean_serial_number(self):
        serial_number = escape(self.cleaned_data['serial_number'])

        try:
            sensor = Sensor.objects.get(serial_number=serial_number)
        except ObjectDoesNotExist:
            self.add_error('serial_number', "Sensor doesn't exist")
        else:
            if sensor.owner is not None:
                self.add_error('serial_number', "Sensor is registered by other user")

        return serial_number.upper()