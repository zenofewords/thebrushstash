from django.contrib import admin
from django.utils.safestring import mark_safe

from shop.models import (
    Country,
    ExchangeRate,
    Order,
    Product,
    ProductType,
    Transaction,
)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'published', )
    list_editable = ('published', )


class OrderAdmin(admin.ModelAdmin):
    list_display_links = ('product', )
    list_display = ('product', 'created', 'first_name', 'last_name', 'status', 'paid', )
    list_editable = ('status', 'paid', )
    list_filter = ('status', )
    readonly_fields = ('created', 'modified', )
    search_fields = ('created', 'first_name', 'last_name', )


class ProductAdmin(admin.ModelAdmin):
    list_display_links = ('name', )
    list_display = ('name', 'price_hrk', 'ordering', 'published', 'image_preview_thumbnail', )
    list_editable = ('price_hrk', 'ordering', 'published', )
    readonly_fields = ('image_preview', )

    def crop_image(self, image, max_width):
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

    def image_preview(self, obj):
        return self.crop_image(obj.image, 800)

    def image_preview_thumbnail(self, obj):
        return self.crop_image(obj.image, 150)


admin.site.register(Country, CountryAdmin)
admin.site.register(ExchangeRate)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType)
admin.site.register(Transaction)
