from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    DetailView,
    FormView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify

from account.forms import AddressForm
from account.models import (
    NewsletterRecipient,
)
from shop.constants import EMPTY_BAG
from shop.models import (
    Invoice,
    InvoiceStatus,
    Product,
)
from thebrushstash.utils import signature_is_valid


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
                'first_name': user.first_name,
                'last_name': user.last_name,
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


# corvus forces a POST redirect which will not contain but requires the csrf token
@method_decorator(csrf_exempt, name='dispatch')
class PurchaseCompletedView(TemplateView):
    template_name = 'shop/purchase_completed.html'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if signature_is_valid(request.POST):
            invoice = Invoice.objects.filter(order_number=request.POST.get('order_number')).first()

            if invoice:
                invoice.status = InvoiceStatus.PAID
                invoice.save()

            request.session['bag'] = EMPTY_BAG
            request.session['order_number'] = None

        return render(
            request,
            self.template_name,
            {'user_information': request.session['user_information']}
        )


# corvus forces a POST redirect which will not contain but requires the csrf token
@method_decorator(csrf_exempt, name='dispatch')
class PurchaseCancelledView(TemplateView):
    template_name = 'shop/purchase_cancelled.html'
    http_method_names = ['get', 'post']

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
