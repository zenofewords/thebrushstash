import copy

from django import template
from django.contrib.contenttypes.models import ContentType

from thebrushstash.constants import (
    DEFAULT_REGION,
    REGIONS,
)
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
    request = context.get('request')
    return {
        'current_url': request.path if request else '/',
        'navigation_items': NavigationItem.published_objects.all(),
    }


@register.inclusion_tag('thebrushstash/tags/ship_to.html', takes_context=True)
def ship_to_tag(context):
    request = context.get('request')

    if request:
        default_region = DEFAULT_REGION if request.LANGUAGE_CODE == DEFAULT_REGION else 'eu'
        selected_region = request.session.get('region', default_region)
    else:
        default_region = DEFAULT_REGION
        selected_region = default_region
    regions_copy = copy.deepcopy(REGIONS)
    regions_copy.pop(selected_region)

    return {
        'selected_region': selected_region,
        'current_url': request.path if request else '/',
        'regions': regions_copy,
    }


@register.inclusion_tag('thebrushstash/tags/footer.html')
def footer_tag(hide_social=False):
    return {
        'hide_social': hide_social,
        'footer_items': FooterItem.published_objects.all(),
        'footer_share_links': FooterShareLink.published_objects.all(),
        'credit_card_logos': CreditCardLogo.published_objects.all(),
    }


@register.inclusion_tag('thebrushstash/tags/cookie.html', takes_context=True)
def cookie_tag(context):
    request = context.get('request')

    return {
        'accepted': request.session.get('accepted', None) if request else None,
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
    if not obj:
        return GalleryItem.objects.none()

    return GalleryItem.objects.filter(
        content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk
    )


@register.simple_tag
def get_lead_image(obj):
    return get_gallery(obj).first()


@register.inclusion_tag('thebrushstash/tags/media_object.html')
def media_object(obj, size, selected=False, hidden=False):
    if not hasattr(obj, 'srcsets') or not getattr(obj, 'srcsets'):
        return

    classes = ['image-wrapper', size]
    if hasattr(obj, 'youtube_video_id') and obj.youtube_video_id:
        classes.append('play-icon')
    if selected:
        classes.append('selected')
    class_list = 'class=\"{}\"'.format(' '.join(classes))

    return {
        'object': obj,
        'class_list': class_list,
        'hidden': hidden,
        'webp_srcset': ', '.join(obj.srcsets['webp_{}'.format(size)]),
        'jpg_srcset': ', '.join(obj.srcsets['jpg_{}'.format(size)]),
    }


@register.inclusion_tag('thebrushstash/tags/gallery_item.html')
def gallery_item(obj, item, selected_item_id, first_item):
    selected = False
    if selected_item_id == '0' and first_item:
        selected = True
    elif selected_item_id == str(item.pk):
        selected = True

    return {
        'object': obj,
        'item': item,
        'selected': selected,
    }
