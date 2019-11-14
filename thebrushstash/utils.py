import copy
import os
from decimal import Decimal
from pathlib import Path
from PIL import Image
from webptools import webplib

from django.utils.safestring import mark_safe

from thebrushstash.constants import (
    LARGE_IMAGE_WIDTH,
    IMAGE_SCALING_PARAMS,
    IMAGE_SRCSETS,
    SIZE_LARGE,

    SQUARE,
    SQUARE_WIDTH,
    SRCSET_MAPPING,
    SLOTS,
    DEFAULT_IMAGE_QUALITY,
    DEFAULT_IMAGE_EXTENSION,
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
        ratio = original_width / width
        height = original_height / ratio

        return mark_safe(
            '<img src={url} width={width} height={height} />'.format(
                url=image.url,
                width=width,
                height=height,
            )
        )
    except FileNotFoundError:  # noqa
        return ''


def get_resized_path(path, size, width, ext=DEFAULT_IMAGE_EXTENSION):
    return path.replace(
        os.path.basename(path), '{}_{}_{}.{}'.format(Path(path).stem, size, width, ext)
    )


def get_srcset(path, size, width, density, ext=DEFAULT_IMAGE_EXTENSION):
    return '{} {}x'.format(get_resized_path(path, size, width, ext), density)


def generate_srcsets(path, url, original, image_srcsets, image_scaling_params, quality=70):
    width = original.width
    height = original.height
    ratio = width / height if width > height else height / width

    scale_params = [(p[0], int(p[0] / ratio), p[1], p[2], p[3]) for p in image_scaling_params]
    for width, height, operation, density, size in scale_params:
        if operation == 'crop':
            resized_image = original.resize((width * 3, height * 3), resample=Image.BICUBIC)
            resized_image = resized_image.crop((
                resized_image.width / 2 - width / 2,
                resized_image.height / 2 - height / 2,
                resized_image.width / 2 + width / 2,
                resized_image.height / 2 + height / 2,
            ))
        else:
            resized_image = original.resize((width, height), resample=Image.BICUBIC)

        resized_image_path = get_resized_path(path, size, width)
        resized_image.save(resized_image_path, 'JPEG', optimize=True, quality=quality)

        webp_image_path = get_resized_path(path, size, width, 'webp')
        webplib.cwebp(resized_image_path, webp_image_path, '-q {}'.format(quality))

        image_srcsets['webp_{}'.format(size)].append(get_srcset(url, size, width, density, 'webp'))
        image_srcsets['jpg_{}'.format(size)].append(get_srcset(url, size, width, density))
    return image_srcsets


def create_image_variations(instance, created, resize=True):
    if not instance.image and instance.srcsets:
        instance.srcsets = {}
        instance.save()

    if instance.srcsets or not instance.image:
        return

    path = instance.image.path
    url = instance.image.url
    original = Image.open(path)

    if Image.MIME[original.format] == 'image/png':
        canvas = Image.new('RGB', (original.width, original.height), color=(255, 255, 255))
        canvas.paste(original, original)
        original = canvas.convert('RGB')

    if resize:
        instance.image = get_resized_path(instance.image.name, SIZE_LARGE, LARGE_IMAGE_WIDTH)
        image_srcsets = generate_srcsets(
            path, url, original, copy.deepcopy(IMAGE_SRCSETS), IMAGE_SCALING_PARAMS
        )
    else:
        srcsets = {
            'webp_original': [],
            'jpg_original': [],
        }
        scale_params = ((original.width, 'resize', 1, 'original'),)
        image_srcsets = generate_srcsets(path, url, original, srcsets, scale_params, 90)
        instance.image = get_resized_path(instance.image.name, 'original', original.width)

    instance.srcsets = image_srcsets
    instance.save()
    os.remove(path)


def get_resized_path_b(path, size, width, ext=DEFAULT_IMAGE_EXTENSION):
    return path.replace(
        os.path.basename(path), '{}_{}_{}.{}'.format(Path(path).stem, size, width, ext)
    )


def process_image(original, dimensions, original_width, original_height, width, height, ratio):
    crop_x = (original_width - width) / 2
    crop_y = (original_height - height) / 2

    cropped = original.crop((crop_x, crop_y, original_width - crop_x, original_height - crop_y))

    resized_images = []
    for dimension in dimensions:
        new_width = 0
        new_height = 0

        if ratio == 1:
            new_width, new_height = dimension, dimension
        else:
            new_width = dimension
            new_height = dimension / ratio

        resized_image = cropped.resize((int(new_width), int(new_height)), resample=Image.BICUBIC)
        resized_image.show()
        resized_images.append(resized_image)
    return resized_images


def generate_srcsets_b(path, url, original, srcset_mapping, slots, quality=DEFAULT_IMAGE_QUALITY):
    original_width = original.width
    original_height = original.height
    original_ratio = Decimal(original_width / original_height)

    for slot in slots:
        width = 0
        height = 0
        shape = slot.get('shape')
        ratio = slot.get('ratio')
        dimensions = slot.get('dimensions')

        if original_ratio >= 1 and ratio < 1:
            width = original_height * ratio
            height = original_height
            processed_images = process_image(
                original, dimensions, original_width, original_height, width, height, ratio
            )

        elif original_ratio >= 1 and ratio > 1:
            width = original_height
            height = original_height / ratio
            processed_images = process_image(
                original, dimensions, original_width, original_height, width, height, ratio
            )

        elif original_ratio >= 1 and ratio == 1:
            x = original_width if original_width < original_height else original_height
            processed_images = process_image(
                original, dimensions, original_width, original_height, x, x, ratio
            )

        # todo r < 1

    raise Exception(':)')
    return srcset_mapping

    # resized_image = original.resize((width, height), resample=Image.BICUBIC)

    # resized_image_path = get_resized_path(path, size, width)
    # resized_image.save(resized_image_path, 'JPEG', optimize=True, quality=quality)

    # webp_image_path = get_resized_path(path, size, width, 'webp')
    # webplib.cwebp(resized_image_path, webp_image_path, '-q {}'.format(quality))

    # image_srcsets['webp_{}'.format(size)].append(get_srcset(url, size, width, density, 'webp'))
    # image_srcsets['jpg_{}'.format(size)].append(get_srcset(url, size, width, density))


def create_image_variations_b(instance, created):
    # clear srcsets if image is removed
    if not instance.image and instance.srcsets:
        instance.srcsets = {}
        instance.save()

    # stop if no image or already has srcsets
    if not instance.image or instance.srcsets:
        return

    path = instance.image.path
    url = instance.image.url
    original = Image.open(path)

    # remove transparent background
    if Image.MIME[original.format] == 'image/png':
        canvas = Image.new('RGB', (original.width, original.height), color=(255, 255, 255))
        canvas.paste(original, original)
        original = canvas.convert('RGB')

    # save default (fallback) image
    instance.image = get_resized_path_b(instance.image.name, SQUARE, SQUARE_WIDTH, 'jpg')
    image_srcsets = generate_srcsets_b(path, url, original, copy.deepcopy(SRCSET_MAPPING), SLOTS)

    instance.srcsets = image_srcsets
    instance.save()
    # remove original image
    os.remove(path)
