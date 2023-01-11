import os
from pathlib import Path

import click
from tqdm import tqdm

from .img_to_text import paddle_img_to_text


@click.argument("images_folder", type=Path)
@click.argument("store_folder", type=Path)
def func_generate_dataset(images_folder: Path, store_folder: Path):
    store_folder.mkdir(parents=True, exist_ok=True)
    for file in tqdm(os.listdir(images_folder)):
        text = paddle_img_to_text(images_folder / file)
        with open(store_folder / (file.split(".")[0] + ".txt"), "w", encoding="utf-16") as fw:
            try:
                fw.write(text)
            except UnicodeEncodeError as e:
                print(e, text)


generate_dataset = click.command()(func_generate_dataset)

if __name__ == "__main__":
    generate_dataset()
