from django.conf.urls import url
from .views import chat_room, SensorListView, sensor_delete


urlpatterns = [
    url(r'^list', SensorListView.as_view(), name='sensors_list'),
    url(r'^room/(?P<label>[0-9A-F]{16})', chat_room, name='room'),
    url(r'^delete/(?P<pk>[0-9A-F]{16})', sensor_delete, name='sensor_delete'),
]
