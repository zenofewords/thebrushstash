from rest_framework import (
    response,
    status,
)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from django.contrib.sites.shortcuts import get_current_site

from thebrushstash.models import Region
from thebrushstash.constants import DEFAULT_REGION
from thebrushstash.api.serializers import (
    CookieSerializer,
    SubscribeToNewsletterSerializer,
    RegionSerializer,
)
from thebrushstash.utils import safe_subscribe_to_newsletter


class CookieView(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CookieSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.session['accepted'] = bool(serializer.data.get('accepted', False))

        if request.user.is_authenticated:
            request.user.accepted_cookies = True
            request.user.save()

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
        request.session['currency'] = Region.objects.get(name=request.session['region']).currency
        return response.Response({
            'region': request.session['region'],
            'currency': request.session['currency'],
            'bag': request.session['bag'],
        }, status=status.HTTP_200_OK)


class SubscribeToNewsletter(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SubscribeToNewsletterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email0 = serializer.data.get('email0')
        email1 = serializer.data.get('email1')

        message = ''
        if not email1:
            current_site = get_current_site(request)
            message = safe_subscribe_to_newsletter(request.user, email0, current_site)

        return response.Response({'message': message}, status=status.HTTP_200_OK)
