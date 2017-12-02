from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, DeleteView

from accounts.models import Profile
from accounts.views import OnlyAuthenticatedView
from map.geo_resolver import GeoResolver
from .forms import SensorForm
from .models import Room, Message, Sensor
from map.forms import AddressForm
from map.models import Address


def chat_room(request, label):
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    room, created = Room.objects.get_or_create(label=label)

    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "sensors/room.html", {
        'room': room,
        'messages': messages,
    })


def statistics(request, label):
    return HttpResponse("Statistics for {}".format(label))


class SensorListView(OnlyAuthenticatedView):
    template_name = "sensors/list.html"

    def get_context_data(self, **kwargs):
        context = super(SensorListView, self).get_context_data(**kwargs)
        context['sensors'] = Sensor.objects.filter(owner=self.request.user)
        form = SensorForm(self.request.POST or None)
        context['form'] = form
        address_form = AddressForm(self.request.POST or None)
        context['address_form'] = address_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        form: SensorForm = context['form']
        address_form: AddressForm = context['address_form']
        if form.is_valid():
            serial_number = form.cleaned_data['serial_number']
            name = form.cleaned_data['name']
            sensor = Sensor.objects.get(serial_number=serial_number)
            sensor.name = name
            sensor.owner = request.user
            if address_form.is_valid():
                country = address_form.cleaned_data['country']
                city = address_form.cleaned_data['city']
                street = address_form.cleaned_data['street']
                house_no = address_form.cleaned_data['house_no']
                resolver = GeoResolver()
                coords = resolver.get_coordinates(country=country, city=city, street=street, house_no=house_no)
                if coords:
                    address = Address(longitude=coords.get('lng'), latitude=coords.get('lat'))
                    address.save()
                    sensor.address = address
                sensor.save()


        return super().render_to_response(context)


def sensor_delete(request, *args, **kwargs):
    sensor_pk = kwargs["pk"]
    if request.method == 'GET':
        return render(request, 'sensors/sensor_delete.html', {"sensor_pk": sensor_pk})
    else:
        sensor = Sensor.objects.filter(serial_number=sensor_pk).first()
        if sensor is not None:
            sensor.owner = None
            sensor.name = None
            Address.objects.get(id=sensor.address.id).delete()
            sensor.save()
        return redirect('sensors_list')
