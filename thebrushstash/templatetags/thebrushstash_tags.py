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
    set_tax(session['bag'])
    session.modified = True

    return {
        'selected_region': selected_region,
        'regions': regions.exclude(name=selected_region.name),
        'bag': session['bag'],
    }


@register.inclusion_tag('thebrushstash/tags/ship_to_tag_mobile.html', takes_context=True)
def ship_to_tag_mobile(context):
    return ship_to_tag(context)


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


@register.simple_tag
def get_font_chars():
    return '''
        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-%C4%8C%C4%86%C4%90%C5%A0%C5%BD
        %C4%8D%C4%87%C4%91%C5%A1%C5%BE%E2%80%98%3F%E2%80%99%E2%80%9C%21%E2%80%9D%28%25%29%5B%23%5D%7B
        %40%7D%2F%26%5C%3C%2B%C3%B7%C3%97%3D%3E%C2%AE%C2%A9%24%E2%82%AC%C2%A3%C2%A5%C2%A2%3A%3B%2C%2A%20
    '''
