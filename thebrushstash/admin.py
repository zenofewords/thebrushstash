from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from thebrushstash.models import (
    Country,
    CreditCardLogo,
    CreditCardSecureLogo,
    FooterItem,
    FooterShareLink,
    GalleryItem,
    NavigationItem,
    TestImage,
)
from thebrushstash.utils import get_preview_image


class GalleryItemAdmin(admin.ModelAdmin):
    list_display_links = ('__str__', )
    list_display = ('__str__', 'name', 'image', 'youtube_link', 'image_preview_thumb', )
    readonly_fields = ('created_at', 'image_preview', )
    search_fields = ('name', )

    def image_preview(self, obj):
        return get_preview_image(obj.image, 800)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class GalleryItemInline(GenericTabularInline):
    model = GalleryItem
    fields = ('name', 'image', 'youtube_link', 'ordering', 'image_preview_thumb', )
    readonly_fields = ('image_preview_thumb', )

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class NavigationItemAdmin(admin.ModelAdmin):
    list_display_links = ('name', )
    list_display = ('name', 'location', 'ordering', 'external', )
    list_editable = ('location', 'ordering', 'external', )


class TestImageAdmin(admin.ModelAdmin):
    inlines = [GalleryItemInline, ]


admin.site.register(Country)
admin.site.register(CreditCardLogo)
admin.site.register(CreditCardSecureLogo)
admin.site.register(FooterItem)
admin.site.register(FooterShareLink)
admin.site.register(GalleryItem, GalleryItemAdmin)
admin.site.register(NavigationItem, NavigationItemAdmin)
admin.site.register(TestImage, TestImageAdmin)
