from django.urls import path

from thebrushstash.api.views import (
    CookieView,
    RegionView,
    SubscribeToNewsletter,
)


thebrushstash_api_urls = []
thebrushstash_api_urls.extend((
    path('cookie/', CookieView.as_view(), name='cookie'),
    path('region/', RegionView.as_view(), name='region'),
    path('subscribe-to-newsletter/', SubscribeToNewsletter.as_view(), name='newsletter'),
))
