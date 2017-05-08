from django.conf.urls import url
from .views import chat_room


urlpatterns = [
    url(r'^room/(?P<label>[0-9A-Za-z_\-]+)', chat_room, name='room'),
]
