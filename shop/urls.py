from django.urls import path

from shop.views import (
    ProductDetailView,
    ProductListView,
    ShopHomeView,
)


app_name = 'shop'
urlpatterns = (
    path('', ShopHomeView.as_view(), name='shop-home'),
    path('products/<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('products', ProductListView.as_view(), name='product-list'),
)
