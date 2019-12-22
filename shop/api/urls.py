from django.urls import path

from shop.api.views import (
    AddToBagView,
    ContinueToPaymentView,
    ProcessOrderView,
    RemoveFromBagView,
    SubmitReviewView,
    UpdateBagView,
    UpdatePaymentMethodView,
    UpdateShippingAddressView,
    UpdateShippingCostView,
)


shop_api_urls = []
shop_api_urls.extend((
    path('add-to-bag/', AddToBagView.as_view(), name='add-to-bag'),
    path('continue-to-payment/', ContinueToPaymentView.as_view(), name='continue-to-payment'),
    path('process-order/', ProcessOrderView.as_view(), name='process-order'),
    path('remove-from-bag/', RemoveFromBagView.as_view(), name='remove-from-bag'),
    path('submit-review/', SubmitReviewView.as_view(), name='submit-review'),
    path('update-bag/', UpdateBagView.as_view(), name='update-bag'),
    path('update-payment-method/', UpdatePaymentMethodView.as_view(), name='update-payment-method'),
    path('update-shipping-address/', UpdateShippingAddressView.as_view(), name='update-shipping-address'),
    path('update-shipping-cost/', UpdateShippingCostView.as_view(), name='update-shipping-cost'),
))
