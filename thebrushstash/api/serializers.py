from rest_framework import serializers


class CookieSerializer(serializers.Serializer):
    accepted = serializers.BooleanField(required=True)


class RegionSerializer(serializers.Serializer):
    region = serializers.SlugField(required=True)


class SubscribeToNewsletterSerializer(serializers.Serializer):
    email0 = serializers.EmailField(max_length=200, min_length=5, allow_blank=False)
    email1 = serializers.EmailField(max_length=None, min_length=None, allow_blank=True)
