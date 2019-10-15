from django import template

from thebrushstash.models import (
    CreditCardLogo,
    CreditCardSecureLogo,
    FooterItem,
    FooterShareLink,
    NavigationItem,
)

register = template.Library()


@register.inclusion_tag('thebrushstash/tags/navigation.html', takes_context=True)
def navigation_tag(context):
    return {
        'current_url': context['request'].path,
        'navigation_items': NavigationItem.published_objects.all(),
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


@register.inclusion_tag('thebrushstash/tags/picture.html')
def render_picture(obj, width=None):
    return {
        'object': obj,
        'width': width,
    }
