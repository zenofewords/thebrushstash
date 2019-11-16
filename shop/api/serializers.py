from rest_framework import serializers


class ProductSeriazlier(serializers.Serializer):
    pk = serializers.CharField(required=True, max_length=10)
    slug = serializers.SlugField(required=True, max_length=500)
    name = serializers.CharField(required=True, max_length=500)
    quantity = serializers.IntegerField(required=True)
    price = serializers.DecimalField(required=True, max_digits=14, decimal_places=2)
    image_url = serializers.CharField(required=True, max_length=1000)


class SimpleProductSerializer(serializers.Serializer):
    slug = serializers.SlugField(required=True, max_length=500)


class UserInformationSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True, max_length=500)
    email = serializers.CharField(required=True, max_length=500)
    country = serializers.CharField(required=True, max_length=500)
    address = serializers.CharField(required=True, max_length=500)
    city = serializers.CharField(required=True, max_length=500)
    state_county = serializers.CharField(required=True, max_length=500)
    zip_code = serializers.CharField(required=True, max_length=500)

    note = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    register = serializers.BooleanField(required=False)
    subscribe_to_newsletter = serializers.BooleanField(required=False)
    agree_to_terms = serializers.BooleanField(required=True)
