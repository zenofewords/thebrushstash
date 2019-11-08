from django import template

from shop.models import Showcase

register = template.Library()


@register.inclusion_tag('shop/tags/showcase.html')
def showcase_tag():
    return {
        'showcase': Showcase.published_objects.last(),
    }


@register.inclusion_tag('shop/tags/purchase_summary.html')
def purchase_summary_tag(bag, region, show_links=False):
    return {
        'bag': bag,
        'region': region,
        'show_links': show_links,
    }
