from os import sep
from pathlib import Path

def unify_path(str_path: str) -> str:
    if sep == "\\":
        return str_path.replace("/", "\\")
    if sep == "/":
        return str_path.replace("\\", "/")
    assert ValueError("Unknown OS file delimiter")


def get_project_path() -> Path:
    return Path(__file__).parent.parent
