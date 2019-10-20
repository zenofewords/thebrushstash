from django import template
from django.contrib.contenttypes.models import ContentType

from thebrushstash.models import (
    CreditCardLogo,
    CreditCardSecureLogo,
    FooterItem,
    FooterShareLink,
    GalleryItem,
    NavigationItem,
)

register = template.Library()


@register.inclusion_tag('thebrushstash/tags/navigation.html', takes_context=True)
def navigation_tag(context):
    return {
        'current_url': context['request'].path,
        'navigation_items': NavigationItem.published_objects.all(),
    }


@register.inclusion_tag('thebrushstash/tags/ship_to.html')
def ship_to_tag():
    return {
        'regions': ('UK', )
    }


@register.inclusion_tag('thebrushstash/tags/footer.html')
def footer_tag():
    return {
        'footer_items': FooterItem.published_objects.all(),
        'footer_share_links': FooterShareLink.published_objects.all(),
        'credit_card_logos': CreditCardLogo.published_objects.all(),
    }


@register.inclusion_tag('thebrushstash/tags/credit_card_secure_logos.html')
def credit_card_secure_logos_tag():
    return {
        'credit_card_secure_logos': CreditCardSecureLogo.published_objects.all(),
    }


@register.inclusion_tag('thebrushstash/tags/newsletter.html')
def newsletter_tag():
    pass


@register.simple_tag
def get_gallery(obj):
    return GalleryItem.objects.filter(
        content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk
    )


@register.simple_tag
def get_lead_image(obj):
    return get_gallery(obj).first()


@register.inclusion_tag('thebrushstash/tags/picture.html')
def picture(obj, size):
    if not hasattr(obj, 'srcsets') or not getattr(obj, 'srcsets'):
        return

    return {
        'object': obj,
        'webp_srcset': ', '.join(obj.srcsets['webp_{}'.format(size)]),
        'jpg_srcset': ', '.join(obj.srcsets['jpg_{}'.format(size)]),
    }