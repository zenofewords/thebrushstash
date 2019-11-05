from decimal import Decimal
from rest_framework import (
    response,
    status,
)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from thebrushstash.constants import DEFAULT_REGION
from thebrushstash.api.serializers import (
    ProductSeriazlier,
    CookieSerializer,
    RegionSerializer,
    SimpleProductSerializer,
)


class AddToBagView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ProductSeriazlier

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_data = serializer.data
        quantity = product_data.get('quantity')
        subtotal = quantity * product_data.get('price')

        products = {}
        bag = {
            'products': products,
            'total': 0,
            'totalQuantity': 0,
        }
        if request.session.get('bag'):
            bag = request.session.get('bag')
            products = bag.get('products')

        product = None
        product_id = product_data.get('slug')
        if product_id in products:
            product = products[product_id]
            products[product_id] = {
                'name': product_data.get('name'),
                'quantity': product.get('quantity') + quantity,
                'subtotal': str(Decimal(product.get('subtotal')) + subtotal),
            }
        else:
            product = {
                'name': product_data.get('name'),
                'quantity': quantity,
                'subtotal': str(subtotal),
            }
            products[product_id] = product

        bag = {
            'products': products,
            'total': str(Decimal(bag['total']) + Decimal(subtotal)),
            'totalQuantity': bag['totalQuantity'] + quantity,
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
            bag['totalQuantity'] = bag['totalQuantity'] - product.get('quantity')
            del products[product_id]

        request.session['bag'] = bag
        return response.Response({'bag': bag}, status=status.HTTP_200_OK)


class CookieView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CookieSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.session['accepted'] = bool(serializer.data.get('accepted', False))
        return response.Response(
            {'accepted': request.session['accepted']}, status=status.HTTP_200_OK
        )


class RegionView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegionSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.session['region'] = serializer.data.get('region', DEFAULT_REGION)
        return response.Response({'region': request.session['region']}, status=status.HTTP_200_OK)
