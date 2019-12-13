from django.urls import path

from shop.api.views import (
    AddToBagView,
    ProcessOrderView,
    RemoveFromBagView,
    UpdateBagView,
    UpdatePaymentMethodView,
    UpdateShippingAddressView,
    UpdateShippingCostView,
)


shop_api_urls = []
shop_api_urls.extend((
    path('add-to-bag/', AddToBagView.as_view(), name='add-to-bag'),
    path('process-order/', ProcessOrderView.as_view(), name='process-order'),
    path('remove-from-bag/', RemoveFromBagView.as_view(), name='remove-from-bag'),
    path('update-bag/', UpdateBagView.as_view(), name='update-bag'),
    path('update-payment-method/', UpdatePaymentMethodView.as_view(), name='update-payment-method'),
    path('update-shipping-address/', UpdateShippingAddressView.as_view(), name='update-shipping-address'),
    path('update-shipping-cost/', UpdateShippingCostView.as_view(), name='update-shipping-cost'),
))
