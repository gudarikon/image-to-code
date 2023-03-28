from os import sep
from pathlib import Path
from typing import Union


def unify_path(str_path: Union[str, Path]) -> str:
    if isinstance(str_path, Path):
        str_path = str(str_path)
    if sep == "\\":
        return str_path.replace("/", "\\")
    if sep == "/":
        return str_path.replace("\\", "/")
    raise ValueError("Unknown OS file delimiter")


def get_project_path() -> Path:
    return Path(__file__).parent.parent
