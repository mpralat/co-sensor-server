from django.conf.urls import url

from stats.views import show_stats

urlpatterns = [
    url(r'^$', show_stats, name='statistics'),
]
