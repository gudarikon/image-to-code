from pathlib import Path

import click
from PIL import Image

from src.image_to_text import img_to_text
from src.text_to_code import text_to_code


def img_to_code(image: Image,
                ocr_processor: str = "PaddleProcessor",
                ocr_config: dict = None,
                text_to_code_processor: str = "CodeT5Processor",
                processor_config: dict = None,
                return_ocr_result: bool = False):
    if ocr_config is None and ocr_processor == "PaddleProcessor":
        ocr_config = {"lang": "en"}
    if processor_config is None and text_to_code_processor == "CodeT5Processor":
        processor_config = {
            "model_bin_path": Path(__file__).parent.parent.parent.resolve() / "resources" / "model" / "codet5_model.bin"
        }

    raw_text = img_to_text(image, ocr_processor, ocr_config, True)
    parsed_text = text_to_code(raw_text, text_to_code_processor, processor_config)

    if return_ocr_result:
        return raw_text, parsed_text
    return parsed_text


@click.argument("img_path", type=Path)
def func_img_to_code(img_path: Path):
    image = Image.open(img_path)
    print(img_to_code(image))


f_img_to_code = click.command()(func_img_to_code)

if __name__ == "__main__":
    f_img_to_code()
