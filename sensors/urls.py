from django.conf.urls import url
from .views import chat_room, SensorListView


urlpatterns = [
    url(r'^list', SensorListView.as_view(), name="sensors_list"),
    url(r'^room/(?P<label>[0-9A-Za-z_\-]+)', chat_room, name='room'),
]
