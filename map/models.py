from django.core.exceptions import ValidationError
from django.db import models


def validate_nonzero(value):
    if value == 0:
        raise ValidationError(
            _('House Number %(value)s is not allowed'),
            params={'value': value},
        )


class Address(models.Model):
    country = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=20, null=True, blank=True)
    house_no = models.PositiveIntegerField(null=True, blank=True, validators=[validate_nonzero])

    def __str__(self):
        return "{city}, {street}".format(city=self.city, street=self.street)
