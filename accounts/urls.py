from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import signup, activate

urlpatterns = [
    url(r'^signup/', signup, name='signup'),
    url(r'^login/',
        auth_views.login, {
            'template_name': 'accounts/login.html',
        },
        name='login'),
    url(r'^logout/', auth_views.logout, name='logout'),
    url(r'^account_activation_sent/$',
        TemplateView.as_view(
            template_name="accounts/account_activation_sent.html"
        ),
        name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]
