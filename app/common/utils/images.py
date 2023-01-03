import os
from datetime import datetime

from fastapi import UploadFile
from PIL import Image


def compress_img(image, path: str, resize_factor: int = 1, quality: int = 50):
    img = Image.open(image)
    width, height = img.size
    new_width = int(width / resize_factor)
    new_height = int(height / resize_factor)
    img = img.resize((new_width, new_height))
    prefix_path, _ = os.path.splitext(path)
    path_jpg = prefix_path + ".png"
    img.save(path_jpg, quality=quality, optimize=True)


def save_compress_image_file(
    file: UploadFile, folder: str, image_prefix: str
) -> dict:
    if not os.path.exists(folder):
        os.makedirs(folder)

    image_paths = {}
    qualities = {"small": 7, "medium": 4, "original": 1}
    for quality_name, quality_value in qualities.items():

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        image_name = f"{image_prefix}_{quality_name}_{timestamp}.png"
        image_path = folder + image_name

        compress_img(file.file, image_path, resize_factor=quality_value)
        # add slash to path because this is the static path
        image_paths[quality_name] = "/" + image_path

    return image_paths
