import operator
from decimal import Decimal

from rest_framework import (
    response,
    status,
)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext as _

from shop.api.serializers import (
    CountryNameSerializer,
    PaymentMethodSerializer,
    ProductSerializer,
    PromoCodeSerializer,
    ReviewSerializer,
    ShippingAddressSerializer,
    SimpleProductSerializer,
    UserInformationSerializer,
)
from shop.constants import (
    GLS_FEE,
    EMPTY_BAG,
)
from shop.models import (
    InvoicePaymentMethod,
    Invoice,
    Product,
    PromoCode,
    Review,
)
from shop.utils import (
    apply_discount,
    get_grandtotals,
    get_totals,
    set_shipping_cost,
    set_tax,
    update_bag_with_discount,
    update_discount,
)
from thebrushstash.constants import (
    DEFAULT_COUNTRY,
    ipg_fields,
    form_mandatory_fields,
)
from thebrushstash.utils import (
    assemble_order_response,
    create_or_update_invoice,
    get_cart,
    get_country,
    register_user,
    subscribe_to_newsletter,
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


class ApplyPromoCodeView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PromoCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        promo_code = PromoCode.published_objects.filter(
            code__iexact=serializer.data.get('code'),
        ).exclude(
            expires__lt=now()
        ).first()
        if not promo_code:
            return response.Response({
                'code': _('The code you used is invalid or inactive.'),
            }, status=status.HTTP_200_OK)

        bag = request.session.get('bag')
        message = update_discount(bag, promo_code, request.session)

        currency = request.session['currency']
        return response.Response({
            'bag': bag,
            'currency': currency,
            'exchange_rate': ExchangeRate.objects.get(currency=currency.upper()).middle_rate,
            'code': message,
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


class ContinueToPaymentView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CountryNameSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return response.Response({
            'show_cod': serializer.data.get('country_name') == DEFAULT_COUNTRY,
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
        update_bag_with_discount(bag, bag.get('promo_code'), session)

        grand_total = bag['new_grand_total'] if bag.get('new_grand_total', None) else bag['grand_total']
        cart = get_cart(bag)
        session['order_number'] = create_or_update_invoice(
            session,
            grand_total,
            serializer.data,
            cart,
            user
        )
        session['user_information'] = serializer.data
        session['user_information']['registration_email_in_use'] = active
        session['user_information']['newsletter_email_in_use'] = not created

        return response.Response(
            assemble_order_response(session, cart, grand_total, serializer.data)
        , status=status.HTTP_200_OK)


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
        grand_total = bag['new_grand_total'] if bag.get('new_grand_total', None) else bag['grand_total']
        cart = get_cart(bag)

        return response.Response(
            assemble_order_response(session, cart, grand_total, session['user_information'])
        , status=status.HTTP_200_OK)


class UpdateShippingCostView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CountryNameSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bag = request.session.get('bag')
        set_shipping_cost(
            bag,
            request.session['region'],
            serializer.data.get('country_name')
        )
        if bag.get('new_grand_total'):
            bag.update(**get_grandtotals(bag, key_prefix='new_'))

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
        bag = session['bag']

        total = Decimal(bag.get('total'))
        new_total = Decimal(bag.get('new_total', 0))
        shipping_cost = Decimal(bag['shipping_cost'])
        fee = bag.get('fees')
        session['payment_method'] = serializer.data.get('payment_method')

        if session['payment_method'] == InvoicePaymentMethod.CASH_ON_DELIVERY:
            bag['fees'] = str(GLS_FEE)
        else:
            bag['fees'] = 0

        bag.update({
            **get_grandtotals(bag),
        })
        if new_total > 0:
            bag.update({
                **get_grandtotals(bag, key_prefix='new_'),
            })
        session.modified = True
        currency = request.session['currency']
        exchange_rate = ExchangeRate.objects.get(currency=currency.upper()).middle_rate

        return response.Response({
            'bag': bag,
            'currency': currency,
            'exchange_rate': exchange_rate,
            'payment_method': session['payment_method'],
        }, status=status.HTTP_200_OK)


class SubmitReviewView(GenericAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = ReviewSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.data.get('product')
        Review.objects.get_or_create(
            product_id=product_id,
            user_id=request.user.pk,
            defaults={
                'score': serializer.data.get('score'),
                'content': serializer.data.get('content'),
                'published': True,
            }
        )
        product = Product.objects.filter(pk=product_id).first()
        data = serializer.data
        data.update({
            'user_name': self.request.user.first_name,
            'total_score': product.score if product else 0,
            'ratings': product.ratings if product else 0,
        })
        return response.Response(data, status=status.HTTP_200_OK)
