import collections
from typing import Tuple

import cv2
import numpy as np
from PIL import Image, ImageEnhance


def convert_from_cv2_to_image(img: np.ndarray, transform_type: int) -> Image:
    return Image.fromarray(cv2.cvtColor(img, transform_type))


def convert_from_image_to_cv2(img: Image, transform_type: int) -> np.ndarray:
    return cv2.cvtColor(np.array(img), transform_type)


def get_image_top_color(image: Image) -> Tuple:
    """
    Gets image and returns most common color of it
    :param image: source PIL.Image
    :return: tuple of colors of image (could be RGB, RGBA)
    """
    im = image.resize((50, 50))
    ar = np.asarray(im)
    color_len = ar.shape[-1]
    ar = np.resize(im, (50 * 50, color_len))
    counter = collections.Counter([tuple(elem) for elem in ar])
    return counter.most_common(1)[0][0]


def resize_image(image: Image, target_len_size: float = 2048) -> Image:
    """
    Resizes the image proportionally up to given quality

    :param image: source PIL.Image object
    :param target_len_size: target image width
    :return: resized PIL.Image object
    """
    length_x, width_y = image.size
    factor = target_len_size / length_x
    size = int(factor * length_x), int(factor * width_y)

    return image.resize(size, Image.Resampling.LANCZOS)


def preprocess_image(image: Image) -> Image:
    """
    Makes preprocessing of image
    Raw version of function

    :param image: source PIL.Image object
    :return: thresholded PIL.Image
    """
    image = ImageEnhance.Sharpness(image).enhance(2)

    img = convert_from_image_to_cv2(image, cv2.COLOR_RGB2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.fastNlMeansDenoising(img, None, 10, 10, 7)

    #img = cv2.GaussianBlur(img, (3, 3), 0)
    #(thresh, img) = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    if np.median(img) <= 127:
        img = 255 - img

    img = convert_from_cv2_to_image(img, cv2.COLOR_GRAY2RGB)
    return img


def add_frame(image: Image, frame_border_size: float = 0.2):
    """
    Adds padding border to image

    :param image: source PIL.Image object in RGB mode
    :param frame_border_size: relative border size (0.1 will be equal to 0.1 of image's params)
    :return: PIL.Image in RGB mode with frame
    """
    assert frame_border_size > 0, "Frame border size setting cannot be non positive number"

    top_color = get_image_top_color(image)

    img_w, img_h = image.size
    background = Image.new(
        'RGB',
        (int(img_w * (1 + frame_border_size)), int(img_h * (1 + frame_border_size))),
        top_color
    )
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(image, offset)

    return background


def prepare_image(image: Image) -> Image:
    """
    Turns image to Black-White mode and adds background frame

    :param image: PIL Image object
    :return: prepared image
    """

    image = resize_image(image)
    image = add_frame(image, 0.1)

    image = preprocess_image(image)

    image = image.convert("L")

    return image
