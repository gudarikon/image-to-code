from PIL import Image


def prepare_image(image: Image) -> Image:
    """
    Turns image to Black-White mode and adds background frame

    :param image: PIL Image object
    :return: prepared image
    """
    image = image.convert("L")

    img_w, img_h = image.size
    background = Image.new('L', (int(img_w * 1.2), int(img_h * 1.2)), 255)
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(image, offset)
    return background
