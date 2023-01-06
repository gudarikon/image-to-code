import json
import os
from pathlib import Path

import click
import pandas as pd
from tqdm import tqdm

from utils import preprocess_text


@click.argument("image_folder", type=Path)
@click.argument("code_folder", type=Path)
@click.argument("tesseract_preds", type=Path)
@click.argument("store_path", type=Path)
def prepare_dataset(image_folder: Path, code_folder: Path, tesseract_preds: Path, store_path: Path):
    image_paths = []
    codes = []
    preds = []

    for file in tqdm(os.listdir(image_folder)):
        pure_name = file.split(".")[0]
        with open(code_folder / (pure_name + ".json")) as fr:
            codes.append(preprocess_text(json.load(fr)["code"]))
        with open(tesseract_preds / (pure_name + ".txt"), "r", encoding="utf-16") as fr:
            preds.append(preprocess_text(fr.read()))
        image_paths.append(str(image_folder / file))

    df = pd.DataFrame({"image_path": image_paths,
                       "source_code": codes,
                       "tesseract_code:": preds})
    df.to_csv(store_path, encoding="utf-16")


f_prepare_dataset = click.command()(prepare_dataset)

if __name__ == "__main__":
    f_prepare_dataset()
