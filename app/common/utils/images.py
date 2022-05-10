import os

from fastapi import UploadFile

from PIL import Image


def compress_img(image, path: str, quality: int = 60):
    img = Image.open(image)
    img.save(path, 'JPEG', quality=quality, optimize=True)


def save_compress_image_file(
    file: UploadFile, folder: str, image_prefix: str
) -> dict:
    if not os.path.exists(folder):
        os.makedirs(folder)

    image_paths = {}
    qualities = {"small": 20, "medium": 40, "original": 100}
    for quality_name, quality_value in qualities.items():

        _, extension = os.path.splitext(file.filename) 
        image_name = f"{image_prefix}_{quality_name}{extension}"
        image_path = folder + image_name

        compress_img(file.file, image_path, quality=quality_value)
        # add slash to path because this is the static path
        image_paths[quality_name] = "/" + image_path

    return image_paths
