import json
from pathlib import Path
from typing import List, Union

import click

from src.TextToCodeGeneration.TextToCodeProcessors.text_to_code_processor import TextToCodeProcessor
import src.TextToCodeGeneration.TextToCodeProcessors as T2CPr


def _get_processor(text_to_code_processor: str):
    assert text_to_code_processor in T2CPr.__all__, f"No given processor found. Try one of {T2CPr.__all__}"
    processor = getattr(T2CPr, text_to_code_processor)
    return processor


def text_to_code(text: Union[str, List[str]], text_to_code_processor: str, processor_config: dict):
    processor = _get_processor(text_to_code_processor)
    processor_obj: TextToCodeProcessor = processor(**processor_config)
    text = processor_obj.predict(text)
    return text


@click.argument("text_path", type=Path)
@click.argument("text_to_code_processor", type=str)
@click.argument("path_to_processor_config", type=Path)
def func_text_to_code(text_path: Path, text_to_code_processor: str, path_to_processor_config: Path):
    with open(text_path, "r") as f:
        text = [line.rstrip() for line in f]
    with open(path_to_processor_config, "r") as fr:
        config = json.load(fr)
    print(text_to_code(text, text_to_code_processor, config))


f_text_to_code = click.command()(func_text_to_code)

if __name__ == "__main__":
    f_text_to_code()
