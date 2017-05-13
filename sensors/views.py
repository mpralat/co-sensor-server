from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Room, Message, Sensor
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

    def get(self, request, *args, **kwargs):
        return super(SensorListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SensorListView, self).get_context_data(**kwargs)
        context["sensors"] = Sensor.objects.filter(owner=self.request.user)
        return context
