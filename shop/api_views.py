from rest_framework import generics

from shop.models import (
    Order,
    Product,
)
from shop.serializers import (
    OrderSerializer,
    ProductSerializer,
)


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
