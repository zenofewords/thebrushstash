from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.views.generic.list import ListView
from django.views.generic import (
    DetailView,
    FormView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify

from account.forms import AddressForm
from account.models import (
    CustomUser,
    NewsletterRecipient,
)
from account.tokens import account_activation_token
from shop.constants import EMPTY_BAG
from shop.models import (
    Invoice,
    Product,
)


class CheckoutView(FormView):
    template_name = 'shop/checkout.html'
    form_class = AddressForm
    success_url = reverse_lazy('shop:purchase-complete')

    def get_initial(self):
        user = self.request.user

        if user.is_authenticated:
            return {
                'full_name': user.full_name,
                'email': user.email,
                'country': user.country,
                'address': user.address,
                'city': user.city,
                'state_county': user.state_county,
                'zip_code': user.zip_code,
                'company_name': user.company_name,
                'company_address': user.company_address,
                'company_uin': user.company_uin,
            }
        return {}

    def form_valid(self, form):
        user = self.register_user(form.cleaned_data)
        self.subscribe_to_newsletter(user, form.cleaned_data.get('email'))
        self.create_invoice(user, form.cleaned_data)
        self.send_purchase_mail(form.cleaned_data.get('email'))
        self.request.session['bag'] = EMPTY_BAG

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.request.session

        subscribed_to_newsletter = False
        user = self.request.user
        if user.is_authenticated:
            subscribed_to_newsletter = NewsletterRecipient.objects.filter(user=user).first()

        context.update({
            'bag': session.get('bag'),
            'region': session.get('region'),
            'subscribed_to_newsletter': subscribed_to_newsletter,
        })
        return context

    def update_user_information(self, user, email, data):
        user.username = email
        user.email = email
        user.full_name = data.get('full_name')
        user.country = data.get('country')
        user.city = data.get('city')
        user.address = data.get('address')
        user.state_county = data.get('state_county')
        user.zip_code = data.get('zip_code')
        user.company_name = data.get('company_name')
        user.company_address = data.get('company_address')
        user.company_uin = data.get('company_uin')
        user.save()

    def register_user(self, data):
        email = data.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            self.update_user_information(user, email, data)
        elif data.get('register') and email:
            user = CustomUser()
            user.is_active = False

            self.update_user_information(user, email, data)
            self.send_registration_email(user)
            return user
        return user

    def subscribe_to_newsletter(self, user, email):
        obj, created = NewsletterRecipient.objects.get_or_create(
            email=email,
            defaults={
                'subscribed': True,
                'user': user,
            }
        )
        if user and not created and not obj.user:
            obj.user = user
            obj.save()
        if created:
            self.send_subscription_email(email)

    def create_invoice(self, user, data):
        invoice = Invoice()

        invoice.email = data.get('email')
        invoice.full_name = data.get('full_name')
        invoice.country = data.get('country')
        invoice.city = data.get('city')
        invoice.address = data.get('address')
        invoice.state_county = data.get('state_county')
        invoice.zip_code = data.get('zip_code')
        invoice.company_name = data.get('company_name')
        invoice.company_address = data.get('company_address')
        invoice.company_uin = data.get('company_uin')

        invoice.note = data.get('note')
        invoice.payment_method = 'on-delivery'
        invoice.status = 'pending'
        invoice.user = user
        invoice.save()

    def send_registration_email(self, user):
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
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

    def send_subscription_email(self, email_address):
        current_site = get_current_site(self.request)
        mail_subject = 'Subscribed to newsletter'
        message = render_to_string('shop/subscribed_to_newsletter_email.html', {
            'domain': current_site.domain,
            'site_name': current_site.name,
            'protocol': 'http' if settings.DEBUG else 'https',
        })
        EmailMessage(mail_subject, message, to=[email_address]).send()

    def send_purchase_mail(self, email_address):
        current_site = get_current_site(self.request)
        mail_subject = 'Purchase complete'
        message = render_to_string('shop/purchase_complete_email.html', {
            'domain': current_site.domain,
            'site_name': current_site.name,
            'protocol': 'http' if settings.DEBUG else 'https',
        })
        EmailMessage(mail_subject, message, to=[email_address]).send()


class PurchaseCompleteView(TemplateView):
    template_name = 'shop/purchase_complete.html'


class ReviewBagView(TemplateView):
    template_name = 'shop/review_bag.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.request.session
        context.update({
            'bag': session.get('bag'),
            'region': session.get('region'),
        })
        return context


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        self.selected_item_id = slugify(request.GET.get('gallery-item', 0))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'selected_item_id': self.selected_item_id,
            'other_products': Product.published_objects.exclude(id=self.object.pk)[:3]
        })
        return context


class ShopHomeView(TemplateView):
    template_name = 'shop/shop_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'products': Product.published_objects.all(),
        })
        return context
