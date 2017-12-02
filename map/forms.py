from django.forms import Form, IntegerField, CharField


class AddressForm(Form):
    country = CharField(max_length=20, required=False)
    city = CharField(max_length=20, required=False)
    street = CharField(max_length=20, required=False)
    house_no = IntegerField(required=False, min_value=1)

    def clean(self):
        country = self.cleaned_data['country']
        city = self.cleaned_data['city']
        street = self.cleaned_data['street']
        house_no = self.cleaned_data['house_no']
        fields = [country, city, street, house_no]
        if any(fields) and any(field is None for field in fields):
            self.add_error('country', 'Please make sure all the address fields are filled.')
