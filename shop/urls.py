from django.urls import path

from shop.views import (
    CheckoutView,
    ReviewBagView,
    ProductDetailView,
    PurchaseCompletedView,
    IPGPurchaseCompletedView,
    IPGPurchaseCancelledView,
    ShopHomeView,
)


app_name = 'shop'
urlpatterns = (
    path('', ShopHomeView.as_view(), name='shop'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('review-bag/', ReviewBagView.as_view(), name='review-bag'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('purchase-completed/', PurchaseCompletedView.as_view(), name='purchase-completed'),
    path('ipg-purchase-completed/', IPGPurchaseCompletedView.as_view(), name='ipg-purchase-completed'),
    path('ipg-purchase-cancelled/', IPGPurchaseCancelledView.as_view(), name='ipg-purchase-cancelled'),
)
