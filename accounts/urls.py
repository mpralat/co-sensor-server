from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import SignUpView, AccountActivateView

urlpatterns = [
    url(r'^signup/', SignUpView.as_view(), name='signup'),
    url(r'^account_activation_sent/$',
        TemplateView.as_view(
            template_name="accounts/account_activation_sent.html"
        ),
        name='account_activation_sent'),
    url(r'^activate/' +
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/' +
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        AccountActivateView.as_view(),
        name='activate'),
    url(r'^account_activation_invalid',
        TemplateView.as_view(
            template_name="accounts/account_activation_invalid.html"
        ),
        name='account_activation_invalid'),
    url(r'^login/',
        auth_views.login, {
            'template_name': 'accounts/login.html',
        },
        name='login'),
    url(r'^logout/', auth_views.logout, name='logout'),
]
