from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    DetailView,
    FormView,
    TemplateView,
)
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify

from account.forms import AddressForm
from account.models import (
    NewsletterRecipient,
)
from shop.constants import GLS_FEE
from shop.models import (
    Invoice,
    InvoicePaymentMethod,
    InvoiceStatus,
    Product,
)
from thebrushstash.models import ExchangeRate
from thebrushstash.utils import (
    complete_purchase,
    signature_is_valid,
)


class CheckoutView(FormView):
    template_name = 'shop/checkout.html'
    form_class = AddressForm
    success_url = reverse_lazy('shop:purchase-completed')

    def get(self, request, *args, **kwargs):
        if not request.session.get('bag'):
            return redirect(reverse('shop:shop'))
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        user = self.request.user
        session_user_information = self.request.session.get('user_information')

        if session_user_information:
            session_user_information.pop('company_name', None)
            session_user_information.pop('company_address', None)
            session_user_information.pop('company_uin', None)
            return session_user_information

        if user.is_authenticated:
            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'country': user.country,
                'address': user.address,
                'city': user.city,
                'phone_number': user.phone_number,
                'state_county': user.state_county,
                'zip_code': user.zip_code,
            }
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.request.session

        subscribed_to_newsletter = False
        user = self.request.user
        if user.is_authenticated:
            subscribed_to_newsletter = NewsletterRecipient.objects.filter(user=user).first()

        exchange_rates = {}
        for exchange_rate in ExchangeRate.objects.all():
            exchange_rates[exchange_rate.currency.lower()] = exchange_rate.middle_rate

        context.update({
            'api_version': settings.IPG_API_VERSION,
            'bag': session.get('bag'),
            'region': session.get('region'),
            'language': session.get('_language'),
            'currency': session.get('currency'),
            'ipg_url': settings.IPG_URL,
            'store_id': settings.IPG_STORE_ID,
            'require_complete': settings.IPG_REQUIRE_COMPLETE,
            'subscribed_to_newsletter': subscribed_to_newsletter,
            'gls_fee': GLS_FEE,
            'exchange_rates': exchange_rates,
        })
        return context


class PurchaseCompletedView(TemplateView):
    template_name = 'shop/purchase_completed.html'

    def post(self, request, *args, **kwargs):
        session = request.session

        user_information = {}
        if session['payment_method'] == InvoicePaymentMethod.CASH_ON_DELIVERY:
            complete_purchase(session, InvoiceStatus.PROCESSED, request)
            user_information = {'user_information': session['user_information']}
        return render(request, self.template_name, user_information)


# IPG forces a POST redirect which will not contain but requires the csrf token
@method_decorator(csrf_exempt, name='dispatch')
class IPGPurchaseCompletedView(TemplateView):
    template_name = 'shop/purchase_completed.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user_information = {}

        if signature_is_valid(request.POST):
            session = request.session
            complete_purchase(session, InvoiceStatus.PAID, request)
            user_information = {'user_information': session['user_information']}
        return render(request, self.template_name, user_information)


# IPG forces a POST redirect which will not contain but requires the csrf token
@method_decorator(csrf_exempt, name='dispatch')
class IPGPurchaseCancelledView(TemplateView):
    template_name = 'shop/purchase_cancelled.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        invoice = Invoice.objects.filter(order_number=request.POST.get('order_number')).first()

        if invoice:
            invoice.status = InvoiceStatus.CANCELLED
            invoice.save()
        return render(request, self.template_name)


class ReviewBagView(TemplateView):
    template_name = 'shop/review_bag.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('bag'):
            return redirect(reverse('shop:shop'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.request.session

        exchange_rates = {}
        for exchange_rate in ExchangeRate.objects.all():
            exchange_rates[exchange_rate.currency.lower()] = exchange_rate.middle_rate

        context.update({
            'bag': session.get('bag'),
            'region': session.get('region'),
            'currency': session.get('currency'),
            'exchange_rates': exchange_rates,
        })
        return context


class ProductDetailView(DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        self.selected_item_id = slugify(request.GET.get('gallery-item', 0))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'selected_item_id': self.selected_item_id,
            'currency': self.request.session.get('currency'),
            'other_products': Product.published_objects.exclude(id=self.object.pk)[:3]
        })
        return context


class ShopHomeView(TemplateView):
    template_name = 'shop/shop_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'products': Product.published_objects.all(),
            'currency': self.request.session.get('currency'),
            'full_site_url': '{}://{}'.format(self.request.scheme, get_current_site(self.request)),
        })
        return context
