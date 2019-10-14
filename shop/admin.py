from django.contrib import admin
from django.utils.safestring import mark_safe

from shop.models import (
    ExchangeRate,
    Order,
    Product,
    ProductType,
    Transaction,
)


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
    list_display = ('name', 'price_hrk', 'ordering', 'published', 'image_preview_thumbnail', )
    list_editable = ('price_hrk', 'ordering', 'published', )
    readonly_fields = ('price_usd', 'price_eur', 'price_gbp', 'image_preview', )
    fields = (
        'product_type', 'name', 'slug', 'foreword', 'description', 'image', 'in_stock', 'ordering',
        'published', 'new', 'price_hrk', 'price_usd', 'price_eur', 'price_gbp', 'image_preview',
    )

    def crop_image(self, image, max_width):
        try:
            original_width = image.width
            original_height = image.height

            width = original_width if original_width < max_width else max_width
            ratio = original_width / width
            height = original_height / ratio

            return mark_safe(
                '<img src={url} width={width} height={height} />'.format(
                    url=image.url,
                    width=width,
                    height=height,
                )
            )
        except FileNotFoundError:
            return ''

    def image_preview(self, obj):
        return self.crop_image(obj.image, 800)

    def image_preview_thumbnail(self, obj):
        return self.crop_image(obj.image, 50)


admin.site.register(ExchangeRate, ExchangeRateAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType)
admin.site.register(Transaction)
