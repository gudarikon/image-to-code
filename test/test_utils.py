from pathlib import Path, PurePosixPath, PureWindowsPath

import pytest

from src import get_project_path, unify_path


def test_get_project_path():
    assert Path(__file__).parent.parent == get_project_path()


@pytest.mark.parametrize(
    ("path1", "path2"),
    [
        ("src/path1/path2/file.txt", "src\\path1\\path2\\file.txt"),
        (Path("src/path1/path2/file.txt"), Path("src\\path1\\path2\\file.txt")),
        (PurePosixPath("src/path1/path2/file.txt"), PurePosixPath("src\\path1\\path2\\file.txt")),
        (PureWindowsPath("src/path1/path2/file.txt"), PureWindowsPath("src\\path1\\path2\\file.txt")),
        (PureWindowsPath("src/path1/path2/file.txt"), PurePosixPath("src\\path1\\path2\\file.txt")),
        (PurePosixPath("src/path1/path2/file.txt"), PureWindowsPath("src\\path1\\path2\\file.txt"))
    ]
)
def test_unify_path(path1, path2):
    assert unify_path("src/path1/path2/file.txt") == unify_path("src\\path1\\path2\\file.txt")

