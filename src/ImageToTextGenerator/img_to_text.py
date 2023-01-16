import json
from pathlib import Path

import click
from PIL import Image

from OCRProcessors.ocr_processor import OCRProcessor
from utils import prepare_image
import OCRProcessors as Op


def _get_processor(ocr_processor: str):
    assert ocr_processor in Op.__all__, f"No given processor found. Try one of {Op.__all__}"
    processor = getattr(Op, ocr_processor)
    return processor


def img_to_text(image: Image, ocr_processor: str, ocr_config: dict):
    processor = _get_processor(ocr_processor)
    processor_obj: OCRProcessor = processor(**ocr_config)
    image = prepare_image(image)
    text = processor_obj.process_image(image)
    return text


@click.argument("img_path", type=Path)
@click.argument("ocr_processor", type=str)
@click.argument("path_to_ocr_config", type=Path)
def func_img_to_text(img_path: Path, ocr_processor: str, path_to_ocr_config: Path):
    image = Image.open(img_path)
    with open(path_to_ocr_config, "r") as fr:
        config = json.load(fr)
    print(img_to_text(image, ocr_processor, config))


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
