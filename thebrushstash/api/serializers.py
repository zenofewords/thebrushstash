from rest_framework import serializers


class ProductSeriazlier(serializers.Serializer):
    slug = serializers.SlugField(required=True, max_length=500)
    name = serializers.CharField(required=True, max_length=500)
    quantity = serializers.IntegerField(required=True)
    price = serializers.DecimalField(required=True, max_digits=14, decimal_places=2)


class SimpleProductSerializer(serializers.Serializer):
    slug = serializers.SlugField(required=True, max_length=500)


class CookieSerializer(serializers.Serializer):
    accepted = serializers.BooleanField(required=True)


class RegionSerializer(serializers.Serializer):
    region = serializers.SlugField(required=True)
