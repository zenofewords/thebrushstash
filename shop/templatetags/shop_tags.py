from decimal import Decimal

from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language

from shop.constants import VARIATIONS
from shop.models import (
    GalleryItem,
    Showcase,
)
from shop.utils import get_price_with_currency
register = template.Library()


@register.inclusion_tag('shop/tags/showcase_tag.html')
def showcase_tag():
    return {
        'showcase': Showcase.published_objects.last(),
        'LANGUAGE_CODE': get_language(),
    }


@register.inclusion_tag('shop/tags/purchase_summary_tag.html', takes_context=True)
def purchase_summary_tag(context, bag, region, exchange_rates, currency, review=False):
    request = context['request']
    return {
        'bag': bag,
        'region': region,
        'currency': currency,
        'review': review,
        'exchange_rates': exchange_rates,
        'user': request.user,
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
def get_images_for_model(obj, standalone=False, number=1):
    if number == 1:
        return get_gallery(obj, standalone).first()
    return get_gallery(obj, standalone).all()[:number]


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
    return '{}'.format(item.image.path)


@register.inclusion_tag('thebrushstash/tags/media_object_tag.html')
def media_object(obj, shape, selected=False, hidden=False, preview=False, exclude_id=False):
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
        'data_id': shape == 'thumbnail',
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


@register.inclusion_tag('thebrushstash/tags/rating_tag.html')
def rating_tag(obj, can_review=False):
    percentage = 0

    if obj.ratings > 0:
        percentage = obj.score / obj.ratings / 5 * 100

    return {
        'ratings': obj.ratings,
        'percentage': percentage,
        'can_review': can_review,
    }


@register.simple_tag()
def get_formatted_discount(value):
    return '-{}%'.format(round(value, 2))


@register.simple_tag()
def get_localized_item_price(obj, key, currency, multiply=1, discount=None):
    price = getattr(obj, '{}_{}'.format(key, currency)) * multiply
    if discount:
        price = round(price - price * Decimal(discount) / 100, 2)
    return get_price_with_currency(price, currency)


@register.simple_tag()
def get_price_in_currency(obj, key, exchange_rates, currency):
    price = '{:0.2f}'.format(Decimal(obj.get(key, 0)) / exchange_rates[currency], 2)
    return get_price_with_currency(price, currency)
