from pathlib import Path


def unify_path(str_path: str) -> str:
    return str(Path(str_path))


def get_project_path() -> Path:
    return Path(__file__).parent.parent
