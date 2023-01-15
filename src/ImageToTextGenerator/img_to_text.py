from pathlib import Path

import click
import numpy as np
from paddleocr import PaddleOCR

from utils import prepare_image
from paddleocr import PaddleOCR


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


def init_paddle():
    return PaddleOCR(use_angle_cls=True,lang='en')  # load model into memory


def paddle_img_to_text(ocr, img_path: Path):
    result = ocr.ocr(str(img_path), cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)


f_img_to_text = click.command()(func_img_to_text)

if __name__ == "__main__":
    #f_img_to_text()
    ocr = init_paddle()
    path = Path('C:\\data_no_ligatures\\code_images\\1.png')
    paddle_img_to_text(ocr, path)
