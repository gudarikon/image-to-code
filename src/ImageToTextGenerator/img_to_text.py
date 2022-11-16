from pathlib import Path

import click
import pytesseract

from utils import prepare_image


def img_to_text(img_path: Path, tesseract_path: str):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    image = prepare_image(img_path)
    text = pytesseract.image_to_string(image, config='--psm 4')
    return text


@click.argument("img_path", type=Path)
@click.argument("tesseract_path", type=str)
def func_img_to_text(img_path: Path, tesseract_path: str):
    print(img_to_text(img_path, tesseract_path))


f_img_to_text = click.command()(func_img_to_text)

if __name__ == "__main__":
    f_img_to_text()
