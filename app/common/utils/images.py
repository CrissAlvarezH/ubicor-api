import os

from fastapi import UploadFile
from PIL import Image


def compress_img(image, path: str, resize_factor: int = 1, quality: int = 50):
    img = Image.open(image)
    width, height = img.size
    new_width = int(width / resize_factor)
    new_height = int(height / resize_factor)
    img = img.resize((new_width, new_height))
    img.save(path, "JPEG", quality=quality, optimize=True)


def save_compress_image_file(
    file: UploadFile, folder: str, image_prefix: str
) -> dict:
    if not os.path.exists(folder):
        os.makedirs(folder)

    image_paths = {}
    qualities = {"small": 7, "medium": 4, "original": 1}
    for quality_name, quality_value in qualities.items():

        _, extension = os.path.splitext(file.filename)
        image_name = f"{image_prefix}_{quality_name}{extension}"
        image_path = folder + image_name

        compress_img(file.file, image_path, resize_factor=quality_value)
        # add slash to path because this is the static path
        image_paths[quality_name] = "/" + image_path

    return image_paths
