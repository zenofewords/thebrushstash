from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import (
    FormView,
    TemplateView,
)
from django.utils.translation import gettext as _


from account.forms import (
    PasswordForm,
    RegistrationForm,
)
from account.models import (
    CustomUser,
    LanguagePreference,
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

    def form_invalid(self, form):
        user = CustomUser.objects.filter(email=form.data.get('email')).first()
        if user and not user.is_active:
            form.add_error('email', _(
                'Since your account was never activated, we\'ve emailed you a new activation link.'
            ))
            send_registration_email(user, get_current_site(self.request))
        return super().form_invalid(form)


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


class UnsubscribeFromNewsletter(TemplateView):
    template_name = 'account/unsubscribe_from_newsletter.html'

    def get(self, request, *args, **kwargs):
        try:
            self.newsletter_recipient = NewsletterRecipient.objects.get(token=request.GET.get('token'))
            self.newsletter_recipient.subscribed = False
            self.newsletter_recipient.save()
        except Exception:
            self.newsletter_recipient = None
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'newsletter_recipient': self.newsletter_recipient,
        })
        return context


class SetNewsletterLanguage(TemplateView):
    template_name = 'account/set_newsletter_language.html'

    def get_verbose_language_preference(self):
        for code, language in LanguagePreference.CHOICES:
            if code == self.preference:
                return language

    def get(self, request, *args, **kwargs):
        try:
            self.newsletter_recipient = NewsletterRecipient.objects.get(token=request.GET.get('token'))
            self.preference = request.GET.get('language_preference')

            if self.preference in [x[0] for x in LanguagePreference.CHOICES]:
                self.newsletter_recipient.language_preference = self.preference
            self.newsletter_recipient.save()
        except Exception:
            self.newsletter_recipient = None
            self.preference = None
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'newsletter_recipient': self.newsletter_recipient,
            'language_preference': self.get_verbose_language_preference(),
        })
        return context


class LoginOverrideView(LoginView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        user = CustomUser.objects.filter(email=form.data.get('username')).first()
        if user and not user.is_active:
            form.add_error('username', _(
                '''You've never activated your account. The activation link was sent to your email when you
                registered your account. If you can't find the link, go to "register here" to request a new one.
                '''
            ))
        elif user and user.password == '':
            form.add_error('password', _(
                'You\'ve never set a password. Click the "Forgot your password?" link to request a reset.'
            ))
        return self.render_to_response(self.get_context_data(form=form))
