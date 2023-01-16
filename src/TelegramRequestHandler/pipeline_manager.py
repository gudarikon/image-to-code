from pathlib import Path

import click
from PIL import Image

from ImageToTextGenerator import img_to_text
from TextToCodeGeneration import text_to_code


def img_to_code(image: Image, ocr_processor="PaddleProcessor", ocr_config=None):
    if ocr_config is None:
        ocr_config = {"lang": "en"}
    raw_text = img_to_text(image, ocr_processor, ocr_config)
    parsed_text = text_to_code(raw_text)
    return parsed_text


@click.argument("img_path", type=Path)
def func_img_to_code(img_path: Path):
    image = Image.open(img_path)
    print(img_to_code(image))


f_img_to_code = click.command()(func_img_to_code)

if __name__ == "__main__":
    f_img_to_code()
