from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.utils.text import slugify


from shop.models import (
    CustomLabel,
    EmailAudit,
    GalleryItem,
    InstallmentOption,
    Invoice,
    Newsletter,
    Product,
    PromoCode,
    Review,
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
        '__str__', 'name', 'image', 'youtube_video_id', 'show_in_gallery', 'standalone',
        'image_preview_thumb',
    )
    readonly_fields = ('created_at', 'image_preview', )
    search_fields = ('name', )
    fields = (
        'name', 'image', 'youtube_video_id', 'show_in_gallery', 'standalone', 'content_type',
        'object_id',
    )

    def image_preview(self, obj):
        return get_preview_image(obj.image, 800)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class GalleryItemInline(GenericTabularInline):
    model = GalleryItem
    fields = (
        'name', 'image', 'youtube_video_id', 'show_in_gallery', 'ordering', 'image_preview_thumb',
    )
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
            for saved_instance in saved_instances:
                instance = saved_instance
                instance.standalone = True
                instance.save()
        return saved_instances


class SingleGalleryItemInline(GenericTabularInline):
    model = GalleryItem
    formset = SingleGalleryItemInlineFormSet
    fields = ('name', 'image', 'image_preview_thumb', )
    readonly_fields = ('image_preview_thumb', )
    extra = 3
    verbose_name = 'Image'
    verbose_name_plural = 'Images'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(standalone=True)

    def image_preview_thumb(self, obj):
        return get_preview_image(obj.image, 100)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'created_at', 'order_number', 'first_name', 'last_name', 'payment_method', 'status',
    )
    list_editable = ('status', )
    list_filter = ('status', 'payment_method', )
    readonly_fields = ('created_at', 'modified_at', )
    search_fields = ('created_at', 'first_name', 'last_name', )
    exclude = ('bag_dump', 'resend_purchase_confirmation_email', 'register_user', 'subscribe_to_newsletter', )


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'schedule_at', 'status', 'status_message', 'completed_at', )
    readonly_fields = ('completed_at', 'status', 'status_message', )
    raw_id_fields = ('recipient_list', )
    autocomplete_fields = ('recipient_list', )
    fieldsets = (
        ('Content', {
            'fields': ('header_image', 'body_image', ),
        }),
        ('Text fields (ENG)', {
            'classes': ('collapse', ),
            'fields': ('title', 'header_text', 'body_text', ),
        }),
        ('Text fields (CRO)', {
            'classes': ('collapse', ),
            'fields': ('title_cro', 'header_text_cro', 'body_text_cro', ),
        }),
        ('Manage', {
            'fields': ('send', 'schedule_at', 'recipient_list', ),
        }),
        ('Info', {
            'fields': ('status', 'status_message', 'completed_at', )
        }),
    )


class ProductAdmin(AutoSlugAdmin):
    list_display_links = ('name', )
    list_display = ('name', 'price_hrk', 'in_stock', 'ordering', 'published', )
    list_editable = ('price_hrk', 'in_stock', 'ordering', 'published', )
    readonly_fields = ('price_usd', 'price_eur', 'price_gbp', )
    fieldsets = (
        (None, {
            'fields': (
                'product_type', 'name', 'slug', 'in_stock', 'ordering', 'published',
                'allow_installments', 'free_shipping', 'new', 'custom_label',
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
        ('Old price (HRK, USD, EUR, GBP)', {
            'classes': ('collapse', ),
            'fields': ('old_price_hrk', 'old_price_usd', 'old_price_eur', 'old_price_gbp', ),
        }),
    )
    inlines = [GalleryItemInline, SingleGalleryItemInline]


class ProductTypeAdmin(AutoSlugAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )
    list_display = ('product', 'user', 'score', 'published', )
    list_editable = ('published', )


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


class EmailAuditAdmin(admin.ModelAdmin):
    list_display_links = ('receiver', )
    list_display = ('receiver', 'status', 'created_at', 'sent_at', 'source', 'payment_method', )
    readonly_fields = (
        'receiver', 'source', 'payment_method', 'created_at', 'sent_at', 'content', 'error_message',
    )
    list_filter = ('status', 'source', 'payment_method', )
    search_fields = ('receiver', )


class PromoCodeInline(admin.TabularInline):
    model = PromoCode.product_list.through
    extra = 0


class PromoCodeAdmin(admin.ModelAdmin):
    exclude = ('product_list', )
    list_display = (
        'code', 'published', 'expires', 'single_use', 'flat_discount', 'flat_discount_amount', 'used',
    )
    readonly_fields = ('used', )
    fieldsets = (
        (None, {
            'fields': ( 'published', 'code', 'expires', ),
        }),
        ('Flat discount', {
            'classes': ('collapse', ),
            'fields': ('single_use', 'flat_discount', 'flat_discount_amount', 'used', ),
        }),
        ('Percentage based discount', {
            'classes': ('collapse', ),
            'fields': ('auto_apply_discount', ),
        }),
    )
    inlines = [PromoCodeInline]


class InstallmentOptionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'range_from', 'range_to', 'installment_number', )


class CustomLabelAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomLabel, CustomLabelAdmin)
admin.site.register(EmailAudit, EmailAuditAdmin)
admin.site.register(GalleryItem, GalleryItemAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Showcase, ShowcaseAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(InstallmentOption, InstallmentOptionAdmin)
