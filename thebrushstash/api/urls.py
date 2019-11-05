from django.urls import path

from thebrushstash.api.views import (
    CookieView,
    RegionView,
    AddToBagView,
    RemoveFromBagView,
)


api_urls = []
api_urls.extend((
    path('cookie/', CookieView.as_view(), name='cookie'),
    path('region/', RegionView.as_view(), name='region'),
    path('add-to-bag/', AddToBagView.as_view(), name='add-to-bag'),
    path('remove-from-bag/', RemoveFromBagView.as_view(), name='remove-from-bag'),
))
