import json
import os
from pathlib import Path

import click
from PIL import Image
from tqdm import tqdm

from src.image_to_text.img_to_text import img_to_text


@click.argument("images_folder", type=Path)
@click.argument("store_folder", type=Path)
@click.argument("ocr_processor", type=str)
@click.argument("path_to_ocr_config", type=Path)
@click.option("--add_spaces", type=bool)
def func_generate_dataset(
        images_folder: Path,
        store_folder: Path,
        ocr_processor: str,
        path_to_ocr_config: Path,
        add_spaces: bool = False
):
    """
    Method to generate dataset of parsed images with OCR

    :param images_folder: Folder with images sources
    :param store_folder: Folder where to save OCR parsing results
    :param ocr_processor: Name of OCR processor to use.
           See available in image_to_text.processors.__init__.__all__
    :param path_to_ocr_config: Path to config for OCR processor
    :param add_spaces: Flag to set using spaces in parsed text
    :return: None
    """
    with open(path_to_ocr_config, "r") as fr:
        config = json.load(fr)
    store_folder.mkdir(parents=True, exist_ok=True)
    for file in tqdm(os.listdir(images_folder)):
        image = Image.open(images_folder / file)
        text = img_to_text(image, ocr_processor, config, add_spaces)
        with open(store_folder / (file.split(".")[0] + ".txt"), "w", encoding="utf-16") as fw:
            try:
                fw.write(text)
            except UnicodeEncodeError as e:
                print(e, text)


generate_dataset = click.command()(func_generate_dataset)

if __name__ == "__main__":
    generate_dataset()
