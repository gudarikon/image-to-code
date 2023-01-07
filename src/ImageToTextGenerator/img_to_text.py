from pathlib import Path

import click
import numpy as np
from paddleocr import PaddleOCR

from utils import prepare_image


def paddle_img_to_text(img_path: Path):
    ocr = PaddleOCR(use_angle_cls=True, lang="en")
    image = prepare_image(img_path)
    result = ocr.ocr(np.array(image), cls=False)[0]
    texts = [line[1][0] for line in result]
    texts = "\n".join(texts)
    return texts


@click.argument("img_path", type=Path)
def func_img_to_text(img_path: Path):
    print(paddle_img_to_text(img_path))


f_img_to_text = click.command()(func_img_to_text)

if __name__ == "__main__":
    f_img_to_text()
