from django.urls import path

from shop.api.views import (
    AddToBagView,
    RemoveFromBagView,
)


shop_api_urls = []
shop_api_urls.extend((
    path('add-to-bag/', AddToBagView.as_view(), name='add-to-bag'),
    path('remove-from-bag/', RemoveFromBagView.as_view(), name='remove-from-bag'),
))
