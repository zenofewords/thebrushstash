from django.contrib import admin

from thebrushstash.models import (
    Country,
    CreditCardLogo,
    ExchangeRate,
    FooterItem,
    FooterShareLink,
    NavigationItem,
    QandAPair,
    Region,
    Setting,
    StaticPageContent,
    TestImage,
)
from shop.admin import (
    GalleryItemInline,
    SingleGalleryItemInline,
)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_cro', 'shipping_cost', 'published', )
    list_editable = ('name_cro', 'shipping_cost', 'published', )


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


class RegionAdmin(admin.ModelAdmin):
    list_display_links = ('name', )
    list_display = ('name', 'language', 'currency', 'published', 'ordering', )
    list_editable = ('published', )


class QandAPairAdmin(admin.ModelAdmin):
    list_display_links = ('question', )
    list_display = ('question', 'ordering', )
    list_editable = ('ordering', )


admin.site.register(Country, CountryAdmin)
admin.site.register(CreditCardLogo)
admin.site.register(ExchangeRate, ExchangeRateAdmin)
admin.site.register(FooterItem)
admin.site.register(FooterShareLink)
admin.site.register(NavigationItem, NavigationItemAdmin)
admin.site.register(QandAPair, QandAPairAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Setting)
admin.site.register(StaticPageContent)
admin.site.register(TestImage, TestImageAdmin)
