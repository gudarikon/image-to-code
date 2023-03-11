import json
from pathlib import Path

import click
from PIL import Image

import src.image_to_text.processors as processors
from src.image_to_text.processors.ocr_processor import OCRProcessor
from src.image_to_text.utils import prepare_image


def _get_processor(ocr_processor: str) -> type:
    """
    Method to get given by string OCRProcessor class

    :param ocr_processor: name of OCRProcessor. See available in image_to_text.processors.__init__.__all__
    :return: class of OCRProcessor
    """
    assert ocr_processor in processors.__all__, f"No given processor found. Try one of {processors.__all__}"
    processor = getattr(processors, ocr_processor)
    return processor


def img_to_text(image: Image, ocr_processor: str, ocr_config: dict, add_spaces: bool = False):
    """
    Method to extract text from image using certain OCRProcessor

    :param image: source PIL Image object
    :param ocr_processor: name of OCRProcessor. See available in image_to_text.processors.__init__.__all__
    :param ocr_config: Path to config for OCR processor
    :param add_spaces: Flag to set using spaces in parsed text
    :return: Parsed text
    """
    processor = _get_processor(ocr_processor)
    processor_obj: OCRProcessor = processor(**ocr_config)
    image = prepare_image(image)
    text = processor_obj.process_image(image, add_spaces)
    return text


@click.argument("img_path", type=Path)
@click.argument("ocr_processor", type=str)
@click.argument("path_to_ocr_config", type=Path)
@click.option("--add_spaces", type=bool)
def func_img_to_text(img_path: Path, ocr_processor: str, path_to_ocr_config: Path, add_spaces: bool = False):
    """
    Method to call from console to extract text from image

    :param img_path: Path to img file
    :param ocr_processor: name of OCRProcessor. See available in image_to_text.processors.__init__.__all__
    :param path_to_ocr_config: Path to config for OCR processor
    :param add_spaces: Flag to set using spaces in parsed text
    :return: None
    """
    image = Image.open(img_path)
    with open(path_to_ocr_config, "r") as fr:
        config = json.load(fr)
    print(img_to_text(image, ocr_processor, config, add_spaces))


f_img_to_text = click.command()(func_img_to_text)

if __name__ == "__main__":
    f_img_to_text()
