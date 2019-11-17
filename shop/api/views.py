from decimal import Decimal

from rest_framework import (
    response,
    status,
)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from django.contrib.sites.shortcuts import get_current_site

from shop.api.serializers import (
    PaymentMethodSerializer,
    ProductSeriazlier,
    SimpleProductSerializer,
    UserInformationSerializer,
)
from shop.constants import EMPTY_BAG
from shop.models import InvoicePaymentMethod
from thebrushstash.utils import (
    create_or_update_invoice,
    get_cart,
    get_signature,
    register_user,
    subscribe_to_newsletter,
)


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
        shipping = Decimal(10.0)

        products = {}
        bag = EMPTY_BAG
        if request.session.get('bag'):
            bag = request.session.get('bag')
            products = bag.get('products')

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
            'shipping': str(shipping),
            'grand_total': str(total + shipping),
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

        gls_fee = Decimal(10.0)

        request.session['payment_method'] = serializer.data.get('payment_method')
        total = Decimal(request.session['bag']['total'])
        shipping = Decimal(request.session['bag']['shipping'])
        grand_total = total + shipping

        if request.session['payment_method'] == InvoicePaymentMethod.CASH_ON_DELIVERY:
            request.session['bag']['fees'] = str(gls_fee)
            grand_total = total + shipping + gls_fee
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
        grand_total = bag.get('grand_total')

        return response.Response({
            'order_number': order_number,
            'cart': cart,
            'grand_total': grand_total,
            'user_information': serializer.data,
            'region': request.session.get('region'),
            'signature': get_signature(
                order_number,
                grand_total,
                cart,
                serializer.data
            ),
        }, status=status.HTTP_200_OK)
