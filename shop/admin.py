from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.utils.text import slugify

from shop.models import (
    GalleryItem,
    Invoice,
    Product,
    Showcase,
)
from thebrushstash.utils import get_preview_image


class AutoSlugAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.slug == '':
            obj.slug = slugify(obj.name)
        obj.save()


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


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'order_number', 'first_name', 'last_name', 'payment_method', 'status', )
    list_editable = ('status', )
    list_filter = ('status', 'payment_method', )
    readonly_fields = ('created_at', 'modified_at', )
    search_fields = ('created_at', 'first_name', 'last_name', )


class ProductAdmin(AutoSlugAdmin):
    list_display_links = ('name', )
    list_display = ('name', 'price_hrk', 'in_stock', 'ordering', 'published', )
    list_editable = ('price_hrk', 'ordering', 'published', )
    readonly_fields = ('price_usd', 'price_eur', 'price_gbp', )
    fieldsets = (
        (None, {
            'fields': (
                'product_type', 'name', 'slug', 'in_stock', 'ordering', 'published', 'new',
            )
        }),
        ('Text fields (ENG)', {
            'classes': ('collapse', ),
            'fields': ('foreword', 'title', 'description', ),
        }),
        ('Text fields (CRO)', {
            'classes': ('collapse', ),
            'fields': ('foreword_cro', 'title_cro', 'description_cro', ),
        }),
        ('Price (HRK, USD, EUR, GBP)', {
            'classes': ('collapse', ),
            'fields': ('price_hrk', 'price_usd', 'price_eur', 'price_gbp', ),
        }),
    )
    inlines = [GalleryItemInline, SingleGalleryItemInline]


class ProductTypeAdmin(AutoSlugAdmin):
    pass


class ShowcaseAdmin(AutoSlugAdmin):
    list_display_links = ('name', )
    list_display = ('name', 'published', )
    list_editable = ('published', )
    fieldsets = (
        (None, {
            'fields': ('published', ),
        }),
        ('Text fields (ENG)', {
            'classes': ('collapse', ),
            'fields': ('name', 'description', ),
        }),
        ('Text fields (CRO)', {
            'classes': ('collapse', ),
            'fields': ('name_cro', 'description_cro', ),
        }),
    )
    inlines = [SingleGalleryItemInline]


admin.site.register(GalleryItem, GalleryItemAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Showcase, ShowcaseAdmin)
