from django import template
from django.utils.translation import get_language

from shop.constants import EMPTY_BAG
from shop.utils import set_tax
from thebrushstash.constants import DEFAULT_REGION
from thebrushstash.models import (
    CreditCardLogo,
    ExchangeRate,
    FooterItem,
    FooterShareLink,
    NavigationItem,
    Region,
)

register = template.Library()


@register.inclusion_tag('thebrushstash/tags/navigation_tag.html', takes_context=True)
def navigation_tag(context):
    request = context['request']

    exchange_rates = {}
    for exchange_rate in ExchangeRate.objects.all():
        exchange_rates[exchange_rate.currency.lower()] = exchange_rate.middle_rate

    return {
        'current_url': request.path,
        'navigation_items': NavigationItem.published_objects.all(),
        'bag': request.session.get('bag'),
        'currency': request.session.get('currency', 'hrk'),
        'exchange_rates': exchange_rates,
        'LANGUAGE_CODE': request.session.get('_language'),
    }


@register.inclusion_tag('thebrushstash/tags/ship_to_tag.html', takes_context=True)
def ship_to_tag(context, prefix=''):
    session = context['request'].session
    regions = Region.published_objects.all()
    default = regions.get(name=DEFAULT_REGION)

    language = get_language()
    if language != session.get('_language'):
        session['_language'] = language

    default_region = default if language == default.name else regions.first()
    region = session.get('region')

    if not region or language == default.name:
        session['region'] = default_region.name
        selected_region = default_region
    else:
        selected_region = regions.get(name=region)

    bag = session.get('bag')
    if not bag:
        session['bag'] = EMPTY_BAG

    session['currency'] = selected_region.currency
    set_tax(session['bag'])
    session.modified = True

    return {
        'selected_region': selected_region,
        'regions': regions.exclude(name=selected_region.name),
        'bag': session['bag'],
        'prefix': prefix,
    }


@register.inclusion_tag('thebrushstash/tags/ship_to_tag_mobile.html', takes_context=True)
def ship_to_tag_mobile(context, prefix=''):
    return ship_to_tag(context, prefix)


@register.inclusion_tag('thebrushstash/tags/footer_tag.html', takes_context=True)
def footer_tag(context, hide_social=False):
    request = context['request']
    return {
        'hide_social': hide_social,
        'footer_items': FooterItem.published_objects.all(),
        'footer_share_links': FooterShareLink.published_objects.all(),
        'LANGUAGE_CODE': request.session.get('_language'),
    }


@register.inclusion_tag('thebrushstash/tags/cookie_tag.html', takes_context=True)
def cookie_tag(context):
    request = context['request']
    accepted = request.user.is_authenticated and request.user.accepted_cookies
    return {
        'accepted': accepted or request.session.get('accepted', False),
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
