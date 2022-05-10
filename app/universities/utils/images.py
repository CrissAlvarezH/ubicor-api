import os
from typing import Tuple, Optional

from fastapi import UploadFile

from app.common.utils.images import save_compress_image_file
from app.core.config import settings
from app.universities.models import Image


def is_valid_image(
    image: UploadFile, max_size: int = settings.BUILDINGS_MAX_BYTES_IMAGE_SIZE
) -> Tuple[bool, Optional[str]]:
    image_size = len(image.file.read())
    image.file.seek(0, 0)  # necessary to read again the file

    # validate size
    if image_size > max_size:
        error = f"The image {image.filename} does not meet " \
                f"with size limit {max_size} Bytes"
        return False, error

    return True, None


def save_building_image_file(
    file: UploadFile, building_id: int, image_id: int
) -> str:
    folder = f"app/static/images/buildings/{building_id}/"
    image_prefix = f"building_{building_id}_image_{image_id}"
    return save_compress_image_file(file, folder, image_prefix)


def delete_building_image_file(image: Image):
    # remove building images
    for image_path in [image.small, image.medium, image.original]:
        # remove first slash from path, it's necessary to find the file
        image_path = image_path[1:]
        if os.path.exists(image_path):
            os.remove(image_path)
