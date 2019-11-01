from rest_framework import generics

from shop.models import (
    Invoice,
    Product,
)
from shop.serializers import (
    OrderSerializer,
    ProductSerializer,
)


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = OrderSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
