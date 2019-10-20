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
    template_name = 'shop/shop_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'products': Product.objects.filter(published=True),
        })
        return context