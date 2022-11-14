from pathlib import Path

from PIL import Image

def prepare_image(path_to_img: Path) -> Image:
    """
    Turns image to Black-White mode and adds background frame
    :param path_to_img: path to source image file
    :return: prepared image
    """
    image = Image.open(path_to_img)
    image = image.convert("L")

    img_w, img_h = image.size
    background = Image.new('L', (int(img_w * 1.2), int(img_h * 1.2)), 255)
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(image, offset)
    return background
