from PIL import Image, ImageOps
import os
from django.conf import settings


def resize_image(img, new_width=400):
    image_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
    image_pil = Image.open(image_full_path)
    image_pil = ImageOps.exif_transpose(image_pil)
    original_width, original_height = image_pil.size

    if original_width <= new_width:
        image_pil.close()
        return

    new_height = round(original_height * (new_width / original_width))

    new_image = image_pil.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    new_image.save(
        image_full_path,
        quality=50,
        optimize=True,
    )
