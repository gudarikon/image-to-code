from os import sep
from pathlib import Path, PurePosixPath, PureWindowsPath


def unify_path(str_path: str) -> str:
    if sep == "\\":
        return str(PureWindowsPath(Path(str_path)))
    if sep == "/":
        return str(PurePosixPath(Path(str_path)))
    assert ValueError("Unknown OS file delimiter")


def get_project_path() -> Path:
    return Path(__file__).parent.parent
