from django.contrib import admin

from thebrushstash.models import (
    Country,
    CreditCardLogo,
    CreditCardSecureLogo,
    FooterItem,
    FooterShareLink,
    NavigationItem,
    OtherImage,
)


class NavigationItemAdmin(admin.ModelAdmin):
    list_display_links = ('name', )
    list_display = ('name', 'location', 'ordering', 'external', )
    list_editable = ('location', 'ordering', 'external', )


class OtherImageAdmin(admin.ModelAdmin):
    fields = ('name', 'image', 'webp_image_url', )
    readonly_fields = ('webp_image_url', )


admin.site.register(Country)
admin.site.register(CreditCardLogo)
admin.site.register(CreditCardSecureLogo)
admin.site.register(FooterItem)
admin.site.register(FooterShareLink)
admin.site.register(NavigationItem, NavigationItemAdmin)
admin.site.register(OtherImage, OtherImageAdmin)
