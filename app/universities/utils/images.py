from fastapi import UploadFile

from app.common.utils.images import save_compress_image_file


def save_building_image_file(
    file: UploadFile, building_id: int, image_id: int
) -> str:
    folder = f"app/static/images/buildings/{building_id}/"
    image_prefix = f"building_{building_id}_image_{image_id}"
    return save_compress_image_file(file, folder, image_prefix)
