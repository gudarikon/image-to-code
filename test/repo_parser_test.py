from unittest import TestCase

from src.code_to_image.repo_parser import *


class TestRepoParser(TestCase):
    """
    Check that repo parser finds files by prefix
    """
    def test_parse_repo(self):
        repo_files = parse_repo("../src", [".py"])
        root = Path("../src/code_to_image")

        assert (repo_files[str(root / "repo_parser.py")] != -1)
        assert (repo_files[str(root / "dataset_parser.py")] != -1)
        assert (repo_files[str(root / "main_functions.py")] != -1)
        assert (repo_files[str(root / "main_code_blocks.py")] != -1)
        assert (repo_files[str(root / "config.py")] != -1)
        assert (repo_files[str(root / "config_builder.py")] != -1)
