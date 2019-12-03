import operator
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
from shop.constants import (
    DEFAULT_SHIPPING_COST,
    GLS_FEE,
    EMPTY_BAG,
)
from shop.models import InvoicePaymentMethod
from shop.utils import (
    get_grandtotals,
    get_totals,
    set_shipping_cost,
    set_tax,
)
from thebrushstash.constants import (
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

        bag = request.session.get('bag')
        products = bag.get('products')
        quantity = serializer.data.get('quantity')

        product = None
        product_slug = serializer.data.get('slug')
        if product_slug in products:
            product = products[product_slug]
            products[product_slug].update({
                'quantity': product.get('quantity') + quantity,
                **get_totals(serializer.data, 'subtotal', operator.add, product),  # noqa
            })
        else:
            product = {
                'pk': serializer.data.get('pk'),
                'name': serializer.data.get('name'),
                'quantity': quantity,
                **get_totals(serializer.data, 'subtotal', operator.add),
                'image_url': serializer.data.get('image_url'),
            }
            products[product_slug] = product

        bag.update({
            'products': products,
            'total_quantity': bag['total_quantity'] + quantity,
            **get_totals(serializer.data, 'total', operator.add, bag),
        })
        set_shipping_cost(bag, request.session['region'])
        set_tax(bag, request.session['currency'])
        bag.update(
            **get_grandtotals(bag),
        )
        request.session['bag'] = bag
        return response.Response({
            'bag': bag,
            'currency': request.session['currency'],
        }, status=status.HTTP_200_OK)


class RemoveFromBagView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SimpleProductSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bag = request.session.get('bag')
        products = bag.get('products')
        product_slug = serializer.data.get('slug')

        if product_slug in products:
            product = products[product_slug]
            bag.update({
                'total_quantity': bag['total_quantity'] - product.get('quantity'),
                **get_totals(product, 'total', operator.sub, bag),
            })
            set_shipping_cost(bag, request.session['region'])
            set_tax(bag, request.session['currency'])
            bag.update({
                **get_grandtotals(bag),
            })
            del products[product_slug]

        if len(products.items()) == 0:
            bag = EMPTY_BAG

        request.session['bag'] = bag
        return response.Response({
            'bag': bag,
            'cart': get_cart(bag),
            'currency': request.session['currency'],
        }, status=status.HTTP_200_OK)


class UpdateBagView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SimpleProductSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bag = request.session.get('bag')
        products = bag.get('products')
        product_slug = serializer.data.get('slug')

        if product_slug in products:
            product = products[product_slug]

            if serializer.data.get('action') == 'increment':
                product['quantity'] = product['quantity'] + 1
                bag['total_quantity'] = bag['total_quantity'] + 1

                product.update({
                    **get_totals(product, 'subtotal', operator.add, product, 1),
                })
                bag.update({
                    **get_totals(product, 'total', operator.add, bag, 1)
                })

            elif serializer.data.get('action') == 'decrement':
                product['quantity'] = product['quantity'] - 1
                bag['total_quantity'] = bag['total_quantity'] - 1

                if product['quantity'] <= 0:
                    del products[product_slug]

                product.update({
                    **get_totals(product, 'subtotal', operator.sub, product, 1),
                })
                bag.update({
                    **get_totals(product, 'total', operator.sub, bag, 1)
                })

            set_shipping_cost(bag, request.session['region'])
            set_tax(bag, request.session['currency'])

            bag.update({
                **get_grandtotals(bag)
            })
            bag['products'] = products
            request.session['bag'] = bag if bag['total_quantity'] > 0 else EMPTY_BAG
            request.session.modified = True
        return response.Response({
            'bag': request.session['bag'],
            'cart': get_cart(request.session['bag']),
            'currency': request.session['currency'],
        }, status=status.HTTP_200_OK)


class ProcessOrderView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserInformationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_site = get_current_site(request)
        user = register_user(serializer.data, current_site)
        subscribe_to_newsletter(user, serializer.data)

        session = request.session
        bag = session.get('bag')
        cart = get_cart(bag)
        session['order_number'] = create_or_update_invoice(
            session.get('order_number'),
            user,
            cart,
            serializer.data,
            session.get('payment_method', '')
        )
        session['user_information'] = serializer.data

        user_info = {}
        for key, ipg_key in dict(zip(form_mandatory_fields, ipg_fields)).items():
            if key in form_mandatory_fields:
                user_info[ipg_key] = serializer.data[key]

        return response.Response({
            'order_number': session['order_number'],
            'cart': cart,
            'grand_total_hrk': bag['grand_total_hrk'],
            'user_information': session['user_information'],
            'region': session['region'],
            'language': session['_language'],
            'signature': get_signature({
                'amount': bag['grand_total_hrk'],  # this value must stay in hrk
                **user_info,  # noqa
                'cart': cart,
                'currency': 'HRK',
                'language': session['_language'],
                'order_number': session['order_number'],
                'require_complete': 'false',
                'store_id': settings.IPG_STORE_ID,
                'version': settings.IPG_API_VERSION,
            }),
        }, status=status.HTTP_200_OK)


class UpdatePaymentMethodView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PaymentMethodSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = request.session

        total_hrk = Decimal(session['bag']['total_hrk'])
        shipping_cost_hrk = Decimal(session['bag']['shipping_cost_hrk'])
        fee = session['bag'].get('fees')
        session['payment_method'] = serializer.data.get('payment_method')

        if session['payment_method'] == InvoicePaymentMethod.CASH_ON_DELIVERY:
            session['bag']['fees'] = str(GLS_FEE)
            grand_total = total_hrk + shipping_cost_hrk + GLS_FEE
        else:
            session['bag']['fees'] = 0
            grand_total = total_hrk + shipping_cost_hrk

        session['bag']['grand_total_hrk'] = str(grand_total)
        session.modified = True

        return response.Response({
            'bag': session['bag'],
            'currency': session['currency'],
            'payment_method': session['payment_method'],
        }, status=status.HTTP_200_OK)
