from django.conf.urls import url
from .views import chat_room, statistics, SensorListView


urlpatterns = [
    url(r'^list', SensorListView.as_view(), name='sensors_list'),
    url(r'^room/(?P<label>[0-9A-F]{16})', chat_room, name='room'),
    url(r'^statistics/(?P<label>[0-9A-F]{16})', statistics, name='statistics'),
]
