from django.conf.urls import url

from stats.views import show_week_stats

urlpatterns = [
    url(r'^$', show_week_stats, name='statistics'),
]
