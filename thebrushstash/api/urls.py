from django.urls import path

from thebrushstash.api.views import (
    CookieView,
    RegionView,
)


api_urls = []
api_urls.extend((
    path('cookie/', CookieView.as_view(), name='cookie'),
    path('region/', RegionView.as_view(), name='region'),
))
