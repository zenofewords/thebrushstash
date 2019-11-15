import copy
import os
from decimal import Decimal
from pathlib import Path
from PIL import Image
from webptools import webplib

from django.utils.safestring import mark_safe

from thebrushstash.constants import (
    DEFAULT_IMAGE_QUALITY,
    SLOTS,
    SQUARE,
    SRCSET_MAPPING,
)


def get_default_link_data(data):
    return {
        'name': data.get('name'),
        'ordering': data.get('ordering'),
        'location': data.get('location', ''),
        'external': data.get('external', False),
        'published': data.get('published', False),
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
