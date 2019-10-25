from rest_framework import serializers


class CookieSerializer(serializers.Serializer):
    accepted = serializers.BooleanField(required=True)


class RegionSerializer(serializers.Serializer):
    region = serializers.SlugField(required=True)
