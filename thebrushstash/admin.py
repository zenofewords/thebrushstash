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
    list_display = ('name', 'region', 'published',)
    list_editable = ('region', 'published',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        request = kwargs['request']
        formfield = super().formfield_for_dbfield(db_field, **kwargs)

        if db_field.name in self.list_editable:
            cache_attr_name = 'choices_cache_{}'.format(db_field.name)
            choices_cache = getattr(request, cache_attr_name, None)

            if choices_cache is not None:
                formfield.choices = choices_cache
            else:
                if hasattr(formfield, 'choices'):
                    setattr(request, cache_attr_name, formfield.choices)
        return formfield


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
    list_display = ('name', 'language', 'currency', 'shipping_cost', 'published', 'ordering', )
    list_editable = ('shipping_cost', 'published', )


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
