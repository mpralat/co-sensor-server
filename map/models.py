from django.core.exceptions import ValidationError
from django.db import models


class Address(models.Model):
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return "Longitude: {long}, latitude: {lat}".format(long=self.longitude, lat=self.latitude)