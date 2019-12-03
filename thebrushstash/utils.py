import copy
import hashlib
import hmac
import os
import secrets

from decimal import Decimal
from pathlib import Path
from PIL import Image
from webptools import webplib

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.utils.timezone import now

from account.models import (
    CustomUser,
    NewsletterRecipient,
)
from account.tokens import account_activation_token
from shop.constants import (
    DEFAULT_IMAGE_QUALITY,
    EMPTY_BAG,
    SLOTS,
    SQUARE,
    SRCSET_MAPPING,
)
from shop.models import (
    Invoice,
    InvoiceItem,
    InvoiceStatus,
    Product,
)
from thebrushstash.constants import currency_symbol_mapping
from thebrushstash.models import Country


def get_country(country_name):
    return Country.objects.get(slug=slugify(country_name))


def get_default_link_data(data):
    return {
        'name': data.get('name'),
        'ordering': data.get('ordering'),
        'location': data.get('location', ''),
        'external': data.get('external', False),
        'published': data.get('published', False),
        'css_class': data.get('css_class', ''),
    }


def get_preview_image(image, max_width):
    try:
        if not image:
            return ''

        original_width = image.width
        original_height = image.height

        width = original_width if original_width < max_width else max_width
        slot_ratio = original_width / width
        height = original_height / slot_ratio

        return mark_safe(
            '<img src={url} width={width} height={height} />'.format(
                url=image.url,
                width=width,
                height=height,
            )
        )
    except FileNotFoundError:  # noqa
        return ''


def get_resized_path(path, shape, size, extension):
    return path.replace(
        os.path.basename(path), '{}_{}_{}.{}'.format(Path(path).stem, shape, size, extension)
    )


def get_srcset(url, shape, size, extension, density):
    return '{} {}x'.format(get_resized_path(url, shape, size, extension), density)


def crop_image(original, original_width, original_height, width, height):
    crop_x = (original_width - width) / 2
    crop_y = (original_height - height) / 2

    return original.crop((crop_x, crop_y, original_width - crop_x, original_height - crop_y))


def create_variations(path, cropped_image, slot):
    slot_shape = slot.get('shape')
    slot_ratio = slot.get('ratio')

    for size, dimension in slot.get('dimensions').items():
        new_width = 0
        new_height = 0

        if slot_ratio == 1:
            new_width, new_height = dimension, dimension
        else:
            new_width = dimension
            new_height = dimension / slot_ratio

        # resize image to new width and height
        resized_image = cropped_image.resize(
            (int(new_width), int(new_height)), resample=Image.BICUBIC,
        )

        # create jpg image
        resized_image_path = get_resized_path(path, slot_shape, size, 'jpg')
        resized_image.save(resized_image_path, 'JPEG', optimize=True, quality=DEFAULT_IMAGE_QUALITY)

        # create webp image
        webp_image_path = get_resized_path(path, slot_shape, size, 'webp')
        webplib.cwebp(resized_image_path, webp_image_path, '-q {}'.format(DEFAULT_IMAGE_QUALITY))


def generate_srcsets(path, url, original, slots):
    original_width = original.width
    original_height = original.height
    original_ratio = Decimal(original_width / original_height)
    srcset_mapping = copy.deepcopy(SRCSET_MAPPING)

    for slot in slots:
        width = 0
        height = 0
        slot_ratio = slot.get('ratio')

        if slot_ratio - 0.15 < original_ratio < slot_ratio + 0.15:
            create_variations(path, original, slot)
        else:
            if original_ratio >= 1 and slot_ratio < 1:
                width = original_height * slot_ratio
                height = original_height
            elif original_ratio >= 1 and slot_ratio > 1:
                width = original_height
                height = original_height / slot_ratio
            elif original_ratio < 1 and slot_ratio < 1:
                width = original_width * slot_ratio
                height = original_width
            elif original_ratio < 1 and slot_ratio > 1:
                width = original_width
                height = original_width / slot_ratio
            else:  # slot_ratio == 1
                width = height = original_width if original_width < original_height else original_height

            cropped_image = crop_image(original, original_width, original_height, width, height)
            create_variations(path, cropped_image, slot)

    for key in srcset_mapping.keys():
        extension, device, shape = key.split('_')

        properties = (('large', 2), ('medium', 1), )
        if device == 'mobile':
            properties = (('medium', 2), ('small', 1), )

        for prop in properties:
            srcset_mapping[key].append(get_srcset(url, shape, prop[0], extension, prop[1]))
    return srcset_mapping


def create_image_variations(instance, created):
    # clear srcsets if image is removed
    if not instance.image and instance.srcsets:
        instance.srcsets = {}
        instance.save()

    # stop if no image or already has srcsets
    if not instance.image or instance.srcsets:
        return

    path = instance.image.path
    # need the original image's URL
    url = instance.image.url

    with Image.open(path) as original:
        original = Image.open(path)

        # remove background transparency
        if Image.MIME[original.format] == 'image/png':
            canvas = Image.new('RGB', (original.width, original.height), color=(255, 255, 255))
            canvas.paste(original, original)
            original = canvas.convert('RGB')

        # save default (fallback) image
        instance.image = get_resized_path(instance.image.name, SQUARE, 'small', 'jpg')
        instance.srcsets = generate_srcsets(path, url, original, SLOTS)
        instance.save()
        # remove original image
        os.remove(path)


def update_user_information(user, email, data):
    user.username = email
    user.email = email

    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.country = get_country(data.get('country'))
    user.city = data.get('city')
    user.address = data.get('address')
    user.zip_code = data.get('zip_code')

    user.phone_number = data.get('phone_number', '')
    user.state_county = data.get('state_county', '')
    user.company_name = data.get('company_name', '')
    user.company_address = data.get('company_address', '')
    user.company_uin = data.get('company_uin', '')
    user.save()


def register_user(data, current_site):
    email = data.get('email')
    user = CustomUser.objects.filter(email=email).first()

    if user:
        update_user_information(user, email, data)
    elif data.get('register') and email:
        user = CustomUser()
        user.is_active = False

        update_user_information(user, email, data)
        send_registration_email(user, current_site)
    return user


def subscribe_to_newsletter(user, data):
    if data.get('subscribe_to_newsletter'):
        email = data.get('email')
        obj, created = NewsletterRecipient.objects.get_or_create(
            email=email,
            defaults={
                'subscribed': True,
                'user': user,
            }
        )
        # link user to newsletter subscription
        if user and not created and not obj.user:
            obj.user = user
            obj.save()


def safe_subscribe_to_newsletter(user, email, current_site):
    obj, created = NewsletterRecipient.objects.get_or_create(
        email=email,
        defaults={
            'subscribed': True if user.is_authenticated else False,
            'user': user if user.is_authenticated else None,
        }
    )
    if user.is_authenticated and not created:
        return _('Already subscribed.')
    if user.is_authenticated and created:
        return _('Subscribed, thanks!')

    send_subscription_email(email, current_site)
    return _('Check your e-mail for confirmation!')


def create_or_update_invoice(order_number, user, cart, data, payment_method=''):
    invoice = Invoice.objects.filter(order_number=order_number).first()

    if not invoice:
        invoice = Invoice()
        invoice.order_number = 'tbs_{}_{}'.format(
            secrets.token_urlsafe(12), now().time().microsecond
        )

    invoice.email = data.get('email')
    invoice.first_name = data.get('first_name')
    invoice.last_name = data.get('last_name')
    invoice.country = get_country(data.get('country'))
    invoice.city = data.get('city')
    invoice.address = data.get('address')
    invoice.zip_code = data.get('zip_code')

    invoice.state_county = data.get('state_county', '')
    invoice.company_name = data.get('company_name', '')
    invoice.company_address = data.get('company_address', '')
    invoice.company_uin = data.get('company_uin', '')
    invoice.note = data.get('note', '')

    invoice.status = InvoiceStatus.PENDING
    invoice.cart = cart
    invoice.user = user
    invoice.save()
    return invoice.order_number


def send_registration_email(user, current_site):
    message_html = render_to_string('account/account_verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'site_name': current_site.name,
        'protocol': 'http' if settings.DEBUG else 'https',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    subject = _('Activate your account')
    send_mail(subject, '', 'The Brush Stash', [user.email], html_message=message_html)


def send_subscription_email(email, current_site):
    message_html = render_to_string('account/subscription_verification_email.html', {
        'domain': current_site.domain,
        'site_name': current_site.name,
        'protocol': 'http' if settings.DEBUG else 'https',
        'uid': urlsafe_base64_encode(force_bytes(email)),
    })
    subject = _('Subscribe to newsletter')
    send_mail(subject, '', 'The Brush Stash', [email], html_message=message_html)


def send_purchase_mail(email_address, current_site, invoice, bag):
    message_html = render_to_string('shop/purchase_complete_email.html', {
        'domain': current_site.domain,
        'site_name': current_site.name,
        'protocol': 'http' if settings.DEBUG else 'https',
        'invoice': invoice,
        'invoice_items': InvoiceItem.objects.filter(
            invoice=invoice).select_related('invoice', 'product'),
        'bag': bag,
    })
    subject = _('Purchase complete')
    send_mail(subject, '', 'The Brush Stash', [email_address], html_message=message_html)


def get_cart(bag):
    products = bag.get('products')

    cart = []
    for product in products:
        cart.append('{} {}x'.format(
            products[product].get('name'),
            products[product].get('quantity')
        ))
    return ' '.join(cart)


def get_signature(data):
    return hmac.new(
        bytes(settings.IPG_API_KEY, 'utf-8'),
        msg=bytes(''.join(['{}{}'.format(x, y) for x, y in data.items()]), 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest().lower()


def signature_is_valid(data):
    return data.get('signature') == hmac.new(
        bytes(settings.IPG_API_KEY, 'utf-8'),
        msg=bytes(
            'approval_code{}language{}order_number{}'.format(
                data.get('approval_code'),
                data.get('language'),
                data.get('order_number')
            ),
            'utf-8'
        ),
        digestmod=hashlib.sha256
    ).hexdigest().lower()


def complete_purchase(session, invoice_status, request):
    invoice = Invoice.objects.filter(order_number=session['order_number']).first()

    if invoice:
        phone_number = request.POST.get('phone_number', '')
        invoice.status = invoice_status
        invoice.order_total = session['bag']['grand_total_hrk']  # must be in hrk
        invoice.payment_method = session['payment_method']
        invoice.phone_number = phone_number
        invoice.save()

        update_inventory(invoice, session['bag']['products'])

        send_purchase_mail(
            session['user_information']['email'],
            get_current_site(request),
            invoice,
            session['bag'],
        )
        session['bag'] = EMPTY_BAG
        session['order_number'] = None
        session['user_information']['phone_number'] = phone_number
        session['user_information']['note'] = None


def format_price(currency, price):
    if currency == 'hrk':
        return '{} {}'.format(price, currency_symbol_mapping[currency])
    return '{}{}'.format(currency_symbol_mapping[currency], price)


def check_bag_content(products):
    if len(products.items()) <= 0:
        return _('There\'s nothing in your bag.')

    for key, value in products.items():
        purchase_count = value['quantity']
        product = Product.objects.get(pk=value['pk'])

        if product.in_stock <= 0:
            return _('''
                Looks like {} is all sold out
                You\'ll have to remove it from your bag to continue.'''.format(product.name))
        if product.in_stock < value['quantity']:
            return _('''
                We've got only {} {} left,
                please remove at least {} from your bag to continue.'''.format(
                product.in_stock, product.name, purchase_count - product.in_stock)
            )
    return None


def update_inventory(invoice, products):
    for key, value in products.items():
        sold_count = value['quantity']

        product = Product.objects.get(pk=value['pk'])
        product.in_stock -= sold_count
        product.save()
        InvoiceItem.objects.create(invoice=invoice, product=product, sold_count=sold_count)
