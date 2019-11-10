from django.urls import path

from shop.views import (
    CheckoutView,
    ReviewBagView,
    ProductDetailView,
    ProductListView,
    PurchaseCompleteView,
    ShopHomeView,
)


app_name = 'shop'
urlpatterns = (
    path('', ShopHomeView.as_view(), name='shop'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('review-bag/', ReviewBagView.as_view(), name='review-bag'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('purchase-complete/', PurchaseCompleteView.as_view(), name='purchase-complete'),
)
