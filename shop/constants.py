from thebrushstash.models import Setting

EMPTY_BAG = {
    'products': {},
    'total_quantity': 0,
    'fees': 0,
    'total_hrk': 0,
    'total_eur': 0,
    'total_gbp': 0,
    'total_usd': 0,
    'shipping_cost_hrk': 0,
    'shipping_cost_eur': 0,
    'shipping_cost_gbp': 0,
    'shipping_cost_usd': 0,
    'grand_total_hrk': 0,
    'grand_total_eur': 0,
    'grand_total_gbp': 0,
    'grand_total_usd': 0,
}

DEFAULT_IMAGE_QUALITY = 70
DEFAULT_DENSITY = 1

PORTRAIT = 'portrait'
PORTRAIT_WIDTH = 425
LANDSCAPE = 'landscape'
LANDSCAPE_WIDTH = 650
SQUARE = 'square'
SQUARE_WIDTH = 480
THUMBNAIL = 'thumbnail'
THUMBNAIL_WIDTH = 70

VARIATIONS = ['webp_desktop', 'webp_mobile', 'jpg_desktop', 'jpg_mobile']
SLOTS = [
    {
        'shape': PORTRAIT,
        'ratio': 0.75,
        'dimensions': {
            'large': PORTRAIT_WIDTH * 3,
            'medium': PORTRAIT_WIDTH * 2,
            'small': PORTRAIT_WIDTH,
        },
    },
    {
        'shape': LANDSCAPE,
        'ratio': 1.48,
        'dimensions': {
            'large': LANDSCAPE_WIDTH * 3,
            'medium': LANDSCAPE_WIDTH * 2,
            'small': LANDSCAPE_WIDTH,
        },
    },
    {
        'shape': SQUARE,
        'ratio': 1,
        'dimensions': {
            'large': SQUARE_WIDTH * 3,
            'medium': SQUARE_WIDTH * 2,
            'small': SQUARE_WIDTH,
        },
    },
    {
        'shape': THUMBNAIL,
        'ratio': 1,
        'dimensions': {
            'large': THUMBNAIL_WIDTH * 3,
            'medium': THUMBNAIL_WIDTH * 2,
            'small': THUMBNAIL_WIDTH,
        },
    },
]

SRCSET_MAPPING = {}
for variation in VARIATIONS:
    for shape in [slot.get('shape') for slot in SLOTS]:
        SRCSET_MAPPING['{}_{}'.format(variation, shape)] = []

DEFAULT_SHIPPING_COST = Setting.objects.get(name='DEFAULT_SHIPPING_COST').value
FREE_SHIPPING_PRODUCTS = Setting.objects.get(name='FREE_SHIPPING_PRODUCTS').value
GLS_FEE = Setting.objects.get(name='GLS_FEE').value
