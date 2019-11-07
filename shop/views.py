from django.views.generic import (
    DetailView,
    TemplateView,
)
from django.utils.text import slugify
from django.views.generic.list import ListView

from shop.models import Product


class ReviewBagView(TemplateView):
    template_name = 'shop/review_bag.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'bag': self.request.session.get('bag'),
        })
        return context


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        self.selected_item_id = slugify(request.GET.get('gallery-item', 0))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'selected_item_id': self.selected_item_id,
            'other_products': Product.published_objects.exclude(id=self.object.pk)[:3]
        })
        return context


class ShopHomeView(TemplateView):
    template_name = 'shop/shop_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'products': Product.published_objects.all(),
        })
        return context
