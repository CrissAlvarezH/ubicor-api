from PIL import Image


def compress_img(image, path: str, quality: int = 60):
    img = Image.open(image)
    img.save(path, 'JPEG', quality=quality, optimize=True)

