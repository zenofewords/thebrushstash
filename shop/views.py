from django.views.generic import (
    DetailView,
    TemplateView,
)
from django.views.generic.list import ListView

from shop.models import Product


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ShopHomeView(TemplateView):
    template_name = 'shop/shop_base.html'
