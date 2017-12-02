from django.conf.urls import url
from .views import show_map


urlpatterns = [
    url(r'^$', show_map, name='map'),
]
