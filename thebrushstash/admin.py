from django.contrib import admin

from thebrushstash.models import (
    Country,
    CreditCardLogo,
    ExchangeRate,
    FooterItem,
    FooterShareLink,
    NavigationItem,
    TestImage,
)
from shop.admin import (
    GalleryItemInline,
    SingleGalleryItemInline,
)


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        'currency', 'modified_at', 'added_value', 'buying_rate', 'middle_rate', 'selling_rate',
    )
    readonly_fields = ('created_at', 'modified_at', )


class NavigationItemAdmin(admin.ModelAdmin):
    list_display_links = ('name', )
    list_display = ('name', 'location', 'ordering', 'external', 'css_class', )
    list_editable = ('location', 'ordering', 'external', 'css_class', )


class TestImageAdmin(admin.ModelAdmin):
    inlines = [SingleGalleryItemInline, GalleryItemInline, ]


admin.site.register(Country)
admin.site.register(CreditCardLogo)
admin.site.register(ExchangeRate, ExchangeRateAdmin)
admin.site.register(FooterItem)
admin.site.register(FooterShareLink)
admin.site.register(NavigationItem, NavigationItemAdmin)
admin.site.register(TestImage, TestImageAdmin)
