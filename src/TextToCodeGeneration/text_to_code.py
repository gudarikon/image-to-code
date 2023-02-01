from pathlib import Path
from typing import List, Union

import click
from utils import preprocess_text
from model import Text2CodeModel


# TODO in telegram bot we should use singleton model!
def text_to_code(source_text: Union[str, List[str]], model_path: str = "./pytorch_model.bin"):
    source_text = preprocess_text(source_text)
    model = Text2CodeModel(model_path)
    return model.predict(source_text)


# you can launch like:
# python3 ./text_to_code.py code_example.txt '/path/to/pytorch_model.bin'
@click.argument("text_path", type=Path)
@click.argument("model_path", type=Path)
def func_text_to_code(text_path: Path, model_path: Path):
    with open(text_path, "r") as f:
        text = [line.rstrip() for line in f]
    print(text_to_code(text, str(model_path)))


f_text_to_code = click.command()(func_text_to_code)

if __name__ == "__main__":
    f_text_to_code()
