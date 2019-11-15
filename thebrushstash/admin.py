from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet

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
    list_display = (
        '__str__', 'name', 'image', 'youtube_video_id', 'standalone', 'image_preview_thumb',
    )
    readonly_fields = ('created_at', 'image_preview', )
    search_fields = ('name', )
    fields = ('name', 'image', 'youtube_video_id', 'standalone', 'content_type', 'object_id',)

    def image_preview(self, obj):
        return get_preview_image(obj.image, 800)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class GalleryItemInline(GenericTabularInline):
    model = GalleryItem
    fields = ('name', 'image', 'youtube_video_id', 'ordering', 'image_preview_thumb', )
    readonly_fields = ('image_preview_thumb', )
    extra = 3
    max_num = 10

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(standalone=False)


class SingleGalleryItemInlineFormSet(BaseGenericInlineFormSet):
    def save_new_objects(self, commit=True):
        saved_instances = super().save_new_objects(commit)
        if commit and len(saved_instances) > 0:
            instance = saved_instances[0]
            instance.standalone = True
            instance.save()
        return saved_instances


class SingleGalleryItemInline(GenericTabularInline):
    model = GalleryItem
    formset = SingleGalleryItemInlineFormSet
    fields = ('name', 'image', 'image_preview_thumb', )
    readonly_fields = ('image_preview_thumb', )
    extra = 1
    max_num = 1
    verbose_name = 'Image'
    verbose_name_plural = 'Images'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(standalone=True)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class NavigationItemAdmin(admin.ModelAdmin):
    list_display_links = ('name', )
    list_display = ('name', 'location', 'ordering', 'external', 'css_class', )
    list_editable = ('location', 'ordering', 'external', 'css_class', )


class TestImageAdmin(admin.ModelAdmin):
    inlines = [SingleGalleryItemInline, GalleryItemInline, ]


admin.site.register(Country)
admin.site.register(CreditCardLogo)
admin.site.register(CreditCardSecureLogo)
admin.site.register(FooterItem)
admin.site.register(FooterShareLink)
admin.site.register(GalleryItem, GalleryItemAdmin)
admin.site.register(NavigationItem, NavigationItemAdmin)
admin.site.register(TestImage, TestImageAdmin)
