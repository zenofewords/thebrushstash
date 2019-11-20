from decimal import Decimal

from rest_framework import (
    response,
    status,
)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from shop.api.serializers import (
    PaymentMethodSerializer,
    ProductSeriazlier,
    SimpleProductSerializer,
    UserInformationSerializer,
)
from shop.constants import EMPTY_BAG
from shop.models import InvoicePaymentMethod
from thebrushstash.constants import (
    DEFAULT_CURRENCY,
    DEFAULT_SHIPPING_COST,
    ipg_fields,
    form_mandatory_fields,
)
from thebrushstash.utils import (
    create_or_update_invoice,
    get_cart,
    get_signature,
    register_user,
    subscribe_to_newsletter,
)
from thebrushstash.models import Region


class AddToBagView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ProductSeriazlier

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_data = serializer.data
        quantity = product_data.get('quantity')
        price = product_data.get('price')
        subtotal = quantity * price

        bag = request.session.get('bag')
        products = bag.get('products')
        shipping_cost = Decimal(bag.get('shipping_cost'))

        product = None
        product_id = product_data.get('slug')
        if product_id in products:
            product = products[product_id]
            products[product_id] = {
                'pk': product_data.get('pk'),
                'name': product_data.get('name'),
                'price': str(price),
                'quantity': product.get('quantity') + quantity,
                'subtotal': str(Decimal(product.get('subtotal')) + subtotal),
                'image_url': product.get('image_url'),
            }
        else:
            product = {
                'pk': product_data.get('pk'),
                'name': product_data.get('name'),
                'price': str(price),
                'quantity': quantity,
                'subtotal': str(subtotal),
                'image_url': product_data.get('image_url'),
            }
            products[product_id] = product

        total = Decimal(bag['total']) + Decimal(subtotal)
        bag = {
            'products': products,
            'total': str(total),
            'total_quantity': bag['total_quantity'] + quantity,
            'shipping_cost': str(shipping_cost),
            'grand_total': str(total + shipping_cost),
        }
        request.session['bag'] = bag
        return response.Response({'bag': bag}, status=status.HTTP_200_OK)


class RemoveFromBagView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SimpleProductSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bag = request.session.get('bag')
        products = bag.get('products')
        product_id = serializer.data.get('slug')

        if product_id in products:
            product = products[product_id]
            bag['total'] = str(Decimal(bag['total']) - Decimal(product.get('subtotal', 0)))
            bag['total_quantity'] = bag['total_quantity'] - product.get('quantity')
            bag['grand_total'] = str(
                Decimal(bag['grand_total']) - Decimal(product.get('subtotal', 0))
            )
            del products[product_id]

        request.session['bag'] = bag
        return response.Response({'bag': bag}, status=status.HTTP_200_OK)


class UpdatePaymentMethodView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PaymentMethodSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        gls_fee = Decimal('10.00')
        request.session['payment_method'] = serializer.data.get('payment_method')
        total = Decimal(request.session['bag']['total'])
        shipping_cost = Decimal(request.session['bag']['shipping_cost'])
        grand_total = total + shipping_cost

        if request.session['payment_method'] == InvoicePaymentMethod.CASH_ON_DELIVERY:
            request.session['bag']['fees'] = str(gls_fee)
            grand_total = total + shipping_cost + gls_fee
        else:
            request.session['bag']['fees'] = None
        request.session['bag']['grand_total'] = str(grand_total)
        request.session.modified = True

        return response.Response({
            'bag': request.session['bag'],
            'payment_method': request.session['payment_method']
        }, status=status.HTTP_200_OK)


class ProcessOrderView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserInformationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_site = get_current_site(request)
        user = register_user(serializer.data, current_site)
        subscribe_to_newsletter(user, serializer.data, current_site)

        bag = request.session.get('bag')
        cart = get_cart(bag)
        request.session['order_number'] = create_or_update_invoice(
            request.session.get('order_number'),
            user,
            cart,
            serializer.data,
            request.session.get('payment_method', '')
        )
        request.session['user_information'] = serializer.data
        order_number = request.session.get('order_number')
        grand_total = Decimal(bag.get('total')) + Decimal(bag.get('shipping_cost'))

        user_info = {}
        for key, ipg_key in dict(zip(form_mandatory_fields, ipg_fields)).items():
            if key in form_mandatory_fields:
                user_info[ipg_key] = serializer.data[key]
        language = request.session.get('_language')

        return response.Response({
            'order_number': order_number,
            'cart': cart,
            'grand_total': str(grand_total),
            'user_information': serializer.data,
            'region': request.session.get('region'),
            'language': language,
            'signature': get_signature({
                'amount': str(grand_total),
                **user_info,  # noqa
                'cart': cart,
                'currency': DEFAULT_CURRENCY,
                'language': language,
                'order_number': order_number,
                'require_complete': 'false',
                'store_id': settings.IPG_STORE_ID,
                'version': settings.IPG_API_VERSION,
            }),
        }, status=status.HTTP_200_OK)
