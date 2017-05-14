from django.shortcuts import render
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Room, Message, Sensor
from .forms import SensorForm
from accounts.views import OnlyAuthenticatedView
from accounts.models import Profile


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


class SensorListView(OnlyAuthenticatedView):
    template_name = "sensors/list.html"

    def get_context_data(self, **kwargs):
        context = super(SensorListView, self).get_context_data(**kwargs)
        context['sensors'] = Sensor.objects.filter(owner=self.request.user)
        form = SensorForm(self.request.POST or None)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        form: SensorForm = context['form']
        if form.is_valid():
            serial_number = form.cleaned_data['serial_number']
            name = form.cleaned_data['name']
            sensor = Sensor.objects.get(serial_number=serial_number)
            sensor.name = name
            sensor.owner = request.user
            sensor.save()

        return super().render_to_response(context)
