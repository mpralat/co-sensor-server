from django.db import models
from django.utils import timezone
from accounts.models import Profile


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
    serial_number = models.UUIDField(primary_key=True, editable=False)
    name = models.TextField()
    owner = models.ForeignKey(Profile, related_name='sensors')
