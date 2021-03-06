from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
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
from shop.constants import (
    GLS_FEE,
    STUDIO_ADDRESS,
)
from shop.models import (
    Invoice,
    InvoiceItem,
    InvoicePaymentMethod,
    InvoiceStatus,
    Product,
    Review,
)
from shop.utils import (
    get_price_with_currency,
    set_shipping_cost,
    update_bag_with_discount,
)
from thebrushstash.models import ExchangeRate
from thebrushstash.utils import (
    complete_purchase,
    get_user_information,
    restore_session_from_invoice,
    signature_is_valid,
)


class CheckoutView(FormView):
    template_name = 'shop/checkout.html'
    form_class = AddressForm
    success_url = reverse_lazy('purchase-completed')

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

        country_name = None
        user_information = session.get('user_information')

        if user_information:
            country_name = user_information.get('country')
        elif user.is_authenticated and user.country:
            country_name = user.country.name
        bag = session.get('bag')
        set_shipping_cost(bag, session['region'], country_name)

        currency = session.get('currency')
        gls_fee = '{:0.2f}'.format(GLS_FEE / exchange_rates[currency], 2)

        if bag.get('promo_code'):
            update_bag_with_discount(bag, bag.get('promo_code'), self.request.session)

        context.update({
            'api_version': settings.IPG_API_VERSION,
            'bag': bag,
            'region': session.get('region'),
            'language': session.get(settings.LANG_COOKIE_NAME_INTERNAL),
            'currency': currency,
            'ipg_url': settings.IPG_URL,
            'store_id': settings.IPG_STORE_ID,
            'require_complete': settings.IPG_REQUIRE_COMPLETE,
            'payment_all_dynamic': settings.IPG_PAYMENT_ALL_DYNAMIC,
            'subscribed_to_newsletter': subscribed_to_newsletter,
            'gls_fee': get_price_with_currency(gls_fee, currency),
            'exchange_rates': exchange_rates,
            'studio_address': STUDIO_ADDRESS,
        })
        return context


class PurchaseCompletedView(TemplateView):
    template_name = 'shop/purchase_completed.html'

    def post(self, request, *args, **kwargs):
        user_information = {}

        if request.POST.get('payment-method') == InvoicePaymentMethod.CASH_ON_DELIVERY:
            invoice = complete_purchase(request.POST.get('order_number'), InvoiceStatus.PROCESSED, request)
            user_information = {
                'user_information': get_user_information(request, invoice)
            }
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
            invoice = complete_purchase(request.POST.get('order_number'), InvoiceStatus.PAID, request)
            user_information = {
                'user_information': get_user_information(request, invoice)
            }
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
            restore_session_from_invoice(request, invoice)
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

        bag = session.get('bag')
        set_shipping_cost(bag, session['region'])

        context.update({
            'bag': bag,
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

        can_review = False
        if self.request.user.is_authenticated:
            bought_the_item = InvoiceItem.objects.filter(
                product=self.object, invoice__user=self.request.user
            ).exists()
            already_reviewed = Review.objects.filter(
                product=self.object, user=self.request.user
            )
            can_review = bought_the_item and not already_reviewed

        context.update({
            'selected_item_id': self.selected_item_id,
            'currency': self.request.session.get('currency'),
            'other_products': Product.published_objects.exclude(id=self.object.pk)[:3],
            'reviews': Review.published_objects.filter(product=self.object),
            'can_review': can_review,
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


class ShopHomePreviewView(TemplateView):
    template_name = 'shop/shop_base.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'products': Product.objects.all(),
            'currency': self.request.session.get('currency'),
            'full_site_url': '{}://{}'.format(self.request.scheme, get_current_site(self.request)),
        })
        return context
