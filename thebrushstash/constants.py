exchange_rate_url = 'http://api.hnb.hr/tecajn/v2?valuta=EUR&valuta=USD&valuta=GBP'

country_name_list = (
    'Afghanistan',
    'Albania',
    'Algeria',
    'Andorra',
    'Angola',
    'Antigua & Deps',
    'Argentina',
    'Armenia',
    'Australia',
    'Austria',
    'Azerbaijan',
    'Bahamas',
    'Bahrain',
    'Bangladesh',
    'Barbados',
    'Belarus',
    'Belgium',
    'Belize',
    'Benin',
    'Bhutan',
    'Bolivia',
    'Bosnia Herzegovina',
    'Botswana',
    'Brazil',
    'Brunei',
    'Bulgaria',
    'Burkina',
    'Burundi',
    'Cambodia',
    'Cameroon',
    'Canada',
    'Cape Verde',
    'Central African Rep',
    'Chad',
    'Chile',
    'China',
    'Colombia',
    'Comoros',
    'Congo',
    'Congo (Democratic Rep)',
    'Costa Rica',
    'Croatia',
    'Cuba',
    'Cyprus',
    'Czech Republic',
    'Denmark',
    'Djibouti',
    'Dominica',
    'Dominican Republic',
    'East Timor',
    'Ecuador',
    'Egypt',
    'El Salvador',
    'Equatorial Guinea',
    'Eritrea',
    'Estonia',
    'Ethiopia',
    'Fiji',
    'Finland',
    'France',
    'Gabon',
    'Gambia',
    'Georgia',
    'Germany',
    'Ghana',
    'Greece',
    'Grenada',
    'Guatemala',
    'Guinea',
    'Guinea-Bissau',
    'Guyana',
    'Haiti',
    'Honduras',
    'Hungary',
    'Iceland',
    'India',
    'Indonesia',
    'Iran',
    'Iraq',
    'Ireland (Republic)',
    'Israel',
    'Italy',
    'Ivory Coast',
    'Jamaica',
    'Japan',
    'Jordan',
    'Kazakhstan',
    'Kenya',
    'Kiribati',
    'Korea North',
    'Korea South',
    'Kosovo',
    'Kuwait',
    'Kyrgyzstan',
    'Laos',
    'Latvia',
    'Lebanon',
    'Lesotho',
    'Liberia',
    'Libya',
    'Liechtenstein',
    'Lithuania',
    'Luxembourg',
    'Macedonia',
    'Madagascar',
    'Malawi',
    'Malaysia',
    'Maldives',
    'Mali',
    'Malta',
    'Marshall Islands',
    'Mauritania',
    'Mauritius',
    'Mexico',
    'Micronesia',
    'Moldova',
    'Monaco',
    'Mongolia',
    'Montenegro',
    'Morocco',
    'Mozambique',
    'Myanmar, Burma',
    'Namibia',
    'Nauru',
    'Nepal',
    'Netherlands',
    'New Zealand',
    'Nicaragua',
    'Niger',
    'Nigeria',
    'Norway',
    'Oman',
    'Pakistan',
    'Palau',
    'Panama',
    'Papua New Guinea',
    'Paraguay',
    'Peru',
    'Philippines',
    'Poland',
    'Portugal',
    'Qatar',
    'Romania',
    'Russian Federation',
    'Rwanda',
    'St Kitts & Nevis',
    'St Lucia',
    'Saint Vincent & the Grenadines',
    'Samoa',
    'San Marino',
    'Sao Tome & Principe',
    'Saudi Arabia',
    'Senegal',
    'Serbia',
    'Seychelles',
    'Sierra Leone',
    'Singapore',
    'Slovakia',
    'Slovenia',
    'Solomon Islands',
    'Somalia',
    'South Africa',
    'South Sudan',
    'Spain',
    'Sri Lanka',
    'Sudan',
    'Suriname',
    'Swaziland',
    'Sweden',
    'Switzerland',
    'Syria',
    'Taiwan',
    'Tajikistan',
    'Tanzania',
    'Thailand',
    'Togo',
    'Tonga',
    'Trinidad & Tobago',
    'Tunisia',
    'Turkey',
    'Turkmenistan',
    'Tuvalu',
    'Uganda',
    'Ukraine',
    'United Arab Emirates',
    'United Kingdom',
    'United States',
    'Uruguay',
    'Uzbekistan',
    'Vanuatu',
    'Vatican City',
    'Venezuela',
    'Vietnam',
    'Yemen',
    'Zambia',
    'Zimbabwe',
)

initial_credit_card_logos = (
    {
        'name': 'American Express',
        'ordering': 6,
        'published': True,
        'external': True,
        'location': 'https://www.americanexpress.com/hr/network/',
        'css_class': 'american-express-icon',
    },
    {
        'name': 'Discover',
        'ordering': 5,
        'published': True,
        'external': True,
        'location': 'https://www.discover.com/',
        'css_class': 'discover-icon',
    },
    {
        'name': 'Diners Club',
        'ordering': 4,
        'published': True,
        'external': True,
        'location': 'https://www.diners.com.hr/Pogodnosti-i-usluge/MasterCard- SecureCode.html?Ym5cMzQsY2FyZFR5cGVcMSxwXDc3',
        'css_class': 'diners-club-icon',
    },
    {
        'name': 'Mastercard',
        'ordering': 3,
        'published': True,
        'external': True,
        'location': 'https://www.mastercard.hr/hr-hr.html',
        'css_class': 'mastercard-icon',
    },
    {
        'name': 'Maestro',
        'ordering': 2,
        'published': True,
        'external': True,
        'location': 'http://www.maestrocard.com/hr/',
        'css_class': 'maestro-icon',
    },
    {
        'name': 'Visa',
        'ordering': 1,
        'published': True,
        'external': True,
        'location': 'https://www.visa.com.hr',
        'css_class': 'visa-icon',
    },
)

CONTACT = 'contact'
PAYMENT_DELIVERY = 'payment-and-delivery'
COMPLAINTS = 'returns-and-complaints'
TOS = 'general-terms-and-conditions'
initial_footer_items = (
    {
        'name': 'Contact',
        'location': '/{}/'.format(CONTACT),
        'ordering': 4,
        'published': True,
    },
    {
        'name': 'Payment and delivery',
        'location': '/{}/'.format(PAYMENT_DELIVERY),
        'ordering': 3,
        'published': True,
    },
    {
        'name': 'Returns and complaints',
        'location': '/{}/'.format(COMPLAINTS),
        'ordering': 2,
        'published': True,
    },
    {
        'name': 'General terms and conditions',
        'location': '/{}/'.format(TOS),
        'ordering': 1,
        'published': True,
    },
)

initial_footer_share_links = (
    {
        'name': 'Facebook',
        'ordering': 2,
        'location': 'https://www.facebook.com/TheBrushStash/',
        'external': True,
        'published': True,
        'css_class': 'facebook-icon',
    },
    {
        'name': 'Instagram',
        'ordering': 1,
        'location': 'https://www.instagram.com/thebrushstash',
        'external': True,
        'published': True,
        'css_class': 'instagram-icon',
    },
)

ABOUT = 'about-the-story'
BRUSH_CARE = 'brush-care'
initial_navigation_items = (
    {
        'name': 'Shop',
        'location': '/',
        'ordering': 6,
        'published': True,
    },
    {
        'name': 'Brush Care',
        'location': '/{}/'.format(BRUSH_CARE),
        'ordering': 5,
        'published': True,
    },
    {
        'name': 'About / The Story',
        'location': '/{}/'.format(ABOUT),
        'ordering': 4,
        'published': True,
    },
    {
        'name': 'FAQ',
        'location': '/faq/',
        'ordering': 3,
        'published': True,
    },
)

initial_product_types = (
    {
        'name': 'Brush',
        'slug': 'brush',
    },
)

inital_exchange_rates = (
    {
        'currency': 'GBP',
        'currency_code': '826',
        'state_iso': 'GBR',
        'buying_rate': '8.39528000',
        'middle_rate': '8.42054200',
        'selling_rate': '8.44580400',
        'added_value': '10',
    },
    {
        'currency': 'USD',
        'currency_code': '840',
        'state_iso': 'USA',
        'buying_rate': '6.71698600',
        'middle_rate': '6.73719800',
        'selling_rate': '6.75741000',
        'added_value': '10',
    },
    {
        'currency': 'EUR',
        'currency_code': '978',
        'state_iso': 'EMU',
        'buying_rate': '7.40211900',
        'middle_rate': '7.42439200',
        'selling_rate': '7.44666500',
        'added_value': '10',
    },
)

DEFAULT_IMAGE_EXTENSION = 'jpg'
LARGE_IMAGE_WIDTH = 960
SMALL_IMAGE_WIDTH = 512
THUMBNAIL_IMAGE_WIDTH = 320
DEFAULT_DENSITY = 1
DOUBLE_DENSITY = DEFAULT_DENSITY * 2
SIZE_LARGE = 'large'
SIZE_SMALL = 'small'
SIZE_THUMBNAIL = 'thumbnail'
RESIZE = 'resize'
CROP = 'crop'
IMAGE_SCALING_PARAMS = (
    (LARGE_IMAGE_WIDTH * 2, RESIZE, DOUBLE_DENSITY, SIZE_LARGE),
    (LARGE_IMAGE_WIDTH, RESIZE, DEFAULT_DENSITY, SIZE_LARGE),
    (SMALL_IMAGE_WIDTH * 2, RESIZE, DOUBLE_DENSITY, SIZE_SMALL),
    (SMALL_IMAGE_WIDTH, RESIZE, DEFAULT_DENSITY, SIZE_SMALL),
    (THUMBNAIL_IMAGE_WIDTH * 2, RESIZE, DOUBLE_DENSITY, SIZE_THUMBNAIL),
    (THUMBNAIL_IMAGE_WIDTH, RESIZE, DEFAULT_DENSITY, SIZE_THUMBNAIL),
)
IMAGE_SRCSETS = {
    'webp_{}'.format(SIZE_LARGE): [],
    'webp_{}'.format(SIZE_SMALL): [],
    'webp_{}'.format(SIZE_THUMBNAIL): [],
    'jpg_{}'.format(SIZE_LARGE): [],
    'jpg_{}'.format(SIZE_SMALL): [],
    'jpg_{}'.format(SIZE_THUMBNAIL): [],
}

DEFAULT_REGION = 'hr'
REGIONS = {
    DEFAULT_REGION: {'language': DEFAULT_REGION},
    'eu': {'language': 'en'},
    'uk': {'language': 'en'},
    'us': {'language': 'en'},
}

# vertical_rectangle
# w: 423
# h: 563
# r: 0.75
# horizonal_rectangle
# w: 646
# h: 434
# r: 1.5 (1.48)
# square
# w: 478, 311, 70
# h: 478, 311, 70
# r: 1

DEFAULT_IMAGE_QUALITY = 70
DEFAULT_IMAGE_EXTENSION = 'webp'

VERTICAL_RECTANGLE = 'vertical_rectangle'
VERTICAL_RECTANGLE_WIDTH = 425
HORIZONTAL_RECTANGLE = 'horizonal_rectangle'
HORIZONTAL_RECTANGLE_WIDTH = 650
SQUARE = 'square'
SQUARE_WIDTH = 480
THUMBNAIL = 'thumbnail'
THUMBNAIL_WIDTH = 70

VARIATIONS = ['webp', 'webp_mobile', 'jpg', 'jpg_mobile']
SLOTS = [
    {
        'shape': VERTICAL_RECTANGLE,
        'ratio': 0.75,
        'dimensions': (
            VERTICAL_RECTANGLE_WIDTH * 3,
            VERTICAL_RECTANGLE_WIDTH * 2,
            VERTICAL_RECTANGLE_WIDTH,
        ),
    },
    {
        'shape': HORIZONTAL_RECTANGLE,
        'ratio': 1.5,
        'dimensions': (
            HORIZONTAL_RECTANGLE_WIDTH * 3,
            HORIZONTAL_RECTANGLE_WIDTH * 2,
            HORIZONTAL_RECTANGLE_WIDTH,
        ),
    },
    {
        'shape': SQUARE,
        'ratio': 1,
        'dimensions': (
            SQUARE_WIDTH * 3,
            SQUARE_WIDTH * 2,
            SQUARE_WIDTH,
        ),
    },
    {
        'shape': THUMBNAIL,
        'ratio': 1,
        'dimensions': (
            THUMBNAIL_WIDTH * 3,
            THUMBNAIL_WIDTH * 2,
            THUMBNAIL_WIDTH,
        ),
    },
]

SRCSET_MAPPING = {}
for variation in VARIATIONS:
    for shape in [slot.get('shape') for slot in SLOTS]:
        SRCSET_MAPPING['{}_{}'.format(variation, shape)] = []

# store ratio as decimal

# 2500x2400 image, 1.04 ratio
# if image r > 1 and r < 1, take h, h * r for w
# 1800, 2400, crop from center
# resize to 1275, 1700

# 2500x2400 image, 1.04 ratio
# if image r > 1 and r > 1, take h, h / r for h
# 2400, 1600, crop from center
# resize to 1600, 1067

# 2500x2400 image, 1.04 ratio
# if image r > 1, r == 1, take smaller for both
# 2400, 2400, crop from center
# resize to 620, 620

# 2300x2500 image, 0.92 ratio
# if image r < 1 and r < 1, take w, w * r for w
# 1725, 2300, crop from center
# resize to 1275, 1700

# 2300x2500 image, 0.92 ratio
# if image r < 1 and r > 1, take w, w / r for h
# 2300, 1533, crom from center
# resize to 1600, 1067

# 2300x2500 image, 0.92 ratio
# if image r < 1 and r == 1, take smaller for both
# 2300, 2300, crop from center
# resize to 620, 620

# 2000x2400 image, 0.83 ratio
# if image r < 1 and r < 1, take w, w * r for w
# 1500, 2000, crop from center
# resize to 1275, 1700

# 2000x2400 image, 0.83 ratio
# if image r < 1 and r > 1, take w, w / r for h
# 2000, 1333, crop from center
# resize to 1600, 1067

# 2000x2000 image, 1 ratio
# if r == 1 and r > 1, take either, picked / r for h
# 2000, 1333, crop from center
# resize to 1600, 1067
