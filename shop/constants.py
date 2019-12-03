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
    'tax': 0,
}

DEFAULT_IMAGE_QUALITY = 80
DEFAULT_DENSITY = 1

LANDSCAPE = 'landscape'
LANDSCAPE_WIDTH = 730
SQUARE = 'square'
SQUARE_WIDTH = 480
THUMBNAIL = 'thumbnail'
THUMBNAIL_WIDTH = 70

VARIATIONS = ['webp_desktop', 'webp_mobile', 'jpg_desktop', 'jpg_mobile']
SLOTS = [
    {
        'shape': LANDSCAPE,
        'ratio': 1.678,
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

default_shipping_cost = Setting.objects.filter(name='DEFAULT_SHIPPING_COST').first()
free_shipping_products = Setting.objects.filter(name='FREE_SHIPPING_PRODUCTS').first()
free_shipping_price = Setting.objects.filter(name='FREE_SHIPPING_PRICE').first()
gle_fee = Setting.objects.filter(name='GLS_FEE').first()
tax = Setting.objects.filter(name='TAX').first()

DEFAULT_SHIPPING_COST = default_shipping_cost.value if default_shipping_cost else '10'
FREE_SHIPPING_PRODUCTS = free_shipping_products.value if free_shipping_products else '3'
FREE_SHIPPING_PRICE = free_shipping_price.value if free_shipping_price else '2000'
GLS_FEE = gle_fee.value if gle_fee else '30'
TAX = tax.value if tax else '0.25'
