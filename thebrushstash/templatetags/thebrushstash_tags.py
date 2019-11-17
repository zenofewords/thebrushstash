import copy

from django import template

from thebrushstash.constants import (
    DEFAULT_REGION,
    REGIONS,
)
from thebrushstash.models import (
    CreditCardLogo,
    FooterItem,
    FooterShareLink,
    NavigationItem,
)

register = template.Library()


@register.inclusion_tag('thebrushstash/tags/navigation.html', takes_context=True)
def navigation_tag(context):
    request = context.get('request')
    return {
        'current_url': request.path if request else '/',
        'navigation_items': NavigationItem.published_objects.all(),
        'bag': request.session.get('bag'),
    }


@register.inclusion_tag('thebrushstash/tags/ship_to.html', takes_context=True)
def ship_to_tag(context):
    request = context.get('request')

    default_region = DEFAULT_REGION if request.LANGUAGE_CODE == DEFAULT_REGION else 'eu'
    region = request.session.get('region')

    if not region:
        request.session['region'] = default_region
        selected_region = default_region
    else:
        selected_region = region
    regions_copy = copy.deepcopy(REGIONS)
    regions_copy.pop(selected_region)

    return {
        'selected_region': selected_region,
        'regions': regions_copy,
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
