from django.urls import path

from shop.api_views import (
    OrderListCreateAPIView,
    ProductListAPIView,
)


urlpatterns = (
    path('order/', OrderListCreateAPIView.as_view()),
    path('product/', ProductListAPIView.as_view()),
)
