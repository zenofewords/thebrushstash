import operator
from decimal import Decimal

from rest_framework import (
    response,
    status,
)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from django.conf import settings

from shop.api.serializers import (
    PaymentMethodSerializer,
    ProductSerializer,
    SimpleProductSerializer,
    UserInformationSerializer,
    ShippingAddressSerializer,
    ShippingCostSerializer,
)
from shop.constants import (
    GLS_FEE,
    EMPTY_BAG,
)
from shop.models import (
    InvoicePaymentMethod,
    Invoice,
)
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
    get_country,
)
from thebrushstash.models import (
    ExchangeRate,
    Region,
)


class AddToBagView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ProductSerializer

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
        currency = request.session['currency']
        exchange_rate = ExchangeRate.objects.get(currency=currency.upper()).middle_rate

        bag.update(**get_grandtotals(bag))
        request.session['bag'] = bag
        return response.Response({
            'bag': bag,
            'currency': currency,
            'exchange_rate': exchange_rate,
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

            bag.update({**get_grandtotals(bag)})
            del products[product_slug]

        if len(products.items()) == 0:
            bag = EMPTY_BAG

        currency = request.session['currency']
        exchange_rate = ExchangeRate.objects.get(currency=currency.upper()).middle_rate

        request.session['bag'] = bag
        return response.Response({
            'bag': bag,
            'cart': get_cart(bag),
            'currency': currency,
            'exchange_rate': exchange_rate,
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

                product.update({**get_totals(product, 'subtotal', operator.add, product, 1)})
                bag.update({**get_totals(product, 'total', operator.add, bag, 1)})

            elif serializer.data.get('action') == 'decrement':
                product['quantity'] = product['quantity'] - 1
                bag['total_quantity'] = bag['total_quantity'] - 1

                if product['quantity'] <= 0:
                    del products[product_slug]

                product.update({**get_totals(product, 'subtotal', operator.sub, product, 1)})
                bag.update({**get_totals(product, 'total', operator.sub, bag, 1)})

            set_shipping_cost(bag, request.session['region'])
            set_tax(bag)

            bag.update({**get_grandtotals(bag)})
            bag['products'] = products
            request.session['bag'] = bag if bag['total_quantity'] > 0 else EMPTY_BAG
            request.session.modified = True

        currency = request.session['currency']
        exchange_rate = ExchangeRate.objects.get(currency=currency.upper()).middle_rate

        return response.Response({
            'bag': request.session['bag'],
            'cart': get_cart(request.session['bag']),
            'currency': currency,
            'exchange_rate': exchange_rate,
        }, status=status.HTTP_200_OK)


class ProcessOrderView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserInformationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, active = register_user(serializer.data)
        created = subscribe_to_newsletter(user, serializer.data)

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
        session['user_information']['registration_email_in_use'] = active
        session['user_information']['newsletter_email_in_use'] = not created

        user_info = {}
        for key, ipg_key in dict(zip(form_mandatory_fields, ipg_fields)).items():
            if key in form_mandatory_fields:
                user_info[ipg_key] = serializer.data[key]

        return response.Response({
            'order_number': session['order_number'],
            'cart': cart,
            'grand_total': bag['grand_total'],
            'user_information': session['user_information'],
            'region': session['region'],
            'language': session['_language'],
            'signature': get_signature({
                'amount': bag['grand_total'],
                **user_info,  # noqa
                'cart': cart,
                'currency': 'HRK',
                'language': session['_language'],
                'order_number': session['order_number'],
                'require_complete': settings.IPG_REQUIRE_COMPLETE,
                'store_id': settings.IPG_STORE_ID,
                'version': settings.IPG_API_VERSION,
            }),
        }, status=status.HTTP_200_OK)


class UpdateShippingAddressView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ShippingAddressSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_number = request.session['order_number']

        invoice = Invoice.objects.get(order_number=order_number)
        invoice.shipping_first_name = serializer.data.get('shipping_first_name', '')
        invoice.shipping_last_name = serializer.data.get('shipping_last_name', '')
        invoice.invoice_shipping_country = get_country(
            serializer.data.get('account_shipping_country', '')
        )
        invoice.shipping_city = serializer.data.get('shipping_city', '')
        invoice.shipping_address = serializer.data.get('shipping_address', '')
        invoice.shipping_zip_code = serializer.data.get('shipping_zip_code', '')
        invoice.save()

        session = request.session
        bag = session.get('bag')
        cart = get_cart(bag)

        user_info = {}
        for key, ipg_key in dict(zip(form_mandatory_fields, ipg_fields)).items():
            if key in form_mandatory_fields:
                user_info[ipg_key] = session['user_information'][key]

        return response.Response({
            'order_number': order_number,
            'grand_total': bag['grand_total'],
            'signature': get_signature({
                'amount': bag['grand_total'],
                **user_info,  # noqa
                'cart': cart,
                'currency': 'HRK',
                'language': session['_language'],
                'order_number': session['order_number'],
                'require_complete': settings.IPG_REQUIRE_COMPLETE,
                'store_id': settings.IPG_STORE_ID,
                'version': settings.IPG_API_VERSION,
            }),
        }, status=status.HTTP_200_OK)


class UpdateShippingCostView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ShippingCostSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bag = request.session.get('bag')
        set_shipping_cost(
            bag,
            request.session['region'],
            serializer.data.get('country_name')
        )
        currency = request.session['currency']
        exchange_rate = ExchangeRate.objects.get(currency=currency.upper()).middle_rate

        request.session['bag'] = bag
        return response.Response({
            'bag': bag,
            'currency': currency,
            'exchange_rate': exchange_rate,
        }, status=status.HTTP_200_OK)


class UpdatePaymentMethodView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PaymentMethodSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = request.session

        total = Decimal(session['bag'].get('total'))
        shipping_cost = Decimal(session['bag']['shipping_cost'])
        fee = session['bag'].get('fees')
        session['payment_method'] = serializer.data.get('payment_method')

        if session['payment_method'] == InvoicePaymentMethod.CASH_ON_DELIVERY:
            session['bag']['fees'] = str(GLS_FEE)
            grand_total = total + shipping_cost + GLS_FEE
        else:
            session['bag']['fees'] = 0
            grand_total = total + shipping_cost

        session['bag']['grand_total'] = str(grand_total)
        session.modified = True
        currency = request.session['currency']
        exchange_rate = ExchangeRate.objects.get(currency=currency.upper()).middle_rate

        return response.Response({
            'bag': session['bag'],
            'currency': currency,
            'exchange_rate': exchange_rate,
            'payment_method': session['payment_method'],
        }, status=status.HTTP_200_OK)
