from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name="co_sensor/home.html"),
        name='home'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^sensors/', include('sensors.urls')),
    url(r'^admin/', admin.site.urls),
]
