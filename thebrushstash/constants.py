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

form_mandatory_fields = (
    'address',
    'city',
    'country',
    'email',
    'first_name',
    'last_name',
    'zip_code',
    'shipping_first_name',
    'shipping_last_name',
    'account_shipping_country',
    'shipping_city',
    'shipping_address',
    'shipping_zip_code',
    'shipping_state_county',
)
ipg_fields = (
    'cardholder_address',
    'cardholder_city',
    'cardholder_country',
    'cardholder_email',
    'cardholder_name',
    'cardholder_surname',
    'cardholder_zip_code',
)
form_extra_fields = (
    'phone_number',
    'state_county',
    'phone_number',
    'note',
    'company_name',
    'company_address',
    'company_uin',
    'register',
    'subscribe_to_newsletter',
    'agree_to_terms',
)

initial_credit_card_logos = (
    {
        'name': 'American Express',
        'ordering': 6,
        'published': True,
        'external': True,
        'location': 'https://www.americanexpress.com/hr/network/',
        'css_class': 'american-express-logo-icon',
    },
    {
        'name': 'Discover',
        'ordering': 5,
        'published': True,
        'external': True,
        'location': 'https://www.discover.com/',
        'css_class': 'discover-logo-icon',
    },
    {
        'name': 'Diners Club',
        'ordering': 4,
        'published': False,
        'external': True,
        'location': 'https://www.diners.com.hr/Pogodnosti-i-usluge/MasterCard- SecureCode.html?Ym5cMzQsY2FyZFR5cGVcMSxwXDc3',
        'css_class': 'diners-club-logo-icon',
    },
    {
        'name': 'Mastercard',
        'ordering': 3,
        'published': True,
        'external': True,
        'location': 'https://www.mastercard.hr/hr-hr.html',
        'css_class': 'mastercard-logo-icon',
    },
    {
        'name': 'Maestro',
        'ordering': 2,
        'published': True,
        'external': True,
        'location': 'http://www.maestrocard.com/hr/',
        'css_class': 'maestro-logo-icon',
    },
    {
        'name': 'Visa',
        'ordering': 1,
        'published': True,
        'external': True,
        'location': 'https://www.visa.com.hr',
        'css_class': 'visa-logo-icon',
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
        'css_class': '',
    },
    {
        'name': 'Payment and delivery',
        'location': '/{}/'.format(PAYMENT_DELIVERY),
        'ordering': 3,
        'published': True,
        'css_class': '',
    },
    {
        'name': 'Returns and complaints',
        'location': '/{}/'.format(COMPLAINTS),
        'ordering': 2,
        'published': True,
        'css_class': '',
    },
    {
        'name': 'General terms and conditions',
        'location': '/{}/'.format(TOS),
        'ordering': 1,
        'published': True,
        'css_class': '',
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
        'name': 'Webshop',
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

DEFAULT_COUNTRY = 'Croatia'
DEFAULT_CURRENCY = 'hrk'
DEFAULT_REGION = 'hr'
currency_symbol_mapping = {
    'hrk': 'kn',
    'eur': '€',
    'gbp': '£',
    'usd': '$',
}

initial_region_data = (
    {
        'name': 'eu',
        'language': 'en',
        'currency': 'eur',
        'shipping_cost': '20',
        'published': True,
        'ordering': 3,
    },
    {
        'name': DEFAULT_REGION,
        'language': 'hr',
        'currency': 'hrk',
        'shipping_cost': '10',
        'published': True,
        'ordering': 2,
    },
    {
        'name': 'uk',
        'language': 'en',
        'currency': 'gbp',
        'shipping_cost': '20',
        'published': True,
        'ordering': 1,
    },
    {
        'name': 'us',
        'language': 'en',
        'currency': 'usd',
        'shipping_cost': '30',
        'published': True,
        'ordering': 0,
    },
)

DEFAULT_INSTALLMENT_CODE = 'Y0000'
initial_installment_options = [
    {
        'range_from': '0',
        'range_to': '499.99',
        'installment_number': 2,
    },
    {
        'range_from': '500',
        'range_to': '999.99',
        'installment_number': 3,
    },
    {
        'range_from': '1000',
        'range_to': '1999.99',
        'installment_number': 4,
    },
    {
        'range_from': '2000',
        'range_to': '3999.99',
        'installment_number': 5,
    },
    {
        'range_from': '4000',
        'range_to': '999999999',
        'installment_number': 6,
    },
]
