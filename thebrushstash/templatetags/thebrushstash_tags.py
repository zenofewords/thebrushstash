from decimal import Decimal

from django import template
from django.utils.translation import get_language

from shop.constants import EMPTY_BAG
from shop.utils import get_shipping_cost
from thebrushstash.constants import (
    DEFAULT_REGION,
)
from thebrushstash.models import (
    CreditCardLogo,
    FooterItem,
    FooterShareLink,
    NavigationItem,
    Region,
)

register = template.Library()


@register.inclusion_tag('thebrushstash/tags/navigation.html', takes_context=True)
def navigation_tag(context):
    request = context.get('request')
    return {
        'current_url': request.path if request else '/',
        'navigation_items': NavigationItem.published_objects.all(),
        'bag': request.session.get('bag'),
        'LANGUAGE_CODE': request.session.get('_language'),
    }


@register.inclusion_tag('thebrushstash/tags/ship_to.html', takes_context=True)
def ship_to_tag(context):
    request = context.get('request')

    language = get_language()
    if not request.session.get('_language'):
        request.session['_language'] = language

    regions = Region.published_objects.all()
    default = regions.get(name=DEFAULT_REGION)
    default_region = default if language == default.name else regions.first()
    region = request.session.get('region')

    if not region:
        request.session['region'] = default_region.name
        selected_region = default_region
    else:
        selected_region = regions.get(name=region)

    bag = request.session.get('bag')
    if not bag:
        request.session['bag'] = EMPTY_BAG

    shipping_cost = get_shipping_cost(
        Decimal(selected_region.shipping_cost), request.session['bag']
    )
    request.session['bag']['shipping_cost'] = str(shipping_cost)
    request.session['bag']['grand_total'] = str(
        Decimal(request.session['bag']['total']) + shipping_cost
    )
    request.session.modified = True

    return {
        'selected_region': selected_region,
        'regions': regions.exclude(name=selected_region.name),
    }


@register.inclusion_tag('thebrushstash/tags/footer.html')
def footer_tag(hide_social=False):
    return {
        'hide_social': hide_social,
        'footer_items': FooterItem.published_objects.all(),
        'footer_share_links': FooterShareLink.published_objects.all(),
    }


@register.inclusion_tag('thebrushstash/tags/cookie.html', takes_context=True)
def cookie_tag(context):
    request = context.get('request')

    return {
        'accepted': request.session.get('accepted', None) if request else None,
    }


@register.inclusion_tag('thebrushstash/tags/credit_card_logos.html')
def credit_card_logos_tag():
    return {
        'credit_card_logos': CreditCardLogo.published_objects.all(),
    }


@register.inclusion_tag('thebrushstash/tags/newsletter.html')
def newsletter_tag():
    pass
