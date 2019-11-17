from django.urls import path

from shop.api.views import (
    AddToBagView,
    RemoveFromBagView,
    ProcessOrderView,
    UpdatePaymentMethodView,
)


shop_api_urls = []
shop_api_urls.extend((
    path('add-to-bag/', AddToBagView.as_view(), name='add-to-bag'),
    path('remove-from-bag/', RemoveFromBagView.as_view(), name='remove-from-bag'),
    path('process-order/', ProcessOrderView.as_view(), name='process-order'),
    path('update-payment-method/', UpdatePaymentMethodView.as_view(), name='update-payment-method'),
))
