from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import (
    DetailView,
    FormView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.utils.text import slugify

from account.forms import AddressForm
from account.models import (
    NewsletterRecipient,
)
from shop.constants import EMPTY_BAG
from shop.models import (
    Invoice,
    Product,
)
from thebrushstash.utils import (
    get_cart,
    get_signature,
    send_purchase_mail,
)


class CheckoutView(FormView):
    template_name = 'shop/checkout.html'
    form_class = AddressForm
    success_url = reverse_lazy('shop:purchase-complete')

    def get_initial(self):
        user = self.request.user
        session_user_information = self.request.session.get('user_information')

        if session_user_information:
            return session_user_information

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
        self.update_invoice(self.request.session['invoice_id'], form.cleaned_data)
        send_purchase_mail(form.cleaned_data.get('email'), get_current_site(self.request))
        self.request.session['bag'] = EMPTY_BAG
        self.request.session['invoice_id'] = ''

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.request.session

        subscribed_to_newsletter = False
        user = self.request.user
        if user.is_authenticated:
            subscribed_to_newsletter = NewsletterRecipient.objects.filter(user=user).first()

        bag = session.get('bag')
        invoice_id = session.get('invoice_id')
        grand_total = bag.get('grand_total')
        cart = get_cart(bag)
        context.update({
            'bag': session.get('bag'),
            'region': session.get('region'),
            'subscribed_to_newsletter': subscribed_to_newsletter,
            'invoice_id': invoice_id,
            'grand_total': grand_total,
            'cart': cart,
            'signature': get_signature(invoice_id, grand_total, cart),
        })
        return context

    def update_invoice(self, invoice_id, data):
        invoice = Invoice.objects.filter(pk=invoice_id).first()

        if invoice:
            invoice.payment_method = 'on-delivery'
            invoice.save()


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
