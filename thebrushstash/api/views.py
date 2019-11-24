from rest_framework import (
    response,
    status,
)
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from thebrushstash.models import Region
from thebrushstash.constants import DEFAULT_REGION
from thebrushstash.api.serializers import (
    CookieSerializer,
    RegionSerializer,
)


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
        request.session['currency'] = Region.objects.get(name=request.session['region']).currency
        return response.Response({
            'region': request.session['region'],
            'currency': request.session['currency'],
            'bag': request.session['bag'],
        }, status=status.HTTP_200_OK)
