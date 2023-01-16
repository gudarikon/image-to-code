from pathlib import Path
from typing import List, Union

import click
from utils import preprocess_text


def text_to_code(source_text: Union[str, List[str]]):
    source_text = preprocess_text(source_text)


@click.argument("text_path", type=Path)
def func_text_to_code(text_path: Path):
    with open(text_path, "r") as f:
        text = [line.rstrip() for line in f]
    print(text_to_code(text))


f_text_to_code = click.command()(func_text_to_code)

if __name__ == "__main__":
    f_text_to_code()
