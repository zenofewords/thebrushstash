from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language

from shop.constants import VARIATIONS
from shop.models import (
    GalleryItem,
    Showcase,
)
from thebrushstash.utils import format_price

register = template.Library()


@register.inclusion_tag('shop/tags/showcase_tag.html')
def showcase_tag():
    return {
        'showcase': Showcase.published_objects.last(),
        'LANGUAGE_CODE': get_language(),
    }


@register.inclusion_tag('shop/tags/purchase_summary_tag.html')
def purchase_summary_tag(bag, region, currency, show_links=False):
    return {
        'bag': bag,
        'region': region,
        'currency': currency,
        'show_links': show_links,
    }


@register.simple_tag
def get_gallery(obj, standalone=False, gallery_only=False):
    if not obj:
        return GalleryItem.objects.none()

    qs = GalleryItem.objects.filter(
        standalone=standalone,
        content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk
    )
    if gallery_only:
        qs = qs.filter(show_in_gallery=True)
    return qs


@register.simple_tag
def get_image_for_model(obj, standalone=False):
    return get_gallery(obj, standalone).first()


@register.simple_tag
def get_image_by_natural_key(app_name, model, object_id):
    return GalleryItem.objects.filter(
        content_type=ContentType.objects.get_by_natural_key(app_name, model), object_id=object_id
    ).first()


@register.simple_tag()
def get_image_url_for_email(site_name, object_id):
    item = GalleryItem.objects.filter(
        content_type=ContentType.objects.get_by_natural_key('shop', 'product'), object_id=object_id
    ).first()
    print('tag', item.image.path)
    return '{}'.format(item.image.path)


@register.inclusion_tag('thebrushstash/tags/media_object_tag.html')
def media_object(obj, shape, selected=False, hidden=False, preview=False):
    if not hasattr(obj, 'srcsets') or not getattr(obj, 'srcsets'):
        return

    classes = ['image-wrapper', shape]
    if hasattr(obj, 'youtube_video_id') and obj.youtube_video_id:
        classes.append('play-icon')
    if selected:
        classes.append('selected')
    class_list = 'class=\"{}\"'.format(' '.join(classes))

    srcsets = {}
    for variation in VARIATIONS:
        srcsets['{}_srcset'.format(variation)] = ', '.join(
            obj.srcsets['{}_{}'.format(variation, shape)]
        )

    data = {
        'object': obj,
        'class_list': class_list,
        'hidden': hidden,
        'preview': preview,
    }
    data.update(srcsets)
    return data


@register.inclusion_tag('thebrushstash/tags/gallery_item_tag.html')
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


@register.simple_tag(takes_context=True)
def get_localized_price(context, key, obj):
    currency = context['request'].session['currency']
    price = getattr(obj, '{}_{}'.format(key, currency))

    return format_price(currency, price)


@register.simple_tag()
def get_localized_price_for_currency(obj, key, currency, multiply=1):
    price = getattr(obj, '{}_{}'.format(key, currency)) * multiply
    return format_price(currency, price)


@register.simple_tag()
def get_price_for_currency(obj, key, currency):
    price = obj.get('{}_{}'.format(key, currency))

    return format_price(currency, price)


@register.simple_tag
def format_price_with_currency(price, currency):
    return format_price(currency, price)
