from django.urls import path

from shop.views import (
    ProductDetailView,
    ShopHomeView,
)


app_name = 'shop'
urlpatterns = (
    path('', ShopHomeView.as_view(), name='shop'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
)
