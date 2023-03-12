from pathlib import Path
import re

import click
from PIL import Image

from src.image_to_text import img_to_text
from src.text_to_code import text_to_code


def img_to_code(image: Image,
                ocr_processor="PaddleProcessor",
                ocr_config=None,
                text_to_code_processor="CodeT5Processor",
                processor_config=None,
                return_ocr_result=False):
    if ocr_config is None and ocr_processor == "PaddleProcessor":
        ocr_config = {"lang": "en"}
    if processor_config is None and text_to_code_processor == "CodeT5Processor":
        processor_config = {"model_bin_path": Path(__file__).parent.parent.parent.resolve() / "resources" / "model"}
    raw_text = img_to_text(image, ocr_processor, ocr_config)

    parsed_text = text_to_code(raw_text, text_to_code_processor, processor_config)
    spaces = [re.findall(r'^\s*', line)[0] for line in raw_text.split("\n")]

    parsed_text_with_spaces = []
    for i, line in enumerate(parsed_text.split("\n")):
        new_line = line if i >= len(spaces) else spaces[i] + line
        parsed_text_with_spaces.append(new_line)
    parsed_text = "\n".join(parsed_text_with_spaces)
    
    if return_ocr_result:
        return raw_text, parsed_text
    else:
        return parsed_text


@click.argument("img_path", type=Path)
def func_img_to_code(img_path: Path):
    image = Image.open(img_path)
    print(img_to_code(image))


f_img_to_code = click.command()(func_img_to_code)

if __name__ == "__main__":
    f_img_to_code()
