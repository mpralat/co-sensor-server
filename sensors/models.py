from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from map.models import Address


class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {
            'handle': self.handle,
            'message': self.message,
            'timestamp': self.formatted_timestamp
        }


class Sensor(models.Model):
    SERIAL_LENGTH = 16
    hex_validator = RegexValidator(
        r'^[0-9A-F]{16}$',
        "Only hex values are allowed"
    )
    serial_number = models.CharField(
        primary_key=True,
        max_length=SERIAL_LENGTH,
        validators=[hex_validator],
    )
    name = models.TextField(max_length=20, null=True, blank=True)
    owner = models.ForeignKey(
        User,
        related_name='sensors',
        null=True,
        blank=True
    )
    address = models.ForeignKey(Address, null=True, blank=True, related_name="sensors")

    def save(self, *args, **kwargs):
        self.serial_number = self.serial_number.upper()
        difference = self.SERIAL_LENGTH - len(self.serial_number)
        if difference > 0:
            self.serial_number = '0' * difference + self.serial_number
        return super(Sensor, self).save(*args, **kwargs)

    def __str__(self):
        if self.owner is not None:
            return "{name}, {owner}".format(name=self.name, owner=self.owner)
        else:
            return "#" + self.serial_number


class SensorData(models.Model):
    timestamp = models.DateTimeField(null=False)
    value = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    sensor = models.ForeignKey(Sensor, related_name="data", null=False)

    def __str__(self):
        name = self.sensor.name
        return "[{timestamp}] {name}: {value}".format(
            timestamp=self.timestamp, name=name, value=self.value
        )
