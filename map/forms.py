from django.forms import ModelForm
from .models import Address


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ('country', 'city', 'street', 'house_no')
