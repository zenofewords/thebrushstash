from django import template
from django.utils.translation import get_language

from shop.constants import EMPTY_BAG
from shop.utils import (
    set_tax,
    set_shipping_cost,
)
from thebrushstash.constants import DEFAULT_REGION
from thebrushstash.models import (
    CreditCardLogo,
    FooterItem,
    FooterShareLink,
    NavigationItem,
    Region,
)

register = template.Library()


@register.inclusion_tag('thebrushstash/tags/navigation_tag.html', takes_context=True)
def navigation_tag(context):
    request = context['request']
    return {
        'current_url': request.path,
        'navigation_items': NavigationItem.published_objects.all(),
        'bag': request.session.get('bag'),
        'currency': request.session['currency'],
        'LANGUAGE_CODE': request.session.get('_language'),
    }


@register.inclusion_tag('thebrushstash/tags/ship_to_tag.html', takes_context=True)
def ship_to_tag(context):
    session = context['request'].session
    regions = Region.published_objects.all()
    default = regions.get(name=DEFAULT_REGION)

    language = get_language()
    if not session.get('_language'):
        session['_language'] = language

    default_region = default if language == default.name else regions.first()
    region = session.get('region')

    if not region:
        session['region'] = default_region.name
        selected_region = default_region
    else:
        selected_region = regions.get(name=region)

    bag = session.get('bag')
    if not bag:
        session['bag'] = EMPTY_BAG

    session['currency'] = selected_region.currency
    set_shipping_cost(session['bag'], selected_region.name)
    set_tax(session['bag'], selected_region.currency)
    session.modified = True

    return {
        'selected_region': selected_region,
        'regions': regions.exclude(name=selected_region.name),
        'bag': session['bag'],
    }


@register.inclusion_tag('thebrushstash/tags/bag_tag.html', takes_context=True)
def bag_tag(context):
    request = context['request']
    return {
        'current_url': request.path,
        'currency': request.session.get('currency', 'hrk'),
        'bag': request.session.get('bag', EMPTY_BAG),
    }


@register.inclusion_tag('thebrushstash/tags/footer_tag.html')
def footer_tag(hide_social=False):
    return {
        'hide_social': hide_social,
        'footer_items': FooterItem.published_objects.all(),
        'footer_share_links': FooterShareLink.published_objects.all(),
    }


@register.inclusion_tag('thebrushstash/tags/cookie_tag.html', takes_context=True)
def cookie_tag(context):
    request = context['request']
    return {
        'accepted': request.session.get('accepted', None),
    }


@register.inclusion_tag('thebrushstash/tags/credit_card_logos_tag.html')
def credit_card_logos_tag(css=''):
    return {
        'credit_card_logos': CreditCardLogo.published_objects.all(),
        'css': css,
    }


@register.inclusion_tag('thebrushstash/tags/newsletter_tag.html')
def newsletter_tag():
    pass
