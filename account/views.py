from django.conf import settings
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import (
    FormView,
    TemplateView,
)

from account.forms import (
    PasswordForm,
    RegistrationForm,
)
from account.models import CustomUser
from account.tokens import account_activation_token


class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:verification-sent')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.is_active = False
        user.save()

        self.send_mail(user)
        return super().form_valid(form)

    def send_mail(self, user):
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account'
        message = render_to_string('account/account_verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'site_name': current_site.name,
            'protocol': 'http' if settings.DEBUG else 'https',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()


class VerificationSentView(TemplateView):
    template_name = 'account/confirmation_sent.html'


class ActivateAccountView(FormView):
    form_class = PasswordForm
    template_name = 'account/activate.html'
    success_url = reverse_lazy('shop:shop')

    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(
                pk=force_text(urlsafe_base64_decode(kwargs.get('uidb64')))
            )
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, kwargs.get('token')):
            user.is_active = True
            user.save()
            login(self.request, user)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'authenticated': self.request.user.is_authenticated,
        })
        return context
