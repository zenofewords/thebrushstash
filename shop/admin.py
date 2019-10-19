from django.contrib import admin

from shop.models import (
    ExchangeRate,
    Order,
    Product,
    ProductType,
    Transaction,
)
from thebrushstash.admin import GalleryItemInline


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        'currency', 'modified_at', 'added_value', 'buying_rate', 'middle_rate', 'selling_rate',
    )
    readonly_fields = ('created_at', 'modified_at', )


class OrderAdmin(admin.ModelAdmin):
    list_display_links = ('product', )
    list_display = ('product', 'created_at', 'first_name', 'last_name', 'status', 'paid', )
    list_editable = ('status', 'paid', )
    list_filter = ('status', )
    readonly_fields = ('created_at', 'modified_at', )
    search_fields = ('created_at', 'first_name', 'last_name', )


class ProductAdmin(admin.ModelAdmin):
    list_display_links = ('name', )
    list_display = ('name', 'price_hrk', 'ordering', 'published', )
    list_editable = ('price_hrk', 'ordering', 'published', )
    readonly_fields = ('price_usd', 'price_eur', 'price_gbp', )
    fields = (
        'product_type', 'name', 'slug', 'foreword', 'description', 'in_stock', 'ordering',
        'published', 'new', 'price_hrk', 'price_usd', 'price_eur', 'price_gbp',
    )
    inlines = [GalleryItemInline, ]


admin.site.register(ExchangeRate, ExchangeRateAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType)
admin.site.register(Transaction)
