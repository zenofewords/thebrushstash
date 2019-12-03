from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import (
    FormView,
    TemplateView,
)

from account.forms import (
    PasswordForm,
    RegistrationForm,
)
from account.models import (
    CustomUser,
    NewsletterRecipient,
)
from account.tokens import account_activation_token
from thebrushstash.utils import send_registration_email


class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:verification-sent')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.is_active = False
        user.save()

        send_registration_email(user, get_current_site(self.request))
        return super().form_valid(form)


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


class SubscribeToNewsletterView(TemplateView):
    template_name = 'account/subscribe_to_newsletter.html'

    def get(self, request, *args, **kwargs):
        try:
            self.newsletter_recipient = NewsletterRecipient.objects.get(
                email=force_text(urlsafe_base64_decode(kwargs.get('uidb64')))
            )
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            self.newsletter_recipient = None

        if self.newsletter_recipient:
            self.newsletter_recipient.subscribed = True
            self.newsletter_recipient.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'newsletter_recipient': self.newsletter_recipient,
        })
        return context
