from django.db import models


class Address(models.Model):
    country = models.TextField(max_length=20, null=True, blank=False)
    city = models.TextField(max_length=20, null=True, blank=False)
    street = models.TextField(max_length=20, null=True, blank=False)
    house_no = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return "{city}, {street}".format(city=self.city, street=self.street)
