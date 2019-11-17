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
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.models import (
    CustomUser,
    NewsletterRecipient,
)
from account.tokens import account_activation_token
from shop.constants import (
    DEFAULT_IMAGE_QUALITY,
    SLOTS,
    SQUARE,
    SRCSET_MAPPING,
)
from shop.models import (
    Invoice,
    InvoiceStatus,
)
from thebrushstash.models import Country


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
    user.country = Country.objects.get(pk=data.get('country'))
    user.city = data.get('city')
    user.address = data.get('address')
    user.zip_code = data.get('zip_code')

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


def subscribe_to_newsletter(user, data, current_site):
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
        # if created:
            # send_subscription_email(email, current_site)


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
    invoice.country = Country.objects.get(pk=data.get('country'))
    invoice.city = data.get('city')
    invoice.address = data.get('address')
    invoice.zip_code = data.get('zip_code')

    invoice.state_county = data.get('state_county', '')
    invoice.company_name = data.get('company_name', '')
    invoice.company_address = data.get('company_address', '')
    invoice.company_uin = data.get('company_uin', '')
    invoice.note = data.get('note', '')

    invoice.status = InvoiceStatus.PENDING
    invoice.payment_method = payment_method
    invoice.cart = cart
    invoice.user = user
    invoice.save()
    return invoice.order_number


def send_registration_email(user, current_site):
    mail_subject = 'Activate your account'
    message = render_to_string('account/account_verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'site_name': current_site.name,
        'protocol': 'http' if settings.DEBUG else 'https',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()


def send_subscription_email(email_address, current_site):
    mail_subject = 'Subscribed to newsletter'
    message = render_to_string('shop/subscribed_to_newsletter_email.html', {
        'domain': current_site.domain,
        'site_name': current_site.name,
        'protocol': 'http' if settings.DEBUG else 'https',
    })
    EmailMessage(mail_subject, message, to=[email_address]).send()


def get_cart(bag):
    products = bag.get('products')

    cart = []
    for product in products:
        cart.append('{} {}x'.format(
            products[product].get('name'),
            products[product].get('quantity')
        ))
    return ' '.join(cart)


def get_signature(order_number, grand_total, cart, user_information):
    language = 'hr'
    currency = 'HRK'
    require_complete = 'false'

    data = 'amount{}cardholder_email{}cardholder_name{}cardholder_surname{}cart{}currency{}language{}order_number{}require_complete{}store_id{}version{}'.format(
        grand_total,
        user_information.get('email'),
        user_information.get('first_name'),
        user_information.get('last_name'),
        cart,
        currency,
        language,
        order_number,
        require_complete,
        settings.STORE_ID,
        settings.CORVUS_API_VERSION
    )

    return hmac.new(
        bytes(settings.CORVUS_API_KEY, 'utf-8'),
        msg=bytes(data, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest().lower()


def signature_is_valid(data):
    approval_code = data.get('approval_code')
    language = data.get('language')
    order_number = data.get('order_number')

    return data.get('signature') == hmac.new(
        bytes(settings.CORVUS_API_KEY, 'utf-8'),
        msg=bytes('approval_code{}language{}order_number{}'.format(
            approval_code, language, order_number),
            'utf-8'
        ),
        digestmod=hashlib.sha256
    ).hexdigest().lower()
