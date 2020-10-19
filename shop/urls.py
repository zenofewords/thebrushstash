from django.urls import path

from shop.views import (
    ProductDetailView,
    ShopHomeView,
    ShopHomePreviewView,
)


app_name = 'shop'
urlpatterns = (
    path('', ShopHomeView.as_view(), name='shop'),
    path('preview/', ShopHomePreviewView.as_view(), name='shop-preview'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
)
