from rest_framework import serializers

from shop.models import (
    Invoice,
    Product,
)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
