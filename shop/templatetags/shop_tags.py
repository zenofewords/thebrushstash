from django import template

from shop.models import Showcase

register = template.Library()


@register.inclusion_tag('shop/tags/showcase.html')
def showcase_tag():
    return {
        'showcase': Showcase.published_objects.last(),
    }
