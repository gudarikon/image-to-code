from pathlib import Path

from src import get_project_path, unify_path


def test_get_project_path():
    assert Path(__file__).parent.parent == get_project_path()


def test_unify_path():
    assert unify_path("src/path1/path2/file.txt") == unify_path("src\\path1\\path2\\file.txt")
