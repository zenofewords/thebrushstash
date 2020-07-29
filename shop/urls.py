from django.urls import path

from shop.views import (
    CheckoutView,
    ReviewBagView,
    ProductDetailView,
    ShopHomeView,
)


app_name = 'shop'
urlpatterns = (
    path('', ShopHomeView.as_view(), name='shop'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('review-bag/', ReviewBagView.as_view(), name='review-bag'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
)
