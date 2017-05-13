from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from .forms import SignUpForm
from .tokens import account_activation_token


class SignUpView(TemplateView):
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        self.form = SignUpForm()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form = SignUpForm(request.POST)
        if self.form.is_valid():
            user = self.__save_user()

            self.__send_activation_mail(user, request)

            return HttpResponseRedirect(reverse('account_activation_sent'))
        else:
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def __save_user(self):
        user = self.form.save(commit=False)
        user.is_active = False
        user.save()
        return user

    def __send_activation_mail(self, user, request):
        domain = get_current_site(request).domain
        subject = 'Activate Your CO Sensor Account'
        message = render_to_string(
            'accounts/account_activation_email.html', {
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )
        send_mail(
            subject=subject,
            message='Activate Your CO Sensor Account',
            from_email="no-reply@" + domain,
            recipient_list=[user.email],
            html_message=message
        )


class AccountActivateView(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        is_token_valid = account_activation_token.check_token(user, token)
        if user is not None and is_token_valid:
            self.__activate_user(user)
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('account_activation_invalid'))

    def __activate_user(self, user):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()


class OnlyAuthenticatedView(TemplateView):

    @method_decorator(login_required(login_url="/"))
    def dispatch(self, *args, **kwargs):
        return super(TemplateView, self).dispatch(*args, **kwargs)
