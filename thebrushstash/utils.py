import copy
import hashlib
import hmac
import io
import os
import secrets

from decimal import Decimal
from pathlib import Path
from PIL import Image
from webptools import webplib
from email.mime.image import MIMEImage

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.staticfiles import finders
from django.core.mail import EmailMultiAlternatives
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
    EmailAudit,
    EmailSource,
    EmailAuditStatus,
    GalleryItem,
    Invoice,
    InvoiceItem,
    InvoiceStatus,
    Product,
)
from thebrushstash.models import (
    Country,
    ExchangeRate,
)


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

        properties = (('large', 3), ('medium', 2), ('small', 1))
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

    active = False
    if user and user.is_active:
        update_user_information(user, email, data)
        active = True
    elif user:
        active = False
    elif data.get('register') and email:
        user = CustomUser()
        user.is_active = False
        update_user_information(user, email, data)

    return user, active


def subscribe_to_newsletter(user, data):
    if data.get('subscribe_to_newsletter'):
        email = data.get('email')
        obj, created = NewsletterRecipient.objects.get_or_create(
            email=email,
            defaults={
                'subscribed': False,
                'user': user,
                'token': get_random_string(),
            }
        )
        # link user to newsletter subscription
        if user and not created and not obj.user:
            obj.user = user
            obj.save()
        return created


def safe_subscribe_to_newsletter(user, email, current_site):
    obj, created = NewsletterRecipient.objects.get_or_create(
        email=email,
        defaults={
            'subscribed': True if user.is_authenticated else False,
            'user': user if user.is_authenticated else None,
            'token': get_random_string(),
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
        invoice.save()
        invoice.order_number = 'TBS_{}'.format(invoice.pk)

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


def start_audit(source, email, payment_method=''):
    email_audit = EmailAudit()
    email_audit.source = source
    email_audit.status = EmailAuditStatus.PENDING
    email_audit.receiver = email
    email_audit.payment_method = payment_method
    email_audit.save()
    return email_audit


def get_logo_attachement():
    logo_path = finders.find('images/tbs-email-logo.png')

    with Image.open(logo_path, mode='r') as tbs_logo_image:
        image_byte_array = io.BytesIO()
        tbs_logo_image.save(image_byte_array, format='png')

        image = MIMEImage(image_byte_array.getvalue(), 'png')
        image.add_header('Content-ID', '<{}>'.format(logo_path))
        image.add_header('Content-Disposition', 'inline', filename='The Brush Stash logo')
    return logo_path, image


def attach_images(message, invoice):
    invoice_items = InvoiceItem.objects.filter(invoice=invoice).select_related('invoice', 'product')

    for invoice_item in invoice_items:
        gallery_item = GalleryItem.objects.filter(
            content_type=ContentType.objects.get_by_natural_key('shop', 'product'),
            object_id=invoice_item.product.pk
        ).first()

        with Image.open(gallery_item.image.path, mode='r') as image:
            image_byte_array = io.BytesIO()
            image.save(image_byte_array, format='jpeg')

            image = MIMEImage(image_byte_array.getvalue(), 'jpeg')

            image.add_header('Content-ID', '<{}>'.format(gallery_item.image.path))
            image.add_header('Content-Disposition', 'inline', filename=invoice_item.product.name)
            message.attach(image)
    return message


def send_registration_email(user, current_site):
    email_audit = start_audit(EmailSource.REGISTRATION, user.email)
    logo_path, logo_image = get_logo_attachement()

    data = {
        'user': user,
        'domain': current_site.domain,
        'site_name': current_site.name,
        'protocol': 'http' if settings.DEBUG else 'https',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'logo_path': logo_path,
    }
    message_txt = render_to_string('account/account_verification_email.txt', data)
    message_html = render_to_string('account/account_verification_email.html', data)
    subject = _('Activate your account')
    message = EmailMultiAlternatives(
        subject, message_html, settings.DEFAULT_FROM_EMAIL, [user.email]
    )
    email_audit.content = message_txt

    message.content_subtype = 'html'
    message.mixed_subtype = 'related'
    message.attach(logo_image)
    send_message(message, email_audit)


def send_subscription_email(email_address, current_site):
    email_audit = start_audit(EmailSource.NEWSLETTER, email_address)
    logo_path, logo_image = get_logo_attachement()

    data = {
        'domain': current_site.domain,
        'site_name': current_site.name,
        'protocol': 'http' if settings.DEBUG else 'https',
        'uid': urlsafe_base64_encode(force_bytes(email_address)),
        'logo_path': logo_path,
    }
    message_txt = render_to_string('account/subscription_verification_email.txt', data)
    message_html = render_to_string('account/subscription_verification_email.html', data)
    message = EmailMultiAlternatives(
        _('Subscribe to newsletter'), message_html, settings.DEFAULT_FROM_EMAIL, [email_address]
    )
    email_audit.content = message_txt

    message.content_subtype = 'html'
    message.mixed_subtype = 'related'
    message.attach(logo_image)
    send_message(message, email_audit)


def send_purchase_email(session, current_site, invoice):
    email_audit = start_audit(EmailSource.PURCHASE, invoice.email, session['payment_method'])

    logo_path, logo_image = get_logo_attachement()
    newsletter_recipient = NewsletterRecipient.objects.filter(user=invoice.user).first()

    include_registration = invoice.user and not invoice.user.is_active
    include_newsletter = newsletter_recipient and not newsletter_recipient.subscribed

    registration_params = {}
    if include_registration:
        registration_params = {
            'user': invoice.user,
            'uid': urlsafe_base64_encode(force_bytes(invoice.user.pk)),
            'token': account_activation_token.make_token(invoice.user),
        }

    if include_newsletter:
        newsletter_recipient.subscribed = True
        newsletter_recipient.save()

    exchange_rates = {}
    for exchange_rate in ExchangeRate.objects.all():
        exchange_rates[exchange_rate.currency.lower()] = exchange_rate.middle_rate

    data = {
        'domain': current_site.domain,
        'site_name': current_site.name,
        'protocol': 'http' if settings.DEBUG else 'https',
        'invoice': invoice,
        'invoice_items': InvoiceItem.objects.filter(
            invoice=invoice).select_related('invoice', 'product'),
        'logo_path': logo_path,
        'bag': session['bag'],
        'currency': session['currency'],
        'include_registration': include_registration,
        'include_newsletter': include_newsletter,
        'exchange_rates': exchange_rates,
        **registration_params,  # noqa
    }
    message_html = render_to_string('shop/purchase_complete_email.html', data)
    message_txt = render_to_string('shop/purchase_complete_email.txt', data)
    email_audit.content = message_txt

    email_address = session['user_information']['email']
    message = EmailMultiAlternatives(
        _('Purchase complete'), message_html, settings.DEFAULT_FROM_EMAIL, [email_address]
    )
    message.content_subtype = 'html'
    message.mixed_subtype = 'related'
    message.attach(logo_image)
    message = attach_images(message, invoice)
    send_message(message, email_audit)


def send_message(message, email_audit):
    try:
        message.send()
        email_audit.sent_at = now()
        email_audit.status = EmailAuditStatus.SENT
    except Exception as error:
        email_audit.status = EmailAuditStatus.FAILED
        email_audit.error_message = error

    email_audit.save()


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
        invoice.order_total = session['bag']['grand_total']  # must be in hrk
        invoice.payment_method = session['payment_method']
        invoice.phone_number = phone_number
        invoice.save()

        update_inventory(invoice, session['bag']['products'])
        current_site = get_current_site(request)

        send_purchase_email(session, current_site, invoice)
        session['bag'] = EMPTY_BAG
        session['order_number'] = None
        session['user_information']['phone_number'] = phone_number
        session['user_information']['note'] = None


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


def get_random_string():
    return '{}-{}'.format(secrets.token_urlsafe(12), now().time().microsecond)
