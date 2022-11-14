from pathlib import Path

import click
import pytesseract

from utils import prepare_image


def img_to_text(img_path: Path):
    image = prepare_image(img_path)
    text = pytesseract.image_to_string(image, config='--psm 4')
    return text


@click.argument("img_path", type=Path)
def func_img_to_text(img_path: Path):
    print(img_to_text(img_path))


f_img_to_text = click.command()(func_img_to_text)

if __name__ == "__main__":
    # Should insert the path to your tesseract.exe file
    pytesseract.pytesseract.tesseract_cmd = r'D:\Applications\Tesseract\Tesseract-OCR\tesseract'
    f_img_to_text()
