import sys
from io import BytesIO
from itertools import chain
from typing import Iterable
from uuid import uuid4

from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

SMALL_THUMBNAIL_SIZE = settings.SMALL_THUMBNAIL_SIZE
MEDIUM_THUMBNAIL_SIZE = settings.MEDIUM_THUMBNAIL_SIZE


def get_filename(old_name):
    format = old_name.rsplit('.', 1)[-1]
    return f'{uuid4()}.{format}'


def compress_image(uploaded_image, is_small_thumbnail=False, is_medium_thumbnail=False, quality=50):
    with Image.open(uploaded_image) as tmp_image:
        tmp_image = tmp_image.convert('RGB')
        output_io_stream = BytesIO()
        if is_medium_thumbnail:
            tmp_image.thumbnail(MEDIUM_THUMBNAIL_SIZE)
        if is_small_thumbnail:
            tmp_image.thumbnail(SMALL_THUMBNAIL_SIZE)
        tmp_image.save(output_io_stream, format='JPEG', quality=quality)
        output_io_stream.seek(0)
        uploaded_image = InMemoryUploadedFile(output_io_stream, 'ImageField', f"{uuid4()}.jpg",
                                              'image/jpeg', sys.getsizeof(output_io_stream), None)
        return uploaded_image